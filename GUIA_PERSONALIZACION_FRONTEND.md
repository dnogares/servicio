# 🎨 GUÍA RÁPIDA DE PERSONALIZACIÓN

## 📝 Cambios Comunes en App.tsx

### 1. Cambiar Título y Subtítulo (líneas 141-142)

```tsx
<h1 className="title">GIS Tecnología Alcalá</h1>
<p className="subtitle">Tu descripción personalizada aquí</p>
```

### 2. Cambiar Texto del Botón Procesar (línea 208)

```tsx
{cargando ? '⏳ Procesando...' : '🚀 TU TEXTO AQUÍ'}
```

### 3. Cambiar Estadísticas (líneas 218-228)

```tsx
<div className="info-item">
  <span className="info-number">25</span> {/* Cambia el número */}
  <span className="info-label">Tu Texto</span>
</div>
```

### 4. Cambiar Lista de Fases (líneas 234-239)

```tsx
<li>🔍 Tu fase personalizada 1</li>
<li>🗺️ Tu fase personalizada 2</li>
```

### 5. Cambiar Footer (línea 318)

```tsx
<p>Tecnología Alcalá © 2026 | Mi madre pensará que lo ha hecho otro</p>
```

---

## 🎨 Cambios de Colores en App.css

### Ubicación: `frontend/src/App.css` (líneas ~10-20)

```css
:root {
  /* Color principal (azul por defecto) */
  --primary: hsl(210, 100%, 50%);     /* Cambia el primer número para otro color */
                                       /* 0=rojo, 120=verde, 210=azul, 280=violeta */
  
  /* Fondos oscuros */
  --bg-primary: hsl(220, 20%, 10%);   /* Fondo principal */
  --bg-secondary: hsl(220, 20%, 15%); /* Fondo de tarjetas */
  
  /* Tema claro: cambia a valores altos */
  --bg-primary: hsl(0, 0%, 95%);      /* Fondo claro */
  --text-primary: hsl(0, 0%, 10%);    /* Texto oscuro */
}
```

---

## 🖼️ Añadir Logo Personalizado

### 1. Crear carpeta public (si no existe)

```bash
mkdir frontend/public
```

### 2. Copiar tu logo ahí

```
frontend/public/logo.png
frontend/public/favicon.ico
```

### 3. Usar en App.tsx (línea 139)

```tsx
<div className="logo-icon">
  <img src="/logo.png" alt="Logo" className="logo-image" />
</div>
```

### 4. Añadir estilos en App.css

```css
.logo-image {
  width: 50px;
  height: 50px;
  object-fit: contain;
}
```

### 5. Cambiar favicon en index.html (línea 5)

```html
<link rel="icon" type="image/png" href="/favicon.ico" />
```

---

## 🔄 Aplicar Cambios

Los cambios se ven **automáticamente** con Vite en desarrollo:

1. Guarda el archivo
2. El navegador se recarga automáticamente
3. Ves los cambios al instante

---

## 📦 Archivos Importantes

```
frontend/
├── src/
│   ├── App.tsx       ← TEXTOS, ESTRUCTURA, LÓGICA
│   ├── App.css       ← ESTILOS, COLORES
│   ├── main.tsx      (no tocar)
│   └── index.css     ← Estilos globales
├── index.html        ← TÍTULO PESTAÑA, META TAGS
└── public/           ← IMÁGENES, LOGOS, FAVICON
    ├── logo.png
    └── favicon.ico
```

---

## ⚡ Cambios Rápidos Más Comunes

| Quiero cambiar | Archivo | Línea aprox. | Buscar |
|----------------|---------|--------------|--------|
| Título principal | App.tsx | 141 | `<h1 className="title">` |
| Color principal | App.css | 12 | `--primary:` |
| Texto botón | App.tsx | 208 | `🚀 Procesar` |
| Footer | App.tsx | 318 | `<footer` |
| Logo | App.tsx | 139 | `<div className="logo-icon">` |
| Título pestaña | index.html | 8 | `<title>` |
| Favicon | index.html | 5 | `<link rel="icon"` |

---

## 🎯 Ejemplo Completo de Cambio de Marca

Si quieres cambiar el nombre completo de "Pipeline GIS Catastral" a "Tu App":

1. **App.tsx línea 141**: `<h1>Tu App</h1>`
2. **App.tsx línea 318**: `Tu App © 2026`
3. **index.html línea 7**: description="Tu App descripción"
4. **index.html línea 8**: `<title>Tu App</title>`
5. **public/logo.png**: Tu logo
6. **App.css**: Cambiar colores principales

¡Y listo! 🎉
