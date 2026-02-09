# 🚀 Guía de Despliegue en Easypanel

## 📋 Prerequisitos

1. ✅ Cuenta activa en Easypanel
2. ✅ Servidor con Docker instalado
3. ✅ Acceso SSH al servidor (opcional, para debugging)

## 🔧 Paso 1: Preparar el Volumen FUENTES

El pipeline necesita acceso a archivos geoespaciales (capas GPKG) almacenados en `/app/FUENTES`.

### Opción A: Crear Volumen en Easypanel UI

1. Ve a tu proyecto en Easypanel
2. Navega a **Volumes** → **Create Volume**
3. Configuración:
   - **Name**: `fuentes`
   - **Mount Path**: `/app/FUENTES`
   - **Size**: Mínimo 5GB (dependiendo de tus datos)

### Opción B: Subir Archivos vía SFTP/SSH

```bash
# Conectar al servidor
ssh usuario@tu-servidor.com

# Crear directorio
sudo mkdir -p /app/FUENTES/CAPAS_gpkg/afecciones

# Subir archivos GPKG (ejemplo)
scp tu-archivo.gpkg usuario@tu-servidor:/app/FUENTES/CAPAS_gpkg/afecciones/
```

## 📦 Paso 2: Desplegar la Aplicación

### Método 1: Desde Git (Recomendado)

1. **Crear nuevo proyecto en Easypanel**
   - Click en **+ New Project**
   - Nombre: `pipeline-catastral`

2. **Añadir servicio Backend**
   - Click en **+ Add Service** → **From Source**
   - Repository: URL de tu repositorio Git
   - Branch: `main`
   - Context: `backend`
   - Dockerfile: `backend/Dockerfile`
   - Port: `8000`
   - Environment Variables:
     ```
     PYTHONUNBUFFERED=1
     MPLBACKEND=Agg
     ```
   - Volumes:
     - `/app/FUENTES` → `fuentes` (volumen creado anteriormente)
     - `/app/data` → nuevo volumen `backend-data`

3. **Añadir servicio Frontend**
   - Click en **+ Add Service** → **From Source**
   - Repository: URL de tu repositorio Git
   - Branch: `main`
   - Context: `frontend`
   - Dockerfile: `frontend/Dockerfile`
   - Port: `80`
   - Environment Variables:
     ```
     VITE_API_URL=http://backend:8000
     ```

4. **Configurar Networking**
   - Asegurar que frontend puede comunicarse con backend
   - Configurar dominio personalizado (opcional)

### Método 2: Desde Docker Compose

1. **Subir archivos al servidor**
   ```bash
   scp -r final-singularity/ usuario@tu-servidor:/opt/apps/
   ```

2. **Conectar por SSH**
   ```bash
   ssh usuario@tu-servidor
   cd /opt/apps/final-singularity
   ```

3. **Editar docker-compose.yml** (ajustar rutas de volúmenes)
   ```yaml
   volumes:
     - /app/FUENTES:/app/FUENTES  # Verificar que existe
   ```

4. **Desplegar**
   ```bash
   docker-compose up -d --build
   ```

## 🌐 Paso 3: Configurar Dominio y SSL

### En Easypanel UI

1. Ve a tu proyecto → **Settings** → **Domains**
2. Añadir dominio:
   - **Domain**: `catastral.tu-dominio.com`
   - **Service**: Frontend (puerto 80)
   - **SSL**: Activar (Let's Encrypt automático)

### Configuración Manual (Nginx Proxy Manager)

```nginx
server {
    listen 80;
    server_name catastral.tu-dominio.com;

    location / {
        proxy_pass http://localhost:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🧪 Paso 4: Verificar Despliegue

### Health Checks

```bash
# Backend
curl http://tu-servidor:8000/health
# Respuesta esperada: {"status":"healthy"}

# Frontend
curl http://tu-servidor/
# Debe devolver HTML
```

### Logs

```bash
# Ver logs del backend
docker-compose logs -f backend

# Ver logs del frontend
docker-compose logs -f frontend
```

### Probar Funcionalidad

1. Accede a `http://catastral.tu-dominio.com`
2. Sube el archivo de ejemplo `ejemplo_referencias.txt`
3. Observa el progreso en tiempo real
4. Descarga el ZIP de resultados

## 🔍 Troubleshooting

### Error: "Volumen FUENTES no encontrado"

**Solución:**
```bash
# Verificar que el volumen existe
docker volume ls

# Si no existe, crearlo manualmente
docker volume create fuentes
```

### Error: "Cannot connect to backend"

**Solución:**
1. Verificar que backend está corriendo:
   ```bash
   docker-compose ps
   ```

2. Verificar networking:
   ```bash
   docker network ls
   docker network inspect final-singularity_default
   ```

3. En frontend, verificar variable de entorno:
   ```bash
   docker-compose exec frontend env | grep API
   ```

### Error: "Permission denied" al escribir en volúmenes

**Solución:**
```bash
# Ajustar permisos
sudo chown -R 1000:1000 /app/FUENTES
sudo chown -R 1000:1000 /app/data
```

### Backend consume mucha memoria

**Solución:**
Añadir límites en `docker-compose.yml`:
```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 4G
        reservations:
          memory: 2G
```

## 📊 Monitoreo

### Estadísticas de Contenedores

```bash
docker stats
```

### Espacio en Disco

```bash
# Ver uso de volúmenes
docker system df -v

# Limpiar imágenes no usadas
docker system prune -a
```

### Logs Persistentes

Configurar log rotation en `/etc/docker/daemon.json`:
```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

## 🔄 Actualizaciones

### Actualizar desde Git

```bash
cd /opt/apps/final-singularity
git pull origin main
docker-compose up -d --build
```

### Actualizar servicios individuales

```bash
# Solo backend
docker-compose up -d --build backend

# Solo frontend
docker-compose up -d --build frontend
```

## 🛡️ Seguridad

### Recomendaciones

1. **Firewall**: Solo exponer puertos 80 y 443
   ```bash
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw enable
   ```

2. **SSL**: Siempre usar HTTPS en producción

3. **CORS**: En `backend/main.py`, cambiar:
   ```python
   allow_origins=["*"]  # ❌ Desarrollo
   # a
   allow_origins=["https://catastral.tu-dominio.com"]  # ✅ Producción
   ```

4. **Rate Limiting**: Añadir en nginx:
   ```nginx
   limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
   ```

## 📈 Backup

### Backup de Volúmenes

```bash
# Backup de FUENTES
docker run --rm -v /app/FUENTES:/data -v $(pwd):/backup ubuntu tar czf /backup/fuentes-backup.tar.gz /data

# Backup de resultados
docker run --rm -v backend-data:/data -v $(pwd):/backup ubuntu tar czf /backup/data-backup.tar.gz /data
```

### Restaurar Backup

```bash
# Restaurar FUENTES
docker run --rm -v /app/FUENTES:/data -v $(pwd):/backup ubuntu tar xzf /backup/fuentes-backup.tar.gz -C /

# Restaurar resultados
docker run --rm -v backend-data:/data -v $(pwd):/backup ubuntu tar xzf /backup/data-backup.tar.gz -C /
```

## 📞 Soporte

Si encuentras problemas:

1. Revisa los logs: `docker-compose logs`
2. Verifica la configuración: `docker-compose config`
3. Consulta la documentación del backend: `http://tu-servidor:8000/docs`

---

✨ **¡Listo!** Tu Pipeline GIS Catastral está desplegado en Easypanel.
