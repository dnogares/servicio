# 🎉 WORKSPACE CONFIGURADO PARA EL EQUIPO

## ✅ Todo Listo

El workspace de desarrollo está completamente configurado y listo para que el equipo comience a trabajar.

---

## 📦 Repositorio

- **URL**: https://github.com/dnogares/servicio
- **Branch principal**: `main`
- **Estado**: ✅ Actualizado con toda la configuración del equipo

---

## 🚀 Quick Start para Nuevos Miembros

### 1. Clonar Repositorio

```bash
git clone https://github.com/dnogares/servicio.git pipeline-catastral
cd pipeline-catastral
```

### 2. Setup Automático

#### Windows:
```powershell
.\setup-dev.ps1
```

#### Linux/Mac:
```bash
chmod +x setup-dev.sh
./setup-dev.sh
```

Este script automáticamente:
- ✅ Verifica dependencias (Git, Python, Node.js, Docker)
- ✅ Crea estructura de directorios
- ✅ Configura entorno virtual Python
- ✅ Instala dependencias del backend
- ✅ Instala dependencias del frontend

### 3. Abrir en VS Code

```bash
code pipeline-catastral.code-workspace
```

**Importante**: Acepta instalar las extensiones recomendadas cuando VS Code lo sugiera.

---

## 📁 Archivos Importantes para el Equipo

| Archivo | Descripción |
|---------|-------------|
| `DESARROLLO_EQUIPO.md` | ⭐ **GUÍA PRINCIPAL** - Setup, workflow, troubleshooting |
| `CONVENCIONES.md` | Estándares de código y mejores prácticas |
| `pipeline-catastral.code-workspace` | Workspace de VS Code |
| `setup-dev.ps1` / `setup-dev.sh` | Scripts de setup automático |
| `README.md` | Documentación del proyecto |
| `BUILD_FIX_FINAL.md` | Solución para errores de build en Easypanel |

---

## 🛠️ Desarrollo Local

### Backend (Puerto 8000)

```bash
cd backend
venv\Scripts\activate     # Windows
# source venv/bin/activate  # Linux/Mac
uvicorn main:app --reload
```

**Acceso**:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

### Frontend (Puerto 3000)

```bash
cd frontend
npm run dev
```

**Acceso**: http://localhost:3000

### Docker (Todo el Stack)

```bash
# Start
docker-compose up --build

# Logs
docker-compose logs -f

# Stop
docker-compose down
```

**Acceso**:
- Frontend: http://localhost
- Backend: http://localhost:8000

---

## 💻 Features del Workspace

### ✅ VS Code Configurado

- **Formateo automático** al guardar
- **Linting** para Python (flake8) y TypeScript (ESLint)
- **Formatters**: Black (Python), Prettier (TS/JS)
- **Type checking**: Pylance y TypeScript
- **Debug configs** para backend y frontend
- **Tasks** para comandos comunes

### ✅ Extensions Recomendadas

- Python
- Pylance
- Black Formatter
- Prettier
- ESLint
- Docker
- Thunder Client (API testing)

### ✅ Launch Configurations

Presiona `F5` y selecciona:
- **Backend: FastAPI** - Debug del backend
- **Frontend: Vite Dev** - Debug del frontend

### ✅ Tasks

`Ctrl+Shift+P` → "Run Task":
- Backend: Install Dependencies
- Frontend: Install Dependencies
- Docker: Build All
- Docker: Start Services
- Docker: Stop Services

---

## 📝 Workflow de Desarrollo

### Crear Feature

```bash
# 1. Actualizar main
git checkout main
git pull origin main

# 2. Crear rama
git checkout -b feature/nombre-descriptivo

# 3. Desarrollar
# ... hacer cambios ...

# 4. Commit
git add .
git commit -m "feat: descripción del cambio"

# 5. Push
git push origin feature/nombre-descriptivo

# 6. Crear Pull Request en GitHub
```

### Convenciones de Commit

