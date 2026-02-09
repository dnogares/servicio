# 👥 GUÍA DE CONFIGURACIÓN DEL WORKSPACE PARA EL EQUIPO

## 🎯 Configuración Inicial

### 1️⃣ Clonar el Repositorio

```bash
# Clonar proyecto
git clone https://github.com/dnogares/servicio.git pipeline-catastral
cd pipeline-catastral
```

### 2️⃣ Abrir en VS Code

```bash
# Abrir workspace
code pipeline-catastral.code-workspace
```

Al abrir el workspace, VS Code te sugerirá instalar las extensiones recomendadas. **Acepta instalarlas todas**.

---

## 🐍 Configuración del Backend (Python)

### Opción A: Entorno Virtual Local (Desarrollo)

```bash
# Ir a carpeta backend
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor de desarrollo
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Acceso**: http://localhost:8000
**API Docs**: http://localhost:8000/docs

### Opción B: Docker (Más cercano a producción)

```bash
# Desde raíz del proyecto
docker-compose up backend

# Ver logs
docker-compose logs -f backend
```

---

## ⚛️ Configuración del Frontend (React + Vite)

### Opción A: Desarrollo Local

```bash
# Ir a carpeta frontend
cd frontend

# Instalar dependencias
npm install

# Ejecutar servidor de desarrollo
npm run dev
```

**Acceso**: http://localhost:3000

### Opción B: Docker

```bash
# Desde raíz del proyecto
docker-compose up frontend
```

---

## 🐳 Desarrollo con Docker (Recomendado)

### Iniciar Todo el Stack

```bash
# Build y start
docker-compose up --build

# En modo detached (segundo plano)
docker-compose up -d --build

# Ver logs en tiempo real
docker-compose logs -f

# Ver solo logs de backend
docker-compose logs -f backend

# Ver solo logs de frontend
docker-compose logs -f frontend
```

### Detener Servicios

```bash
# Detener
docker-compose down

# Detener y limpiar volúmenes
docker-compose down -v

# Detener y limpiar todo (imágenes también)
docker-compose down -v --rmi all
```

### Acceder a Contenedores

```bash
# Backend shell
docker-compose exec backend bash

# Frontend shell  
docker-compose exec frontend sh

# Ver procesos
docker-compose ps

# Ver estadísticas de recursos
docker stats
```

---

## 📁 Estructura de Directorios para Desarrollo

```
pipeline-catastral/
│
├── backend/                      ← API FastAPI
│   ├── venv/                    (crear localmente, gitignored)
│   ├── logic/
│   │   ├── __init__.py
│   │   └── orquestador.py      ⭐ PIPELINE PRINCIPAL
│   ├── main.py                  ⭐ ENDPOINTS API
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/                     ← React + Vite
│   ├── node_modules/            (npm install, gitignored)
│   ├── src/
│   │   ├── App.tsx             ⭐ COMPONENTE PRINCIPAL
│   │   ├── App.css             ⭐ ESTILOS
│   │   ├── main.tsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.ts
│   └── Dockerfile
│
├── data/                         ← Datos locales (crear)
│   ├── INPUTS/
│   ├── OUTPUTS/
│   └── uploads/
│
├── FUENTES/                      ← Archivos GPKG (crear)
│   └── CAPAS_gpkg/
│       └── afecciones/
│           ├── RGVP2024.gpkg
│           └── ...
│
├── docker-compose.yml
├── pipeline-catastral.code-workspace  ⭐ WORKSPACE
├── DESARROLLO_EQUIPO.md               ⭐ ESTA GUÍA
└── README.md
```

---

## 🗂️ Crear Directorios de Desarrollo

```bash
# Crear estructura de datos local
mkdir -p data/INPUTS data/OUTPUTS data/uploads
mkdir -p FUENTES/CAPAS_gpkg/afecciones

