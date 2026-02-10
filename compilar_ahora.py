# -*- coding: utf-8 -*-
import os
import subprocess
import shutil
from pathlib import Path

def run_command(command, cwd=None):
    print(f"[EJECUTANDO] {command}")
    result = subprocess.run(command, shell=True, cwd=cwd)
    if result.returncode != 0:
        print(f"[ERROR] Fallo en el comando: {command}")
        exit(1)

def build():
    root_dir = Path.cwd()
    backend_dir = root_dir / "backend"
    frontend_dir = root_dir / "frontend"
    dist_dir = root_dir / "dist_exe"

    print("=" * 70)
    print("INICIANDO PROCESO DE CREACION DEL EJECUTABLE")
    print("=" * 70)

    # 1. Verificar que el frontend ya esté compilado
    print("\n[PASO 1] Verificando Frontend compilado...")
    print("-" * 70)
    frontend_dist = frontend_dir / "dist"
    if not frontend_dist.exists():
        print("[ERROR] No se encuentra frontend/dist/")
        print("[INFO] Ejecuta primero: cd frontend && npm run build")
        exit(1)
    print(f"[OK] Frontend ya compilado en: {frontend_dist}")

    # 2. Crear el ejecutable con PyInstaller usando el archivo .spec
    print("\n[PASO 2] Generando ejecutable con PyInstaller...")
    print("-" * 70)
    
    # Usar el archivo .spec que ya existe
    spec_file = root_dir / "VisorCatastral.spec"
    
    if spec_file.exists():
        print(f"[INFO] Usando archivo .spec: {spec_file}")
        run_command(f'pyinstaller "{spec_file}"')
    else:
        print("[ERROR] No se encontro el archivo VisorCatastral.spec")
        exit(1)

    # 3. Crear estructura de carpetas en dist/
    print("\n[PASO 3] Creando estructura de carpetas...")
    print("-" * 70)
    dist_output = root_dir / "dist"
    
    # Crear carpetas necesarias
    (dist_output / "data" / "INPUTS").mkdir(parents=True, exist_ok=True)
    (dist_output / "data" / "OUTPUTS").mkdir(parents=True, exist_ok=True)
    (dist_output / "FUENTES" / "CAPAS_gpkg" / "afecciones").mkdir(parents=True, exist_ok=True)
    
    print("[OK] Estructura de carpetas creada:")
    print("  - dist/data/INPUTS/")
    print("  - dist/data/OUTPUTS/")
    print("  - dist/FUENTES/CAPAS_gpkg/afecciones/")

    print("\n" + "=" * 70)
    print("PROCESO FINALIZADO EXITOSAMENTE!")
    print("=" * 70)
    print(f"\n[EJECUTABLE] {dist_output / 'VisorCatastral.exe'}")
    print(f"[TAMANO APROX] 200-400 MB")
    print(f"\n[NOTA] La carpeta FUENTES/CAPAS_gpkg/afecciones/ esta vacia.")
    print(f"       Los archivos .gpkg se cargaran desde el frontend.")

if __name__ == "__main__":
    build()
