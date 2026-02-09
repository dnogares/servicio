"""
FastAPI Backend para Pipeline GIS Catastral
"""
import asyncio
import shutil
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional
import zipfile
import io

from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from logic.orquestador2 import OrquestadorPipeline

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ═══════════════════════════════════════════════════════════════════════════

app = FastAPI(
    title="Pipeline GIS Catastral",
    description="API para procesamiento automatizado de referencias catastrales",
    version="1.0.0"
)

# CORS para permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominio exacto
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directorios
BASE_DIR = Path("/app/data") if Path("/app/data").exists() else Path.cwd() / "data"
FUENTES_DIR = Path("/app/FUENTES") if Path("/app/FUENTES").exists() else Path.cwd() / "FUENTES"
UPLOADS_DIR = BASE_DIR / "uploads"
OUTPUTS_DIR = BASE_DIR / "OUTPUTS"

# Crear directorios
BASE_DIR.mkdir(parents=True, exist_ok=True)
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
FUENTES_DIR.mkdir(parents=True, exist_ok=True)

# Estado de los procesos
procesos_activos = {}

# ═══════════════════════════════════════════════════════════════════════════
# MODELOS
# ═══════════════════════════════════════════════════════════════════════════

class ProcesoStatus(BaseModel):
    proceso_id: str
    estado: str  # "procesando", "completado", "error"
    progreso: int  # 0-100
    mensaje: str
    carpeta_resultado: Optional[str] = None
    error: Optional[str] = None

# ═══════════════════════════════════════════════════════════════════════════
# ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════

@app.get("/")
async def root():
    """Endpoint de salud."""
    return {
        "servicio": "Pipeline GIS Catastral",
        "version": "1.0.0",
        "estado": "activo",
        "fuentes_dir": str(FUENTES_DIR),
        "outputs_dir": str(OUTPUTS_DIR)
    }

@app.get("/health")
async def health():
    """Health check para Easypanel."""
    return {"status": "healthy"}

@app.get("/info")
async def info():
    """Información detallada del servicio."""
    # Verificar si FUENTES existe y tiene archivos
    fuentes_ok = FUENTES_DIR.exists()
    fuentes_archivos = 0
    if fuentes_ok:
        fuentes_archivos = len(list(FUENTES_DIR.rglob("*.gpkg")))
    
    # Contar archivos en OUTPUTS
    outputs_archivos = 0
    if OUTPUTS_DIR.exists():
        outputs_archivos = len(list(OUTPUTS_DIR.rglob("*")))
    
    return {
        "servicio": "Pipeline GIS Catastral",
        "version": "1.0.0",
        "estado": "activo",
        "descripcion": "Procesamiento automatizado de referencias catastrales - 19 pasos",
        "directorios": {
            "base": str(BASE_DIR),
            "fuentes": str(FUENTES_DIR),
            "uploads": str(UPLOADS_DIR),
            "outputs": str(OUTPUTS_DIR)
        },
        "estadisticas": {
            "fuentes_disponible": fuentes_ok,
            "fuentes_gpkg_count": fuentes_archivos,
            "outputs_archivos": outputs_archivos,
            "procesos_activos": len(procesos_activos),
            "procesos_completados": len([p for p in procesos_activos.values() if p["estado"] == "completado"]),
            "procesos_en_curso": len([p for p in procesos_activos.values() if p["estado"] == "procesando"]),
            "procesos_error": len([p for p in procesos_activos.values() if p["estado"] == "error"])
        },
        "endpoints": {
            "root": "/",
            "health": "/health",
            "info": "/info",
            "upload": "POST /upload",
            "status": "GET /status/{proceso_id}",
            "logs": "GET /logs/{proceso_id}",
            "download": "GET /download/{proceso_id}",
            "delete": "DELETE /proceso/{proceso_id}",
            "list": "GET /procesos"
        }
    }

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None
):
    """
    Sube un archivo .txt con referencias catastrales y comienza el procesamiento.
    
    Returns:
        proceso_id para consultar el estado
    """
    # Validar extensión
    if not file.filename.endswith('.txt'):
        raise HTTPException(status_code=400, detail="Solo se aceptan archivos .txt")
    
    # Generar ID único para este proceso
    proceso_id = str(uuid.uuid4())
    
    # Guardar archivo
    archivo_path = UPLOADS_DIR / f"{proceso_id}_{file.filename}"
    
    try:
        contenido = await file.read()
        archivo_path.write_bytes(contenido)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error guardando archivo: {str(e)}")
    
    # Iniciar procesamiento en background
    procesos_activos[proceso_id] = {
        "estado": "procesando",
        "progreso": 0,
        "mensaje": "Iniciando procesamiento...",
        "logs": [],
        "carpeta_resultado": None,
        "error": None
    }
    
    # Ejecutar en background
    background_tasks.add_task(procesar_archivo, proceso_id, archivo_path)
    
    return {
        "proceso_id": proceso_id,
        "mensaje": "Procesamiento iniciado",
        "archivo": file.filename
    }

