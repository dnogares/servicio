# 🚀 Despliegue en Easypanel - UN SOLO SERVICIO

## 📝 Configuración Simple con Docker Compose

Este proyecto se despliega como **un solo servicio** en Easypanel usando el archivo `docker-compose.yml`.

---

## ✅ PASO 1: Preparar Volumen FUENTES

Antes de desplegar, necesitas crear y poblar el volumen para los archivos geoespaciales.

### Opción A: Desde la UI de Easypanel

1. Ve a tu proyecto → **Volumes**
2. Click en **+ Add Volume**
3. Configurar:
   ```
   Name: fuentes
   Mount Path: /app/FUENTES
   Size: 5-20 GB (según tus datos)
   ```

### Opción B: Via SSH

```bash
# Conectar al servidor
ssh usuario@tu-servidor.com

# Crear directorio
sudo mkdir -p /app/FUENTES/CAPAS_gpkg/afecciones

# Subir tus archivos GPKG
# Ejemplo: RGVP2024.gpkg, otras capas de afecciones
```

---

## 🚢 PASO 2: Desplegar en Easypanel

### Desde Repositorio Git (Recomendado)

1. **Subir tu código a GitHub/GitLab**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/TU-USUARIO/pipeline-catastral.git
   git push -u origin main
   ```

2. **En Easypanel:**
   - Click en **+ Create**
   - Selecciona **App**
   - Choose **Source** → **Git Repository**
   
3. **Configurar el servicio:**
   ```yaml
   General:
     Name: pipeline-catastral
     
   Source:
     Repository: https://github.com/TU-USUARIO/pipeline-catastral.git
     Branch: main
     
   Build:
     Type: Docker Compose
     Compose File: docker-compose.yml
     
   Networking:
     Port: 80
     Domain: catastral.tudominio.com
     SSL: ✅ Enable (Let's Encrypt)
     
   Volumes:
     - Source: /app/FUENTES
       Target: /app/FUENTES
       (o usar el volumen 'fuentes' si lo creaste en Paso 1)
   ```

4. **Click en Deploy** 🚀

---

## 🔧 PASO 3: Verificar Despliegue

### Check 1: Health Status

Espera 1-2 minutos y verifica que ambos contenedores estén **healthy** (verde) en Easypanel.

### Check 2: URLs

```bash
# Frontend
curl https://catastral.tudominio.com
# Debe devolver HTML

# Backend Health
curl https://catastral.tudominio.com/api/health
# Debe devolver: {"status":"healthy"}

# API Docs
# Abre en navegador: https://catastral.tudominio.com/api/docs
```

### Check 3: Logs

En Easypanel, ve a tu servicio → **Logs** y verifica:

```
✅ backend  | INFO: Application startup complete
✅ frontend | Ready on port 80
```

---

## 🧪 PASO 4: Probar la Aplicación

1. Abre tu app: `https://catastral.tudominio.com`
2. Sube el archivo `ejemplo_referencias.txt` (incluido en el proyecto)
3. Observa el progreso en tiempo real
4. Descarga el ZIP con los resultados

---

## 📊 Estructura en Easypanel

Cuando despliegas con docker-compose, Easypanel crea:

```
TU SERVICIO (pipeline-catastral)
│
├── 🐳 Container: catastral-backend (puerto interno 8000)
│   ├── Healthcheck: /health
│   ├── Volume: /app/FUENTES → Tus archivos GPKG
│   └── Volume: /app/data → Datos generados
│
└── 🐳 Container: catastral-frontend (puerto 80 → externo)
    ├── Healthcheck: /
    ├── Nginx sirve React app
    └── Proxy: /api/* → backend:8000
```

---

## 🔀 Alternativa: Despliegue Manual

Si prefieres desplegar manualmente:

```bash
# 1. Conectar al servidor
ssh usuario@tu-servidor.com

# 2. Clonar o subir el proyecto
cd /opt/apps
git clone https://github.com/TU-USUARIO/pipeline-catastral.git
cd pipeline-catastral

# 3. Asegurar que /app/FUENTES existe y tiene datos
ls -la /app/FUENTES/CAPAS_gpkg/afecciones

# 4. Desplegar
docker-compose up -d --build

# 5. Ver logs
docker-compose logs -f

# 6. Ver estado
docker-compose ps
```

---

## ⚙️ Variables de Entorno (Opcional)

Puedes personalizar el despliegue creando un archivo `.env`:

```bash
# Puerto externo (por defecto 80)
PORT=8080

# Ruta personalizada a FUENTES
FUENTES_PATH=/mi/ruta/custom/FUENTES
```

---

## 🔄 Actualizar la Aplicación

### Desde Easypanel:

1. Push cambios a Git
2. En Easypanel → Tu servicio → **Redeploy**
3. Easypanel automáticamente hace pull y rebuild

### Manualmente:

```bash
ssh usuario@tu-servidor.com
cd pipeline-catastral
git pull
docker-compose up -d --build
```

---

## 🛑 Detener/Reiniciar

```bash
# Detener
docker-compose down

# Reiniciar
docker-compose restart

# Ver estado
docker-compose ps

# Logs en vivo
docker-compose logs -f
```

---

## 🧹 Limpieza

```bash
# Detener y limpiar contenedores
docker-compose down

# Limpiar volúmenes también (⚠️ CUIDADO: borra datos!)
docker-compose down -v

# Limpiar imágenes antiguas
docker system prune -f
```

---

## 🔍 Troubleshooting

### ❌ Error: "Network catastral-network not found"

**Solución:**
```bash
docker-compose down
docker-compose up -d --build
```

### ❌ Frontend no puede comunicarse con Backend

**Verificar:**
1. Ambos contenedores en la misma red:
   ```bash
   docker network inspect pipeline-catastral_catastral-network
   ```

2. Backend está healthy:
   ```bash
   docker-compose ps
   ```

3. Nginx config correcto:
   ```bash
   docker-compose exec frontend cat /etc/nginx/conf.d/default.conf | grep proxy_pass
   # Debe mostrar: proxy_pass http://backend:8000/;
   ```

### ❌ "Permission denied" en volúmenes

**Solución:**
```bash
sudo chown -R 1000:1000 /app/FUENTES
sudo chown -R 1000:1000 /app/data
```

### ❌ Puerto 80 ya está en uso

**Solución 1:** Cambiar puerto en `.env`:
```bash
echo "PORT=8080" > .env
docker-compose up -d
```

**Solución 2:** Detener servicio conflictivo:
```bash
sudo lsof -i :80
sudo systemctl stop nginx  # o el servicio que use el puerto
```

---

## 📈 Monitoreo

### Recursos

```bash
# CPU y RAM en tiempo real
docker stats

# Espacio en disco
docker system df -v
```

### Logs

```bash
# Todos los servicios
docker-compose logs -f

# Solo backend
docker-compose logs -f backend

# Solo frontend
docker-compose logs -f frontend

# Últimas 100 líneas
docker-compose logs --tail=100
```

---

## 🎯 URLs Finales

Después del despliegue exitoso:

| Servicio | URL |
|----------|-----|
| **App Principal** | https://catastral.tudominio.com |
| **Subir Archivos** | https://catastral.tudominio.com |
| **API Swagger** | https://catastral.tudominio.com/api/docs |
| **Health Check** | https://catastral.tudominio.com/api/health |

---

## ✅ Checklist Final

- [ ] Volumen `/app/FUENTES` creado y con archivos GPKG
- [ ] Código en repositorio Git (o subido al servidor)
- [ ] Servicio creado en Easypanel
- [ ] Dominio configurado con SSL
- [ ] Health checks pasando (verde en Easypanel)
- [ ] Frontend accesible en navegador
- [ ] API docs accesible en `/api/docs`
- [ ] Probado con `ejemplo_referencias.txt`
- [ ] ZIP de resultados descarga correctamente

---

🎉 **¡Listo!** Tu Pipeline GIS Catastral está corriendo como un solo servicio en Easypanel.
