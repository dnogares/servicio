import sys
import io
import asyncio
import shutil
import uuid
import zipfile
import threading
import time
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

# Configurar salida estándar a UTF-8 para evitar errores de emojis en Windows
if sys.stdout and hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if sys.stderr and hasattr(sys.stderr, 'buffer'):
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks, APIRouter
from fastapi.responses import FileResponse, StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from logic.orquestador2 import OrquestadorPipeline

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN DE RUTAS PARA MODO PORTABLE (PyInstaller)
# ═══════════════════════════════════════════════════════════════════════════

def get_base_path():
    """Retorna la ruta base del ejecutable o del script."""
    if hasattr(sys, '_MEIPASS'):
        # Estamos en un bundle de PyInstaller
        return Path(sys._MEIPASS)
    return Path.cwd()

BASE_PATH = get_base_path()

# Directorios de datos (fuera del bundle, en el mismo directorio que el .exe)
# Si estamos en dev, Path.cwd() es la raíz del proyecto.
# Si estamos en exe, sys.executable nos da la ruta del .exe.
if hasattr(sys, '_MEIPASS'):
    EXE_DIR = Path(sys.executable).parent
else:
    EXE_DIR = Path.cwd()

BASE_DIR = EXE_DIR / "data"
FUENTES_DIR = EXE_DIR / "FUENTES"
UPLOADS_DIR = BASE_DIR / "uploads"
OUTPUTS_DIR = BASE_DIR / "OUTPUTS"

# Ruta del frontend (dentro del bundle si es portable, o en frontend/dist en dev)
FRONTEND_DIR = BASE_PATH / "frontend" / "dist"

# Crear directorios de ejecución
BASE_DIR.mkdir(parents=True, exist_ok=True)
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
FUENTES_DIR.mkdir(parents=True, exist_ok=True)

# ═══════════════════════════════════════════════════════════════════════════
# APP FASTAPI
# ═══════════════════════════════════════════════════════════════════════════

app = FastAPI(
    title="Pipeline GIS Catastral",
    description="API para procesamiento automatizado de referencias catastrales",
    version="1.0.0"
)

# CORS opcional (útil en desarrollo si el frontend corre en otro puerto)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Estado de los procesos
procesos_activos = {}

# ═══════════════════════════════════════════════════════════════════════════
# ENDPOINTS API (Prefijo /api para coincidir con el frontend)
# ═══════════════════════════════════════════════════════════════════════════

api_router = APIRouter()

@api_router.get("/")
async def api_root():
    return {"status": "ok", "message": "API del Pipeline GIS Catastral"}

@api_router.get("/health")
async def health():
    return {"status": "healthy"}

@api_router.get("/info")
async def info():
    fuentes_ok = FUENTES_DIR.exists()
    fuentes_archivos = len(list(FUENTES_DIR.rglob("*.gpkg"))) if fuentes_ok else 0
    return {
        "servicio": "Pipeline GIS Catastral",
        "version": "1.0.0",
        "directorios": {
            "exe_dir": str(EXE_DIR),
            "fuentes": str(FUENTES_DIR),
            "outputs": str(OUTPUTS_DIR)
        },
        "estadisticas": {
            "fuentes_gpkg_count": fuentes_archivos,
            "procesos_activos": len(procesos_activos)
        }
    }

