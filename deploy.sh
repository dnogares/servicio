#!/bin/bash

# Script de despliegue para Easypanel
# Pipeline GIS Catastral

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                    PIPELINE GIS CATASTRAL - DESPLIEGUE                       ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Verificar Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado. Por favor, instala Docker primero."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose no está instalado. Por favor, instala Docker Compose primero."
    exit 1
fi

echo "✅ Docker y Docker Compose detectados"
echo ""

# Crear volumen FUENTES si no existe
echo "📁 Verificando volumen FUENTES..."
if [ ! -d "/app/FUENTES" ]; then
    echo "⚠️  El volumen /app/FUENTES no existe."
    echo "   Por favor, créalo en Easypanel antes de continuar."
    echo ""
    read -p "¿Deseas continuar de todos modos? (y/n): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✅ Volumen /app/FUENTES encontrado"
fi

echo ""
echo "🏗️  Construyendo imágenes Docker..."
docker-compose build

if [ $? -ne 0 ]; then
    echo "❌ Error al construir las imágenes"
    exit 1
fi

echo ""
echo "🚀 Iniciando servicios..."
docker-compose up -d

if [ $? -ne 0 ]; then
    echo "❌ Error al iniciar los servicios"
    exit 1
fi

echo ""
echo "✅ Despliegue completado con éxito!"
echo ""
echo "📊 Estado de los servicios:"
docker-compose ps

echo ""
echo "🌐 Acceso:"
echo "   Frontend: http://localhost"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "📝 Ver logs:"
echo "   docker-compose logs -f"
echo ""
echo "🛑 Detener servicios:"
echo "   docker-compose down"
echo ""