async def procesar_archivo(proceso_id: str, archivo_path: Path):
    """
    Procesa un archivo .txt con el orquestador del pipeline.
    Actualiza el estado en procesos_activos.
    """
    def actualizar_progreso(mensaje: str):
        """Callback para recibir logs del orquestrador."""
        if proceso_id in procesos_activos:
            procesos_activos[proceso_id]["logs"].append(mensaje)
            procesos_activos[proceso_id]["mensaje"] = mensaje
            
            # Estimar progreso basado en las fases (19 pasos)
            if "FASE 1" in mensaje:
                procesos_activos[proceso_id]["progreso"] = 10
            elif "FASE 2" in mensaje:
                procesos_activos[proceso_id]["progreso"] = 20
            elif "FASE 3" in mensaje:
                procesos_activos[proceso_id]["progreso"] = 30
            elif "FASE 4" in mensaje:
                procesos_activos[proceso_id]["progreso"] = 40
            elif "FASE 5" in mensaje:
                procesos_activos[proceso_id]["progreso"] = 50
            elif "FASE 6" in mensaje:
                procesos_activos[proceso_id]["progreso"] = 60
            elif "FASE 7" in mensaje:
                procesos_activos[proceso_id]["progreso"] = 65
            elif "FASE 8" in mensaje:
                procesos_activos[proceso_id]["progreso"] = 70
            elif "FASE 9" in mensaje:
                procesos_activos[proceso_id]["progreso"] = 75
            elif "FASE 10" in mensaje:
                procesos_activos[proceso_id]["progreso"] = 80
            elif "FASE 11" in mensaje:
                procesos_activos[proceso_id]["progreso"] = 85
            elif "FASE 12" in mensaje:
                procesos_activos[proceso_id]["progreso"] = 90
            elif "PIPELINE COMPLETO FINALIZADO" in mensaje:
                procesos_activos[proceso_id]["progreso"] = 100
    
    try:
        # Crear inputs directory temporal
        inputs_dir = BASE_DIR / "INPUTS"
        inputs_dir.mkdir(exist_ok=True)
        
        # Copiar archivo a INPUTS
        shutil.copy(archivo_path, inputs_dir / archivo_path.name)
        
        # Ejecutar orquestador
        orquestador = OrquestadorPipeline(
            base_dir=BASE_DIR,
            fuentes_dir=FUENTES_DIR,
            progress_callback=actualizar_progreso
        )
        
        carpeta_resultado = orquestador.procesar_archivo_txt(
            inputs_dir / archivo_path.name
        )
        
        if carpeta_resultado:
            procesos_activos[proceso_id]["estado"] = "completado"
            procesos_activos[proceso_id]["progreso"] = 100
            procesos_activos[proceso_id]["mensaje"] = "Procesamiento completado"
            procesos_activos[proceso_id]["carpeta_resultado"] = str(carpeta_resultado)
        else:
            procesos_activos[proceso_id]["estado"] = "error"
            procesos_activos[proceso_id]["mensaje"] = "No se pudo procesar el archivo"
            procesos_activos[proceso_id]["error"] = "Sin resultados válidos"
            
    except Exception as e:
        procesos_activos[proceso_id]["estado"] = "error"
        procesos_activos[proceso_id]["mensaje"] = f"Error: {str(e)}"
        procesos_activos[proceso_id]["error"] = str(e)
    finally:
        # Limpiar archivo temporal
        if archivo_path.exists():
            archivo_path.unlink()

@app.get("/status/{proceso_id}")
async def get_status(proceso_id: str):
    """
    Consulta el estado de un proceso.
    """
    if proceso_id not in procesos_activos:
        raise HTTPException(status_code=404, detail="Proceso no encontrado")
    
    proceso = procesos_activos[proceso_id]
    
    return ProcesoStatus(
        proceso_id=proceso_id,
        estado=proceso["estado"],
        progreso=proceso["progreso"],
        mensaje=proceso["mensaje"],
        carpeta_resultado=proceso.get("carpeta_resultado"),
        error=proceso.get("error")
    )

@app.get("/logs/{proceso_id}")
async def get_logs(proceso_id: str):
    """
    Obtiene los logs completos de un proceso.
    """
    if proceso_id not in procesos_activos:
        raise HTTPException(status_code=404, detail="Proceso no encontrado")
    
    return {
        "proceso_id": proceso_id,
        "logs": procesos_activos[proceso_id]["logs"]
    }

@app.get("/download/{proceso_id}")
async def download_results(proceso_id: str):
    """
    Descarga los resultados como archivo ZIP.
    """
    if proceso_id not in procesos_activos:
        raise HTTPException(status_code=404, detail="Proceso no encontrado")
    
    proceso = procesos_activos[proceso_id]
    
    if proceso["estado"] != "completado":
        raise HTTPException(status_code=400, detail="El proceso aún no ha terminado")
    
    carpeta_resultado = Path(proceso["carpeta_resultado"])
    
    if not carpeta_resultado.exists():
        raise HTTPException(status_code=404, detail="Carpeta de resultados no encontrada")
    
    # Crear ZIP en memoria
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for archivo in carpeta_resultado.rglob('*'):
            if archivo.is_file():
                arcname = archivo.relative_to(carpeta_resultado.parent)
                zip_file.write(archivo, arcname)
    
    zip_buffer.seek(0)
    
    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={
            "Content-Disposition": f"attachment; filename={carpeta_resultado.name}.zip"
        }
    )

@app.delete("/proceso/{proceso_id}")
async def delete_proceso(proceso_id: str):
    """
    Elimina un proceso y sus archivos.
    """
    if proceso_id not in procesos_activos:
        raise HTTPException(status_code=404, detail="Proceso no encontrado")
    
    proceso = procesos_activos[proceso_id]
    
    # Eliminar carpeta de resultados si existe
    if proceso.get("carpeta_resultado"):
        carpeta = Path(proceso["carpeta_resultado"])
        if carpeta.exists():
            shutil.rmtree(carpeta)
    
    # Eliminar del estado
    del procesos_activos[proceso_id]
    
    return {"mensaje": "Proceso eliminado correctamente"}

@app.get("/procesos")
async def listar_procesos():
    """
    Lista todos los procesos activos.
    """
    return {
        "total": len(procesos_activos),
        "procesos": [
            {
                "proceso_id": pid,
                "estado": p["estado"],
                "progreso": p["progreso"],
                "mensaje": p["mensaje"]
            }
            for pid, p in procesos_activos.items()
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
