# Script de setup para desarrollo local
# Pipeline GIS Catastral

Write-Host "╔══════════════════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║               SETUP DE DESARROLLO - PIPELINE GIS CATASTRAL                   ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

$ErrorActionPreference = "Continue"

# Función para verificar comando
function Test-Command {
    param($Command)
    try {
        Get-Command $Command -ErrorAction Stop | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

# 1. Verificar Git
Write-Host "📦 Verificando Git..." -ForegroundColor Yellow
if (Test-Command git) {
    Write-Host "✅ Git instalado" -ForegroundColor Green
    git --version
}
else {
    Write-Host "❌ Git no instalado. Descárgalo de https://git-scm.com/" -ForegroundColor Red
    exit 1
}

# 2. Verificar Python
Write-Host ""
Write-Host "🐍 Verificando Python..." -ForegroundColor Yellow
if (Test-Command python) {
    Write-Host "✅ Python instalado" -ForegroundColor Green
    python --version
}
else {
    Write-Host "❌ Python no instalado. Descárgalo de https://python.org/" -ForegroundColor Red
    exit 1
}

# 3. Verificar Node.js
Write-Host ""
Write-Host "📦 Verificando Node.js..." -ForegroundColor Yellow
if (Test-Command node) {
    Write-Host "✅ Node.js instalado" -ForegroundColor Green
    node --version
}
else {
    Write-Host "❌ Node.js no instalado. Descárgalo de https://nodejs.org/" -ForegroundColor Red
    exit 1
}

# 4. Verificar Docker (opcional)
Write-Host ""
Write-Host "🐳 Verificando Docker (opcional)..." -ForegroundColor Yellow
if (Test-Command docker) {
    Write-Host "✅ Docker instalado" -ForegroundColor Green
    docker --version
}
else {
    Write-Host "⚠️  Docker no instalado (opcional para desarrollo)" -ForegroundColor Yellow
}

# 5. Crear estructura de directorios
Write-Host ""
Write-Host "📁 Creando estructura de directorios..." -ForegroundColor Yellow

$dirs = @(
    "data/INPUTS",
    "data/OUTPUTS",
    "data/uploads",
    "FUENTES/CAPAS_gpkg/afecciones"
)

foreach ($dir in $dirs) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "✅ Creado: $dir" -ForegroundColor Green
    }
    else {
        Write-Host "⏭️  Ya existe: $dir" -ForegroundColor Gray
    }
}

# 6. Configurar backend
Write-Host ""
Write-Host "🐍 Configurando Backend Python..." -ForegroundColor Yellow

Set-Location backend

if (!(Test-Path "venv")) {
    Write-Host "Creando entorno virtual..." -ForegroundColor Cyan
    python -m venv venv
    Write-Host "✅ Entorno virtual creado" -ForegroundColor Green
}
else {
    Write-Host "⏭️  Entorno virtual ya existe" -ForegroundColor Gray
}

Write-Host "Activando entorno virtual..." -ForegroundColor Cyan
& ".\venv\Scripts\Activate.ps1"

Write-Host "Instalando dependencias..." -ForegroundColor Cyan
pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Dependencias del backend instaladas" -ForegroundColor Green
}
else {
    Write-Host "⚠️  Hubo errores al instalar dependencias" -ForegroundColor Yellow
}

Set-Location ..

# 7. Configurar frontend
Write-Host ""
Write-Host "⚛️  Configurando Frontend React..." -ForegroundColor Yellow

Set-Location frontend

Write-Host "Instalando dependencias..." -ForegroundColor Cyan
npm install

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Dependencias del frontend instaladas" -ForegroundColor Green
}
else {
    Write-Host "⚠️  Hubo errores al instalar dependencias" -ForegroundColor Yellow
}

Set-Location ..

# 8. Resumen
Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                          SETUP COMPLETADO                                    ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

Write-Host "🎯 Próximos Pasos:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Abrir VS Code con el workspace:" -ForegroundColor White
Write-Host "   code pipeline-catastral.code-workspace" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Iniciar backend (en terminal separado):" -ForegroundColor White
Write-Host "   cd backend" -ForegroundColor Gray
Write-Host "   venv\Scripts\activate" -ForegroundColor Gray
Write-Host "   uvicorn main:app --reload" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Iniciar frontend (en terminal separado):" -ForegroundColor White
Write-Host "   cd frontend" -ForegroundColor Gray
Write-Host "   npm run dev" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Acceder a:" -ForegroundColor White
Write-Host "   Frontend: http://localhost:3000" -ForegroundColor Gray
Write-Host "   Backend:  http://localhost:8000" -ForegroundColor Gray
Write-Host "   API Docs: http://localhost:8000/docs" -ForegroundColor Gray
Write-Host ""
Write-Host "📚 Documentación:" -ForegroundColor Cyan
Write-Host "   - DESARROLLO_EQUIPO.md (guía completa)" -ForegroundColor Gray
Write-Host "   - README.md (visión general)" -ForegroundColor Gray
Write-Host ""
Write-Host "🎉 ¡Listo para desarrollar!" -ForegroundColor Green