```bash
feat: Nueva funcionalidad
fix: Corrección de bug
docs: Cambios en documentación
refactor: Refactorización
style: Cambios de formato
test: Añadir tests
chore: Tareas de mantenimiento
```

Ver `CONVENCIONES.md` para más detalles.

---

## 🗂️  Estructura del Proyecto

```
pipeline-catastral/
│
├── 📂 backend/                       ← API FastAPI
│   ├── venv/                        (local, no en git)
│   ├── logic/
│   │   ├── __init__.py
│   │   └── orquestador.py          ⭐ PIPELINE PRINCIPAL
│   ├── main.py                      ⭐ ENDPOINTS API
│   ├── requirements.txt
│   └── Dockerfile
│
├── 📂 frontend/                      ← React + Vite
│   ├── node_modules/                (local, no en git)
│   ├── src/
│   │   ├── App.tsx                 ⭐ COMPONENTE PRINCIPAL
│   │   ├── App.css
│   │   ├── main.tsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.ts
│   └── Dockerfile
│
├── 📂 data/                          ← Datos locales (crear)
│   ├── INPUTS/
│   ├── OUTPUTS/
│   └── uploads/
│
├── 📂 FUENTES/                       ← Archivos GPKG (crear)
│   └── CAPAS_gpkg/
│       └── afecciones/
│
├── 📄 docker-compose.yml
├── 📄 pipeline-catastral.code-workspace  ⭐ WORKSPACE
│
├── 📚 DESARROLLO_EQUIPO.md          ⭐ GUÍA PRINCIPAL
├── 📚 CONVENCIONES.md               ⭐ ESTÁNDARES
├── 📚 README.md
├── 📚 BUILD_FIX_FINAL.md
│
├── 🚀 setup-dev.ps1                 (Windows)
└── 🚀 setup-dev.sh                  (Linux/Mac)
```

---

## 🎯 Checklist para Nuevos Miembros

- [ ] Clonar repositorio
- [ ] Ejecutar script de setup
- [ ] Abrir workspace en VS Code
- [ ] Instalar extensiones recomendadas
- [ ] Crear directorios locales (data/, FUENTES/)
- [ ] Verificar que backend inicia correctamente
- [ ] Verificar que frontend inicia correctamente
- [ ] Leer `DESARROLLO_EQUIPO.md`
- [ ] Leer `CONVENCIONES.md`
- [ ] Hacer primer commit de prueba

---

## 📚 Documentación Completa

1. **Primera vez en el proyecto**: Lee `DESARROLLO_EQUIPO.md`
2. **Antes de escribir código**: Lee `CONVENCIONES.md`
3. **Problemas con build**: Consulta `BUILD_FIX_FINAL.md`
4. **Información general**: Lee `README.md`

---

## 🐛 Troubleshooting Común

### Puerto ocupado
```bash
# Backend (8000)
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # Linux/Mac

# Kill process
taskkill /PID <PID> /F        # Windows
kill -9 <PID>                 # Linux/Mac
```

### Dependencias backend
```bash
cd backend
pip install -r requirements.txt
```

### Dependencias frontend
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Docker issues
```bash
docker-compose down -v
docker system prune -af
docker-compose up --build
```

---

## 👥 Equipo

Añadir miembros aquí:

| Nombre | Rol | GitHub | Email |
|--------|-----|--------|-------|
| ... | ... | @... | ... |

---

## 📞 Contacto

- **GitHub**: https://github.com/dnogares/servicio
- **Issues**: https://github.com/dnogares/servicio/issues

---

## ✅ Estado Actual

- ✅ Repositorio configurado
- ✅ Workspace creado
- ✅ Scripts de setup listos
- ✅ Documentación completa
- ✅ Convenciones definidas
- ✅ VS Code configurado
- ✅ Todo subido a GitHub

**🎉 El equipo puede empezar a trabajar inmediatamente**

---

Para cualquier duda, consulta `DESARROLLO_EQUIPO.md` o pregunta en el canal del equipo.

¡Bienvenid@ al equipo! 🚀
