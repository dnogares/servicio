# 📐 Convenciones de Código y Estándares del Equipo

## 🎯 Objetivo

Mantener un código limpio, consistente y mantenible para todo el equipo.

---

## 🐍 Python (Backend)

### Estilo General
- **PEP 8** como guía principal
- **Black** como formateador (configurado en workspace)
- Máximo **88 caracteres** por línea (Black default)

### Nombres

```python
# Variables y funciones: snake_case
usuario_activo = True
def procesar_archivo(archivo_path):
    pass

# Clases: PascalCase
class OrquestadorPipeline:
    pass

# Constantes: UPPER_SNAKE_CASE
MAX_REFERENCIAS = 100
API_URL = "https://api.example.com"

# Archivos: snake_case.py
# orquestador.py
# catastro_engine.py
```

### Imports

```python
# 1. Standard library
import os
import sys
from pathlib import Path

# 2. Third party
import pandas as pd
import geopandas as gpd
from fastapi import FastAPI

# 3. Local/application
from logic.orquestador import OrquestadorPipeline
```

### Docstrings

```python
def procesar_referencias(referencias: list[str]) -> dict:
    """
    Procesa una lista de referencias catastrales.
    
    Args:
        referencias: Lista de referencias catastrales (formato: 9872023VG1697S0001WR)
        
    Returns:
        dict: Diccionario con resultados del procesamiento
        
    Raises:
        ValueError: Si alguna referencia no es válida
        
    Example:
        >>> procesar_referencias(["9872023VG1697S0001WR"])
        {"status": "ok", "procesadas": 1}
    """
    pass
```

### Type Hints

```python
# Siempre usar type hints
def calcular_area(ancho: float, alto: float) -> float:
    return ancho * alto

# Para tipos complejos
from typing import Optional, List, Dict

def buscar_parcela(ref: str) -> Optional[Dict[str, Any]]:
    pass
```

---

## ⚛️ TypeScript/React (Frontend)

### Estilo General
- **Prettier** como formateador (configurado en workspace)
- **ESLint** para linting

### Nombres

```typescript
// Variables y funciones: camelCase
const archivoSeleccionado = file;
const handleFileUpload = () => {};

// Componentes React: PascalCase
function App() {}
function FileUploader() {}

// Interfaces y Types: PascalCase con prefijo 'I' opcional
interface ProcesoStatus {
    procesoId: string;
    estado: 'procesando' | 'completado' | 'error';
}

// Constantes: UPPER_SNAKE_CASE
const API_URL = import.meta.env.VITE_API_URL;
const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB

// Archivos componentes: PascalCase.tsx
// App.tsx
// FileUploader.tsx

// Archivos utilidades: camelCase.ts
// apiClient.ts
// formatters.ts
```

### Componentes React

```typescript
// Componente funcional con TypeScript
interface ButtonProps {
    label: string;
    onClick: () => void;
    disabled?: boolean;
}

export function Button({ label, onClick, disabled = false }: ButtonProps) {
    return (
        <button onClick={onClick} disabled={disabled}>
            {label}
        </button>
    );
}
```

### Hooks

```typescript
// Custom hooks: usar prefijo 'use'
function useFileUpload() {
    const [uploading, setUploading] = useState(false);
    
    const upload = async (file: File) => {
        setUploading(true);
        // ...
        setUploading(false);
    };
    
    return { uploading, upload };
}
```

---

## 📁 Estructura de Archivos

### Backend

```
backend/
├── logic/
│   ├── __init__.py
│   ├── orquestador.py       ← Lógica principal del pipeline
│   ├── catastro_client.py   ← Cliente para APIs de Catastro
│   └── utils.py             ← Utilidades generales
├── models/
│   ├── __init__.py
│   └── schemas.py           ← Modelos Pydantic
├── main.py                  ← Endpoints FastAPI
└── requirements.txt
```

### Frontend

```
frontend/src/
├── components/
│   ├── FileUploader.tsx
│   ├── ProgressBar.tsx
│   └── LogsViewer.tsx
├── hooks/
│   ├── useFileUpload.ts
│   └── useProcessStatus.ts
├── utils/
│   ├── apiClient.ts
│   └── formatters.ts
├── App.tsx
└── main.tsx
```

---

## 💬 Mensajes de Commit

Seguir **Conventional Commits**:

```
tipo(scope): descripción corta

[cuerpo opcional]

[footer opcional]
```

### Tipos

- `feat`: Nueva funcionalidad
- `fix`: Corrección de bug
- `docs`: Cambios en documentación
- `style`: Formato, punto y coma, etc (no afecta código)
- `refactor`: Refactorización (no añade funcionalidad ni corrige bug)
- `test`: Añadir tests
- `chore`: Tareas de mantenimiento