@api_router.post("/upload")
async def upload_file(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    if not file.filename.endswith('.txt'):
        raise HTTPException(status_code=400, detail="Solo se aceptan archivos .txt")
    
    proceso_id = str(uuid.uuid4())
    archivo_path = UPLOADS_DIR / f"{proceso_id}_{file.filename}"
    
    try:
        contenido = await file.read()
        archivo_path.write_bytes(contenido)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error guardando archivo: {str(e)}")
    
    procesos_activos[proceso_id] = {
        "estado": "procesando",
        "progreso": 0,
        "mensaje": "Iniciando...",
        "logs": [],
        "geometrias": [],
        "carpeta_resultado": None
    }
    
    background_tasks.add_task(procesar_archivo_task, proceso_id, archivo_path)
    
    return {"proceso_id": proceso_id}

@api_router.get("/status/{proceso_id}")
async def get_status(proceso_id: str):
    if proceso_id not in procesos_activos:
        raise HTTPException(status_code=404, detail="Proceso no encontrado")
    return procesos_activos[proceso_id]

@api_router.get("/logs/{proceso_id}")
async def get_logs(proceso_id: str):
    if proceso_id not in procesos_activos:
        raise HTTPException(status_code=404, detail="Proceso no encontrado")
    return {"logs": procesos_activos[proceso_id]["logs"]}

@api_router.get("/download/{proceso_id}")
async def download_results(proceso_id: str):
    if proceso_id not in procesos_activos or procesos_activos[proceso_id]["estado"] != "completado":
        raise HTTPException(status_code=400, detail="Proceso no listo")
    
    carpeta_resultado = Path(procesos_activos[proceso_id]["carpeta_resultado"])
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for archivo in carpeta_resultado.rglob('*'):
            if archivo.is_file():
                zip_file.write(archivo, archivo.relative_to(carpeta_resultado.parent))
    
    zip_buffer.seek(0)
    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename={carpeta_resultado.name}.zip"}
    )

def procesar_archivo_task(proceso_id: str, archivo_path: Path):
    def atualizar_progreso(msg: str):
        if proceso_id in procesos_activos:
            procesos_activos[proceso_id]["logs"].append(msg)
            procesos_activos[proceso_id]["mensaje"] = msg
            if "PIPELINE COMPLETO FINALIZADO" in msg:
                procesos_activos[proceso_id]["progreso"] = 100

    def nueva_geometria(refcat: str, coords: list):
        if proceso_id in procesos_activos:
            # Convertir (lon, lat) a (lat, lon) para Leaflet
            lat_lon = [[lat, lon] for lon, lat in coords]
            procesos_activos[proceso_id]["geometrias"].append({
                "refcat": refcat,
                "coords": lat_lon
            })

    try:
        orquestador = OrquestadorPipeline(
            base_dir=BASE_DIR,
            fuentes_dir=FUENTES_DIR,
            progress_callback=atualizar_progreso,
            geometry_callback=nueva_geometria
        )
        # Aseguramos que INPUTS existe en BASE_DIR
        inputs_dir = BASE_DIR / "INPUTS"
        inputs_dir.mkdir(exist_ok=True)
        dest_path = inputs_dir / archivo_path.name
        shutil.copy(archivo_path, dest_path)
        
        res = orquestador.procesar_archivo_txt(dest_path)
        if res:
            procesos_activos[proceso_id]["estado"] = "completado"
            procesos_activos[proceso_id]["progreso"] = 100
            procesos_activos[proceso_id]["carpeta_resultado"] = str(res)
        else:
            procesos_activos[proceso_id]["estado"] = "error"
    except Exception as e:
        procesos_activos[proceso_id]["estado"] = "error"
        procesos_activos[proceso_id]["error"] = str(e)
    finally:
        if archivo_path.exists():
            archivo_path.unlink()

# Mas endpoints si son necesarios...

# ═══════════════════════════════════════════════════════════════════════════
# MONTAJE DE API Y FRONTEND
# ═══════════════════════════════════════════════════════════════════════════

app.include_router(api_router, prefix="/api")

# Servir el frontend
from fastapi.staticfiles import StaticFiles

if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
else:
    print(f"⚠️ Advertencia: No se encontró el directorio del frontend en {FRONTEND_DIR}")
    @app.get("/")
    async def fallback_root():
        return {"error": "Frontend no encontrado. Asegúrate de compilarlo con 'npm run build'."}

if __name__ == "__main__":
    import uvicorn
    import webbrowser
    
    port = 8000
    # Abrir el navegador automáticamente en modo portable
    if hasattr(sys, '_MEIPASS'):
        threading.Thread(target=lambda: (time.sleep(1.5), webbrowser.open(f"http://localhost:{port}")), daemon=True).start()
    
    uvicorn.run(app, host="0.0.0.0", port=port, log_config=None)
