# 🚀 GUÍA DE EJECUCIÓN LOCAL

## ⚡ START RÁPIDO

### Terminal 1: Backend (FastAPI)

```powershell
# 1. Ir a carpeta backend
cd backend

# 2. Activar entorno virtual
.\venv\Scripts\activate

# 3. Instalar dependencias (solo primera vez)
pip install -r requirements.txt

# 4. Ejecutar servidor
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Acceso Backend**:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health
- Info: http://localhost:8000/info

---

### Terminal 2: Frontend (React + Vite)

```powershell
# 1. Ir a carpeta frontend
cd frontend

# 2. Instalar dependencias (solo primera vez)
npm install

# 3. Ejecutar servidor de desarrollo
npm run dev
```

**Acceso Frontend**:
- App: http://localhost:3000 (o el puerto que indique Vite)

---

## 🧪 PROBAR LA APLICACIÓN

1. ✅ **Verifica Backend**:
   - Abre: http://localhost:8000/docs
   - Deberías ver Swagger UI

2. ✅ **Verifica Frontend**:
   - Abre: http://localhost:3000
   - Deberías ver interfaz de subida de archivos

3. ✅ **Prueba Upload**:
   - Arrastra `ejemplo_referencias.txt`
   - Observa progreso en tiempo real
   - Descarga ZIP de resultados

---

## 📁 DIRECTORIOS NECESARIOS

El backend creará automáticamente:
```
data/
├── INPUTS/
├── OUTPUTS/
└── uploads/

FUENTES/  ← Necesitas crear y poblar con archivos GPKG
└── CAPAS_gpkg/
    └── afecciones/
```

**Crear FUENTES**:
```powershell
mkdir -p FUENTES/CAPAS_gpkg/afecciones
```

---

## 🐛 TROUBLESHOOTING

### Error: "Puerto 8000 ya en uso"

```powershell
# Ver qué usa el puerto
netstat -ano | findstr :8000

# Matar proceso
taskkill /PID <PID> /F
```

### Error: "Module not found" (Backend)

```powershell
cd backend
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Error: "Cannot find module" (Frontend)

```powershell
cd frontend
rm -rf node_modules package-lock.json
npm install
```

---

## ⏹️ DETENER SERVIDORES

- **Backend**: `Ctrl+C` en la terminal del backend
- **Frontend**: `Ctrl+C` en la terminal del frontend

---

## 🔄 REINICIOS RÁPIDOS

```powershell
# Backend
cd backend
.\venv\Scripts\activate
uvicorn main:app --reload

# Frontend
cd frontend
npm run dev
```

---

## ✅ TODO FUNCIONANDO

Si ves:

**Backend**:
```
INFO: Uvicorn running on http://0.0.0.0:8000
INFO: Application startup complete
```

**Frontend**:
```
VITE vX.X.X  ready in X ms

➜  Local:   http://localhost:3000/
➜  Network: http://192.168.X.X:3000/
```

¡Estás listo! 🎉

---

## 📦 CON DOCKER (Alternativa)

Si prefieres Docker:

```powershell
# Start todo
docker-compose up --build

# Ver logs
docker-compose logs -f

# Stop
docker-compose down
```

**URLs con Docker**:
- Frontend: http://localhost
- Backend: http://localhost:8000
