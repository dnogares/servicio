# 🎯 DESPLIEGUE RÁPIDO EN EASYPANEL

## ✅ Repositorio Git
- **URL**: https://github.com/dnogares/servicio.git
- **Branch**: main
- **Estado**: ✅ Código subido y listo

---

## 🚀 PASOS PARA DESPLEGAR

### 1️⃣ Preparar Volumen FUENTES

**Antes de desplegar**, asegúrate de tener tus archivos GPKG:

```bash
# Conectar al servidor de Easypanel
ssh usuario@tu-servidor.com

# Crear directorio
sudo mkdir -p /app/FUENTES/CAPAS_gpkg/afecciones

# Subir archivos GPKG (ejemplo: RGVP2024.gpkg)
# Via SFTP, SCP o directamente
```

---

### 2️⃣ Desplegar en Easypanel

1. **Ir a Easypanel** → **+ Create** → **App**

2. **Configurar Source**:
   - Type: **Git Repository**
   - Repository: `https://github.com/dnogares/servicio.git`
   - Branch: `main`
   - Auto Deploy: ✅ (opcional)

3. **Configurar Build**:
   - Type: **Docker Compose**
   - Compose File: `docker-compose.yml`

4. **Configurar Port & Domain**:
   - Port: `80`
   - Domain: `catastral.tudominio.com`
   - SSL: ✅ Enable

5. **Configurar Volumes**:
   - Add Volume:
     ```
     Host Path: /app/FUENTES
     Container Path: /app/FUENTES
     ```

6. **Click en DEPLOY** 🚀

---

### 3️⃣ Verificar Despliegue (1-2 minutos)

```bash
# Health Check Backend
curl https://catastral.tudominio.com/api/health
# Respuesta: {"status":"healthy"}

# Frontend
curl https://catastral.tudominio.com
# Respuesta: HTML de la app
```

---

## 📊 URLs de la Aplicación

| Servicio | URL |
|----------|-----|
| **App Principal** | https://catastral.tudominio.com |
| **API Docs** | https://catastral.tudominio.com/api/docs |
| **Health Check** | https://catastral.tudominio.com/api/health |

---

## 🧪 Probar la App

1. Abre `https://catastral.tudominio.com`
2. Arrastra y suelta `ejemplo_referencias.txt`
3. Observa el progreso en tiempo real
4. Descarga el ZIP con todos los resultados

---

## 🔄 Actualizar la App

Cada vez que hagas cambios:

```bash
git add .
git commit -m "Descripción de los cambios"
git push origin main
```

Si configuraste **Auto Deploy**, Easypanel automáticamente:
- ✅ Detecta el push
- ✅ Hace pull del nuevo código
- ✅ Reconstruye las imágenes
- ✅ Redespliega la aplicación

**Sin Auto Deploy**: Ir a Easypanel → Tu App → **Redeploy**

---

## 📦 Estructura de Archivos Generados

Cada procesamiento crea una carpeta con timestamp en `/app/data/OUTPUTS/`:

```
referencias-20260209-141530/
├── [RC]_INSPIRE.xml              ← Datos XML de Catastro
├── [RC]_CDyG.pdf                 ← PDF Croquis
├── [RC].kml                      ← KML individual
├── [RC]_silueta.png              ← Silueta PNG
├── MAPA_MAESTRO_TOTAL.kml        ← KML maestro
├── CONJUNTO_TOTAL.png            ← Todas las siluetas
├── DATOS_CATASTRALES.xlsx        ← Tabla Excel
├── DATOS_CATASTRALES.csv         ← Tabla CSV
├── log.txt                       ← Resumen del expediente
├── afecciones_resultados.xlsx    ← Análisis de afecciones
├── PLANO-EMPLAZAMIENTO.jpg       ← 12 planos cartográficos
└── ... (más planos)
```

---

## 🛠️ Troubleshooting

### ❌ Error: "No module named 'logic'"

**Causa**: Falta el archivo `__init__.py` en `backend/logic/`

**Solución**: Ya está incluido en el repo, verifica que se descargó correctamente.

---

### ❌ Error: "Cannot connect to backend"

**Verificar**:
1. Ambos contenedores están running:
   ```bash
   docker ps
   ```

2. Logs del backend:
   ```bash
   docker logs catastral-backend
   ```

3. Red interna:
   ```bash
   docker network inspect servicio_catastral-network
   ```

---

### ❌ Error: "Permission denied" en `/app/FUENTES`

**Solución**:
```bash
sudo chown -R 1000:1000 /app/FUENTES
sudo chmod -R 755 /app/FUENTES
```

---

## 📞 Soporte

- **Repositorio**: https://github.com/dnogares/servicio
- **Issues**: https://github.com/dnogares/servicio/issues
- **Documentación**: Ver `README.md` en el repo

---

## ✅ Checklist Final

- [ ] Repositorio clonado/accesible
- [ ] Volumen `/app/FUENTES` creado con archivos GPKG
- [ ] Servicio creado en Easypanel
- [ ] Domain configurado con SSL
- [ ] Health checks pasando (verde)
- [ ] Frontend carga correctamente
- [ ] API Docs accesible
- [ ] Probado con archivo de ejemplo
- [ ] Descarga de ZIP funciona

---

🎉 **¡Todo listo!** Tu Pipeline GIS Catastral está desplegado en producción.