# Verificar
ls -la data/
ls -la FUENTES/
```

---

## 🔧 Configuración de VS Code

El workspace ya incluye:

✅ **Formateo automático** al guardar
✅ **Python linting** con flake8
✅ **Black formatter** para Python
✅ **Prettier** para TypeScript/JS/JSON
✅ **Launch configs** para debug
✅ **Tasks** para comandos comunes

### Debug en VS Code

1. **Backend**:
   - Presiona `F5`
   - Selecciona "Backend: FastAPI"
   - El servidor se iniciará en modo debug

2. **Frontend**:
   - Presiona `F5`
   - Selecciona "Frontend: Vite Dev"
   - El server de desarrollo se iniciará

### Tasks Útiles

Presiona `Ctrl+Shift+P` y escribe "Run Task":

- **Backend: Install Dependencies**
- **Frontend: Install Dependencies**
- **Docker: Build All**
- **Docker: Start Services**
- **Docker: Stop Services**

---

## 🧪 Testing

### Backend

```bash
cd backend
pytest  # (cuando se implementen tests)
```

### Frontend

```bash
cd frontend
npm test  # (cuando se implementen tests)
```

---

## 🌐 URLs de Desarrollo

| Servicio | URL Local | URL Docker |
|----------|-----------|------------|
| **Backend** | http://localhost:8000 | http://localhost:8000 |
| **Frontend** | http://localhost:3000 | http://localhost |
| **API Docs** | http://localhost:8000/docs | http://localhost:8000/docs |
| **Health Check** | http://localhost:8000/health | http://localhost:8000/health |

---

## 📝 Workflow de Desarrollo

### 1. Crear Rama de Feature

```bash
# Desde main
git checkout -b feature/nombre-del-feature

# Ejemplo:
git checkout -b feature/mejorar-logs
git checkout -b fix/error-upload
```

### 2. Hacer Cambios

```bash
# Editar archivos
# Probar localmente
# Verificar que funciona
```

### 3. Commit y Push

```bash
# Ver cambios
git status

# Añadir archivos
git add .

# Commit
git commit -m "feat: Descripción del cambio"

# Push
git push origin feature/nombre-del-feature
```

### 4. Pull Request

1. Ir a https://github.com/dnogares/servicio
2. Crear Pull Request
3. Esperar review
4. Merge a main

### 5. Actualizar Local

```bash
# Volver a main
git checkout main

# Actualizar
git pull origin main

# Borrar rama local (opcional)
git branch -d feature/nombre-del-feature
```

---

## 🔥 Comandos Rápidos (Cheatsheet)

### Git

```bash
git status                          # Ver estado
git pull origin main                # Actualizar desde remoto
git checkout -b feature/nombre      # Nueva rama
git add .                           # Añadir todos los cambios
git commit -m "mensaje"             # Commit
git push origin nombre-rama         # Push
```

### Docker

```bash
docker-compose up -d                # Start todo
docker-compose logs -f              # Ver logs
docker-compose restart backend      # Restart solo backend
docker-compose down                 # Stop todo
docker system prune -af             # Limpiar todo
```

### Backend

```bash
cd backend
venv\Scripts\activate               # Activar venv (Windows)
source venv/bin/activate            # Activar venv (Linux/Mac)
pip install -r requirements.txt     # Instalar deps
uvicorn main:app --reload           # Run server
```

### Frontend

```bash
cd frontend
npm install                         # Instalar deps
npm run dev                         # Run dev server
npm run build                       # Build producción
```

---

## 🐛 Troubleshooting

### Error: "Puerto 8000 ya en uso"

```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :8000
kill -9 <PID>
```

### Error: "Module not found" (Backend)

```bash
cd backend
pip install -r requirements.txt
```

### Error: "Module not found" (Frontend)

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Error: Docker build falla

```bash
docker-compose down -v
docker system prune -af
docker-compose up --build
```

---

## 📚 Recursos del Equipo

- **Repositorio**: https://github.com/dnogares/servicio
- **Documentación**: Ver archivos `.md` en la raíz
- **API Docs**: http://localhost:8000/docs (cuando esté corriendo)

---

## 👥 Equipo

Añadir miembros del equipo aquí:

- **Nombre** - Rol - GitHub: @username

---

## 🎯 Próximos Pasos

1. [ ] Clonar repositorio
2. [ ] Abrir workspace en VS Code
3. [ ] Instalar extensiones recomendadas
4. [ ] Configurar backend (venv o Docker)
5. [ ] Configurar frontend (npm install)
6. [ ] Crear estructura de directorios locales
7. [ ] Probar que todo funciona
8. [ ] Leer documentación completa
9. [ ] Hacer primer commit de prueba

---

¿Dudas? Consulta los archivos `.md` en la raíz del proyecto o pregunta al equipo.

🚀 **¡Bienvenido al equipo!**
