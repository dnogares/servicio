#!/bin/bash

# Script de setup para desarrollo local
# Pipeline GIS Catastral

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║               SETUP DE DESARROLLO - PIPELINE GIS CATASTRAL                   ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
GRAY='\033[0;37m'
NC='\033[0m' # No Color

# Función para verificar comando
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 1. Verificar Git
echo -e "${YELLOW}📦 Verificando Git...${NC}"
if command_exists git; then
    echo -e "${GREEN}✅ Git instalado${NC}"
    git --version
else
    echo -e "${RED}❌ Git no instalado. Instálalo con: sudo apt install git${NC}"
    exit 1
fi

# 2. Verificar Python
echo ""
echo -e "${YELLOW}🐍 Verificando Python...${NC}"
if command_exists python3; then
    echo -e "${GREEN}✅ Python instalado${NC}"
    python3 --version
else
    echo -e "${RED}❌ Python no instalado. Instálalo con: sudo apt install python3${NC}"
    exit 1
fi

# 3. Verificar Node.js
echo ""
echo -e "${YELLOW}📦 Verificando Node.js...${NC}"
if command_exists node; then
    echo -e "${GREEN}✅ Node.js instalado${NC}"
    node --version
else
    echo -e "${RED}❌ Node.js no instalado. Descárgalo de https://nodejs.org/${NC}"
    exit 1
fi

# 4. Verificar Docker (opcional)
echo ""
echo -e "${YELLOW}🐳 Verificando Docker (opcional)...${NC}"
if command_exists docker; then
    echo -e "${GREEN}✅ Docker instalado${NC}"
    docker --version
else
    echo -e "${YELLOW}⚠️  Docker no instalado (opcional para desarrollo)${NC}"
fi

# 5. Crear estructura de directorios
echo ""
echo -e "${YELLOW}📁 Creando estructura de directorios...${NC}"

dirs=(
    "data/INPUTS"
    "data/OUTPUTS"
    "data/uploads"
    "FUENTES/CAPAS_gpkg/afecciones"
)

for dir in "${dirs[@]}"; do
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
        echo -e "${GREEN}✅ Creado: $dir${NC}"
    else
        echo -e "${GRAY}⏭️  Ya existe: $dir${NC}"
    fi
done

# 6. Configurar backend
echo ""
echo -e "${YELLOW}🐍 Configurando Backend Python...${NC}"

cd backend

if [ ! -d "venv" ]; then
    echo -e "${CYAN}Creando entorno virtual...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✅ Entorno virtual creado${NC}"
else
    echo -e "${GRAY}⏭️  Entorno virtual ya existe${NC}"
fi

echo -e "${CYAN}Activando entorno virtual...${NC}"
source venv/bin/activate

echo -e "${CYAN}Instalando dependencias...${NC}"
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Dependencias del backend instaladas${NC}"
else
    echo -e "${YELLOW}⚠️  Hubo errores al instalar dependencias${NC}"
fi

deactivate
cd ..

# 7. Configurar frontend
echo ""
echo -e "${YELLOW}⚛️  Configurando Frontend React...${NC}"

cd frontend

echo -e "${CYAN}Instalando dependencias...${NC}"
npm install

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Dependencias del frontend instaladas${NC}"
else
    echo -e "${YELLOW}⚠️  Hubo errores al instalar dependencias${NC}"
fi

cd ..

# 8. Resumen
echo ""
echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                          SETUP COMPLETADO                                    ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

echo -e "${CYAN}🎯 Próximos Pasos:${NC}"
echo ""
echo -e "${NC}1. Abrir VS Code con el workspace:${NC}"
echo -e "${GRAY}   code pipeline-catastral.code-workspace${NC}"
echo ""
echo -e "${NC}2. Iniciar backend (en terminal separado):${NC}"
echo -e "${GRAY}   cd backend${NC}"
echo -e "${GRAY}   source venv/bin/activate${NC}"
echo -e "${GRAY}   uvicorn main:app --reload${NC}"
echo ""
echo -e "${NC}3. Iniciar frontend (en terminal separado):${NC}"
echo -e "${GRAY}   cd frontend${NC}"
echo -e "${GRAY}   npm run dev${NC}"
echo ""
echo -e "${NC}4. Acceder a:${NC}"
echo -e "${GRAY}   Frontend: http://localhost:3000${NC}"
echo -e "${GRAY}   Backend:  http://localhost:8000${NC}"
echo -e "${GRAY}   API Docs: http://localhost:8000/docs${NC}"
echo ""
echo -e "${CYAN}📚 Documentación:${NC}"
echo -e "${GRAY}   - DESARROLLO_EQUIPO.md (guía completa)${NC}"
echo -e "${GRAY}   - README.md (visión general)${NC}"
echo ""
echo -e "${GREEN}🎉 ¡Listo para desarrollar!${NC}"
