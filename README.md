# Pipeline GIS Catastral

> 🗺️ **Procesamiento automatizado de referencias catastrales** - Sistema completo de 19 pasos para generación de cartografía, análisis espacial y documentación catastral.

## 🌟 Características

### 📊 Pipeline Completo de 19 Pasos

#### **Fase 1: Adquisición de Datos** (Pasos 1-3)
- 📥 Lectura de referencias catastrales desde archivos `.txt`
- 🌐 Descarga de XML INSPIRE desde Catastro
- 📄 Descarga de PDF (Croquis y Datos Gráficos)

#### **Fase 2: Generación Vectorial** (Pasos 4-5)
- 🗺️ Generación de archivos KML (individuales + maestro)
- 🖼️ Generación de siluetas PNG

#### **Fase 3: Exportación Tabular** (Paso 6)
- 📊 Creación de tablas Excel y CSV con datos catastrales
- 📐 Superficie, coordenadas, polígono, parcela

#### **Fase 4: Documentación** (Paso 7)
- 📝 Generación de log.txt con resumen del expediente

#### **Fase 5: Análisis Espacial** (Paso 8)
- 🔍 Análisis de afecciones con capas GPKG locales
- 📈 Intersecciones, porcentajes, mapas de afecciones

#### **Fases 6-12: Generación de Planos Cartográficos**
- 📍 Planos de emplazamiento (OSM, Ortofoto)
- 🏘️ Plano catastral (WMS Catastro 1000m)
- 🗺️ Planos IGN detallados (2 variantes)
- 🌍 Planos de localización provincial (3 estilos)
- 📜 Planos históricos (MTN25, MTN50, Catastrones)
- ⛰️ Plano de pendientes con leyenda
- 🌿 Plano Red Natura 2000
- 🌲 Plano Montes Públicos (CMUP)
- 🐄 Plano Vías Pecuarias

### 🎨 Interfaz Web Moderna

- ✨ Diseño moderno con glassmorphism y gradientes vibrantes
- 📤 Drag & drop para subir archivos
- ⏱️ Progreso en tiempo real con logs
- 📦 Descarga de resultados en formato ZIP
- 📱 Diseño responsive

## 🚀 Despliegue en Easypanel

### Prerequisitos

1. **Volumen FUENTES**: Crear volumen en Easypanel montado en `/app/FUENTES`
2. **Puerto 80**: Asegurar que el puerto esté disponible

### Instrucciones

1. **Clonar o subir el proyecto** a tu servidor Easypanel

2. **Configurar el volumen** en `docker-compose.yml`:
   ```yaml
   volumes:
     - /app/FUENTES:/app/FUENTES  # Ya configurado
   ```

3. **Construir y desplegar**:
   ```bash
   docker-compose up -d --build
   ```

4. **Acceder a la aplicación**:
   - Frontend: `http://tu-dominio/`
   - Backend API: `http://tu-dominio/api/`
   - Documentación API: `http://tu-dominio/api/docs`

### Estructura de Volúmenes

```
/app/FUENTES/           ← Volumen de Easypanel (datos geoespaciales)
  └── CAPAS_gpkg/
      └── afecciones/
          ├── RGVP2024.gpkg
          └── ... (otras capas)

/app/data/              ← Volumen interno Docker
  ├── INPUTS/
  ├── OUTPUTS/
  └── uploads/
```

## 💻 Desarrollo Local

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Acceder a:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 📁 Estructura del Proyecto

```
final-singularity/
├── backend/
│   ├── logic/
│   │   └── orquestador.py      # Pipeline principal
│   ├── main.py                  # API FastAPI
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.tsx              # Componente principal
│   │   ├── App.css              # Estilos
│   │   └── main.tsx
│   ├── package.json
│   ├── Dockerfile
│   └── nginx.conf
├── docker-compose.yml
└── README.md
```

## 🔌 API Endpoints

### `POST /upload`
Sube un archivo `.txt` con referencias catastrales e inicia el procesamiento.

**Request:**
```bash
curl -X POST -F "file=@referencias.txt" http://localhost:8000/upload
```

**Response:**
```json
{
  "proceso_id": "uuid-del-proceso",
  "mensaje": "Procesamiento iniciado",
  "archivo": "referencias.txt"
}
```

### `GET /status/{proceso_id}`
Consulta el estado de un proceso.

**Response:**
```json
{
  "proceso_id": "uuid",
  "estado": "procesando",
  "progreso": 45,
  "mensaje": "FASE 5: ANÁLISIS ESPACIAL",
  "carpeta_resultado": null
}
```

### `GET /logs/{proceso_id}`
Obtiene los logs completos de un proceso.

### `GET /download/{proceso_id}`
Descarga los resultados como archivo ZIP.

### `DELETE /proceso/{proceso_id}`
Elimina un proceso y sus archivos.

### `GET /procesos`
Lista todos los procesos activos.

## 📊 Outputs Generados

Cada procesamiento genera una carpeta con timestamp:

```
OUTPUTS/
└── referencias-20260209-141530/
    ├── [RC]_INSPIRE.xml
    ├── [RC]_CDyG.pdf
    ├── [RC].kml
    ├── [RC]_silueta.png
    ├── MAPA_MAESTRO_TOTAL.kml
    ├── CONJUNTO_TOTAL.png
    ├── DATOS_CATASTRALES.xlsx
    ├── DATOS_CATASTRALES.csv
    ├── log.txt
    ├── afecciones_resultados.xlsx
    ├── PLANO-EMPLAZAMIENTO.jpg
    ├── PLANO-EMPLAZAMIENTO-ORTO.jpg
    ├── PLANO-CATASTRAL-map.jpg
    ├── PLANO-IGN-V1.jpg
    ├── PLANO-IGN-V2.jpg
    ├── PLANO-PROVINCIAL-V1-STREETS.jpg
    ├── PLANO-PROVINCIAL-V1-TOPO.jpg
    ├── PLANO-PROVINCIAL-V1-OSM.jpg
    ├── PLANO-MTN25.jpg
    ├── PLANO-MTN50.jpg
    ├── PLANO-CATASTRONES.jpg
    ├── PLANO-PENDIENTES-LEYENDA.jpg
    ├── PLANO-NATURA-2000.jpg
    ├── PLANO-MONTES-PUBLICOS.jpg
    └── PLANO-VIAS-PECUARIAS.jpg
```

## 🛠️ Tecnologías

**Backend:**
- FastAPI
- Geopandas
- Matplotlib
- Contextily
- Pandas

**Frontend:**
- React 18
- TypeScript
- Vite
- Axios

**Infraestructura:**
- Docker
- Nginx

## 📝 Licencia

MIT

## 👨‍💻 Autor

Pipeline GIS Catastral v1.0