### Ejemplos

```bash
# Feature
git commit -m "feat(backend): añadir endpoint para descargar ZIP"

# Fix
git commit -m "fix(frontend): corregir error al subir archivo grande"

# Docs
git commit -m "docs: actualizar README con instrucciones de Docker"

# Refactor
git commit -m "refactor(backend): mejorar estructura del orquestador"

# Con cuerpo
git commit -m "feat(frontend): añadir indicador de progreso

- Añadido componente ProgressBar
- Integrado con polling de status
- Animación suave"
```

---

## 🌿 Git Workflow

### Ramas

```
main              ← Producción (protegida)
├── develop       ← Desarrollo (opcional)
├── feature/xxx   ← Nuevas funcionalidades
├── fix/xxx       ← Correcciones
└── hotfix/xxx    ← Correcciones urgentes
```

### Flujo

1. **Crear rama desde main**:
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature/nombre-descriptivo
   ```

2. **Desarrollar y commitear frecuentemente**:
   ```bash
   git add .
   git commit -m "feat: descripción"
   ```

3. **Push y crear PR**:
   ```bash
   git push origin feature/nombre-descriptivo
   # Crear Pull Request en GitHub
   ```

4. **Review → Merge → Borrar rama**

---

## 🧪 Testing

### Backend

```python
# Usar pytest
# archivo: tests/test_orquestador.py

def test_procesar_referencia_valida():
    """Test que una referencia válida se procesa correctamente."""
    ref = "9872023VG1697S0001WR"
    resultado = procesar_referencia(ref)
    assert resultado["status"] == "ok"

def test_procesar_referencia_invalida():
    """Test que una referencia inválida lanza error."""
    with pytest.raises(ValueError):
        procesar_referencia("referencia-invalida")
```

### Frontend

```typescript
// Usar Vitest (cuando se implemente)
// archivo: src/components/Button.test.tsx

describe('Button', () => {
    it('should render with label', () => {
        render(<Button label="Click me" onClick={() => {}} />);
        expect(screen.getByText('Click me')).toBeInTheDocument();
    });
});
```

---

## 📝 Comentarios

### Cuándo Comentar

✅ **SÍ comentar**:
- Algoritmos complejos
- Workarounds temporales
- TODOs
- Explicar el "por qué", no el "qué"

```python
# ✅ BIEN
# Usamos timeout de 60s porque la API de Catastro puede ser lenta
respuesta = requests.get(url, timeout=60)

# TODO: Cachear resultados para evitar llamadas redundantes
```

❌ **NO comentar**:
- Cosas obvias
- Código comentado (bórralo)

```python
# ❌ MAL
# Asignar usuario a variable
usuario = get_usuario()

# ❌ MAL (código comentado)
# def funcion_vieja():
#     pass
```

---

## 🎨 CSS/Styling

### Frontend

- Usar **CSS Modules** o **App.css** para estilos globales
- Variables CSS para colores y valores reutilizables
- Mobile-first design

```css
/* Variables en :root */
:root {
  --primary: hsl(210, 100%, 50%);
  --bg-primary: hsl(220, 20%, 10%);
}

/* Clases descriptivas */
.upload-section {
  padding: 2rem;
}

/* Mobile first */
.container {
  width: 100%;
}

@media (min-width: 768px) {
  .container {
    max-width: 1200px;
  }
}
```

---

## 🔒 Seguridad

### NO commitear

- ❌ Contraseñas
- ❌ API Keys
- ❌ Tokens
- ❌ Certificados

### SÍ usar

- ✅ Variables de entorno (`.env`)
- ✅ `.gitignore` actualizado
- ✅ Secrets manager en producción

```python
# ❌ MAL
API_KEY = "sk_12345abcde"

# ✅ BIEN
import os
API_KEY = os.getenv("API_KEY")
```

---

## 📚 Documentación

### README de cada módulo

Cada carpeta importante debe tener un README:

```markdown
# Módulo de Orquestación

## Propósito
Coordina el pipeline de procesamiento de referencias catastrales.

## Uso
...

## API
...
```

---

## ✅ Checklist Pre-Commit

Antes de hacer commit, verifica:

- [ ] Código formateado (Black/Prettier)
- [ ] Sin errores de linting
- [ ] Type hints añadidos (Python)
- [ ] Tests pasan (si existen)
- [ ] Comentarios necesarios añadidos
- [ ] Código innecesario eliminado
- [ ] Variables de entorno protegidas
- [ ] Mensaje de commit descriptivo

---

## 📞 Dudas

Si algo no está claro, pregunta al equipo antes de proceder de forma incorrecta.

**Recuerda**: Código limpio hoy = menos bugs mañana 🚀
