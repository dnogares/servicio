# 🚀 Configuración Rápida en Easypanel (2 Servicios)

## 📦 SERVICIO 1: Backend (catastral-backend)

```yaml
CONFIGURACIÓN BÁSICA:
  Nome: catastral-backend
  Tipo: App → From Source
  
GIT:
  Repository: https://github.com/TU-USUARIO/pipeline-catastral.git
  Branch: main
  
BUILD:
  Context: backend
  Dockerfile: backend/Dockerfile
  
NETWORKING:
  Port: 8000
  Domain: api.catastral.tudominio.com (opcional)
  
ENVIRONMENT VARIABLES:
  PYTHONUNBUFFERED: 1
  MPLBACKEND: Agg
  
VOLUMES:
  /app/FUENTES → fuentes (volumen existente con tus GPKGs)
  /app/data → backend-data (nuevo volumen)
  
HEALTH CHECK:
  Path: /health
  Port: 8000
  Interval: 30s
```

---

## 🎨 SERVICIO 2: Frontend (catastral-frontend)

```yaml
CONFIGURACIÓN BÁSICA:
  Nombre: catastral-frontend
  Tipo: App → From Source
  
GIT:
  Repository: https://github.com/TU-USUARIO/pipeline-catastral.git
  Branch: main
  
BUILD:
  Context: frontend
  Dockerfile: frontend/Dockerfile
  
NETWORKING:
  Port: 80
  Domain: catastral.tudominio.com (principal)
  SSL: ✅ Activar
  
ENVIRONMENT VARIABLES:
  VITE_API_URL: http://catastral-backend:8000
  
HEALTH CHECK:
  Path: /
  Port: 80
  Interval: 30s
```

---

## 🔗 Comunicación entre Servicios

En Easypanel, los servicios en el mismo proyecto pueden comunicarse usando sus **nombres**:

- Frontend → Backend: `http://catastral-backend:8000`
- Esto ya está configurado en `frontend/nginx.conf`

---

## ✅ Checklist de Despliegue

- [ ] Volumen `fuentes` creado y poblado con archivos GPKG
- [ ] Código subido a repositorio Git
- [ ] Servicio Backend creado y desplegado
- [ ] Servicio Frontend creado y desplegado
- [ ] Dominio configurado con SSL
- [ ] Health checks pasando (verde)
- [ ] Probar subiendo `ejemplo_referencias.txt`

---

## 🧪 Verificación

```bash
# Health check backend
curl https://api.catastral.tudominio.com/health

# Debería devolver:
{"status":"healthy"}

# Frontend
curl https://catastral.tudominio.com

# Debería devolver HTML
```

---

## 🔧 Ajustes Post-Despliegue

### Si backend y frontend no se comunican:

1. **Verificar nombre del servicio backend en Easypanel**
2. **Actualizar en `frontend/nginx.conf`:**
   ```nginx
   proxy_pass http://NOMBRE-EXACTO-DEL-BACKEND:8000/;
   ```
3. **Rebuild del frontend**

### Si falta el volumen FUENTES:

1. Crear volumen en Easypanel: nombre `fuentes`
2. Subir archivos vía SFTP al servidor
3. Copiar a `/var/lib/docker/volumes/fuentes/_data/`
4. Reiniciar backend

---

## 📊 Recursos Recomendados

| Componente | CPU | RAM | Disk |
|------------|-----|-----|------|
| Backend | 1-2 cores | 2-4 GB | - |
| Frontend | 0.5 cores | 512 MB | - |
| Volumen fuentes | - | - | 5-20 GB |
| Volumen backend-data | - | - | 10-50 GB |

---

## 🎯 URLs Finales

Después del despliegue:

- **App Principal**: https://catastral.tudominio.com
- **API Docs**: https://catastral.tudominio.com/api/docs
- **Health Backend**: https://catastral.tudominio.com/api/health
- **Direct Backend** (opcional): https://api.catastral.tudominio.com
