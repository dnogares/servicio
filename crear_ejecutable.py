import os
import subprocess
import shutil
from pathlib import Path

def run_command(command, cwd=None):
    print(f"🚀 Ejecutando: {command}")
    result = subprocess.run(command, shell=True, cwd=cwd)
    if result.returncode != 0:
        print(f"❌ Error en el comando: {command}")
        exit(1)

def build():
    root_dir = Path.cwd()
    backend_dir = root_dir / "backend"
    frontend_dir = root_dir / "frontend"
    dist_dir = root_dir / "dist_exe"

    print("🏗️ Iniciando proceso de creación del ejecutable...")

    # 1. Compilar Frontend
    print("\n📦 Paso 1: Compilando Frontend (React)...")
    run_command("npm install", cwd=frontend_dir)
    run_command("npm run build", cwd=frontend_dir)

    # 2. Preparar carpeta para PyInstaller
    print("\n📂 Paso 2: Preparando carpetas...")
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    dist_dir.mkdir()

    # 3. Crear el ejecutable con PyInstaller
    # Usamos --add-data para incluir el frontend y las dependencias necesarias
    # Nota: GDAL a veces requiere rutas específicas, este es un comando base
    print("\n🔨 Paso 3: Generando ejecutable con PyInstaller...")
    
    # Comando PyInstaller
    # --onefile: crea un solo .exe
    # --noconsole: no abre la ventana negra de terminal
    # --add-data: incluye el frontend compilado
    pyinstaller_cmd = (
        f'pyinstaller --onefile --noconsole '
        f'--add-data "{frontend_dir}/dist;frontend/dist" '
        f'--add-data "{backend_dir}/logic;logic" '
        f'--name "VisorCatastral" '
        f'"{backend_dir}/main.py"'
    )
    
    run_command(pyinstaller_cmd)

    print("\n✅ Proceso finalizado!")
    print(f"📍 El ejecutable se encuentra en: {root_dir}/dist/VisorCatastral.exe")

if __name__ == "__main__":
    build()
