# FASE 1: Construcción del Frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ .
RUN npm run build

# FASE 2: Backend y Servidor Final
FROM python:3.11-slim
WORKDIR /app

# Instalar dependencias del sistema + Nginx
RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    libspatialindex-dev \
    build-essential \
    curl \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias del Backend
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del Backend
COPY backend/ .
RUN mkdir -p /app/data/INPUTS /app/data/OUTPUTS /app/FUENTES

# Copiar el build del Frontend a la carpeta de Nginx
COPY --from=frontend-builder /app/frontend/dist /usr/share/nginx/html

# Configurar Nginx para que haga de proxy local
COPY frontend/nginx.conf /etc/nginx/sites-available/default
# Modificamos el proxy_pass para que apunte localmente (127.0.0.1)
RUN sed -i 's/backend:8000/127.0.0.1:8000/g' /etc/nginx/sites-available/default
RUN ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default

# Crear script de arranque dual
RUN echo '#!/bin/bash\nnginx -g "daemon off;" &\nuvicorn main:app --host 127.0.0.1 --port 8000' > /app/start.sh
RUN chmod +x /app/start.sh

# Exponemos solo el puerto 80 (Nginx servirá todo)
EXPOSE 80

CMD ["/app/start.sh"]
