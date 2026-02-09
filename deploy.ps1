# Script de despliegue para Easypanel (PowerShell)
# Pipeline GIS Catastral

Write-Host "╔══════════════════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                    PIPELINE GIS CATASTRAL - DESPLIEGUE                       ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Verificar Docker
try {
    docker --version | Out-Null
    Write-Host "✅ Docker detectado" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker no está instalado. Por favor, instala Docker primero." -ForegroundColor Red
    exit 1
}

try {
    docker-compose --version | Out-Null
    Write-Host "✅ Docker Compose detectado" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker Compose no está instalado. Por favor, instala Docker Compose primero." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🏗️  Construyendo imágenes Docker..." -ForegroundColor Yellow
docker-compose build

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error al construir las imágenes" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🚀 Iniciando servicios..." -ForegroundColor Yellow
docker-compose up -d

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error al iniciar los servicios" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✅ Despliegue completado con éxito!" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Estado de los servicios:" -ForegroundColor Cyan
docker-compose ps

Write-Host ""
Write-Host "🌐 Acceso:" -ForegroundColor Cyan
Write-Host "   Frontend: http://localhost"
Write-Host "   Backend:  http://localhost:8000"
Write-Host "   API Docs: http://localhost:8000/docs"
Write-Host ""
Write-Host "📝 Ver logs:" -ForegroundColor Cyan
Write-Host "   docker-compose logs -f"
Write-Host ""
Write-Host "🛑 Detener servicios:" -ForegroundColor Cyan
Write-Host "   docker-compose down"
Write-Host ""
