# 🔧 Fix: Dockerfiles para Easypanel

## ✅ Problema Solucionado

**Error anterior**: 
```
ERROR: "/requirements.txt": not found
```

**Causa**: Easypanel usa el contexto de build desde la raíz del proyecto, no desde las subcarpetas como especifica docker-compose.

**Solución**: Creados nuevos Dockerfiles con paths correctos:
- `Dockerfile.backend` - Copia desde `backend/requirements.txt`
- `Dockerfile.frontend` - Copia desde `frontend/package.json`

---

## 📦 Estructura de Build

### Antes (no funcionaba en Easypanel):
```yaml
backend:
  build:
    context: ./backend      # ❌ Easypanel ignora esto
    dockerfile: Dockerfile
```

```dockerfile
COPY requirements.txt .    # ❌ Busca en raíz, no en ./backend
```

### Después (funciona en Easypanel):
```yaml
backend:
  build:
    context: .              # ✅ Contexto raíz
    dockerfile: Dockerfile.backend
```

```dockerfile
COPY backend/requirements.txt .  # ✅ Path correcto desde raíz
COPY backend/ .                   # ✅ Copia todo el backend
```

---

## 🚀 Redeployar en Easypanel

Ahora que el código está actualizado:

1. **En Easypanel** → Tu servicio → **Redeploy**
2. Easypanel detectará el nuevo commit
3. El build debería completarse sin errores

---

## 🧪 Verificar Localmente

Prueba que funciona con docker-compose:

```bash
# Limpiar builds anteriores
docker-compose down
docker system prune -f

# Build y start
docker-compose up --build

# Verificar
curl http://localhost:8000/health
# {"status":"healthy"}
```

---

## 📊 Archivos Modificados

| Archivo | Cambio |
|---------|--------|
| `Dockerfile.backend` | ✅ Nuevo - Contexto raíz |
| `Dockerfile.frontend` | ✅ Nuevo - Contexto raíz |
| `docker-compose.yml` | ✅ Actualizado - Usa nuevos Dockerfiles |
| `backend/Dockerfile` | ⚠️ Legacy - Mantener para reference |
| `frontend/Dockerfile` | ⚠️ Legacy - Mantener para reference |

---

## ✅ Commit Actualizado

```
fix: Dockerfiles con contexto raíz para compatibilidad Easypanel

- Creados Dockerfile.backend y Dockerfile.frontend
- Ajustados paths para build desde raíz del proyecto
- Actualizado docker-compose.yml
- Añadido curl al backend para healthchecks
```

**Push realizado**: ✅ https://github.com/dnogares/servicio

---

🎉 **El build ahora debería funcionar en Easypanel**
