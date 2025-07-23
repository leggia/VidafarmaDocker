# Guía de Desarrollo - Vidafarma_IA

## Requisitos Previos

- Docker y Docker Compose instalados
- Git para control de versiones
- Editor de código (VS Code recomendado)

## Levantar el Proyecto

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd agente-ia
```

### 2. Levantar servicios con Docker Compose
```bash
docker-compose up --build
```

Esto levantará:
- **Backend API:** http://localhost:8000
- **Frontend PWA:** http://localhost:3000
- **Documentación API:** http://localhost:8000/docs (Swagger UI)

### 3. Verificar que todo funciona
- Backend: http://localhost:8000/health
- Frontend: http://localhost:3000

## Desarrollo

### Backend (FastAPI)

#### Estructura de archivos
```
backend/api/
├── app/
│   ├── main.py          # Punto de entrada
│   ├── api/             # Endpoints organizados por recurso
│   ├── models/          # Modelos de datos
│   ├── crud/            # Lógica CRUD
│   └── schemas/         # Esquemas Pydantic
├── Dockerfile
└── requirements.txt
```

#### Agregar un nuevo endpoint
1. Crear archivo en `app/api/nuevo_recurso.py`
2. Definir modelos en `app/models/` y esquemas en `app/schemas/`
3. Agregar lógica CRUD en `app/crud/`
4. Importar y registrar en `main.py`

#### Ejemplo de endpoint
```python
from fastapi import APIRouter
from app.schemas.nuevo_recurso import NuevoRecurso

router = APIRouter()

@router.get("/nuevo-recurso")
def get_nuevo_recurso():
    return {"mensaje": "Nuevo recurso"}

@router.post("/nuevo-recurso")
def crear_nuevo_recurso(recurso: NuevoRecurso):
    return {"mensaje": "Creado", "datos": recurso}
```

### Frontend (React PWA)

#### Estructura de archivos
```
frontend/
├── public/
├── src/
│   ├── components/      # Componentes reutilizables
│   ├── hooks/          # Hooks personalizados
│   ├── services/       # Lógica para APIs
│   ├── App.js
│   └── index.js
├── Dockerfile
└── package.json
```

#### Agregar un nuevo componente
1. Crear archivo en `src/components/NuevoComponente.js`
2. Importar y usar en `App.js` o en otros componentes

#### Ejemplo de componente
```jsx
import React from 'react';

function NuevoComponente({ titulo }) {
  return (
    <div>
      <h2>{titulo}</h2>
      {/* Contenido del componente */}
    </div>
  );
}

export default NuevoComponente;
```

### Funcionalidad de Voz

#### Web Speech API
El frontend usa la Web Speech API para:
- **Reconocimiento de voz:** Convertir voz a texto
- **Síntesis de voz:** Leer respuestas en voz alta

#### Uso en componentes
```jsx
// Reconocimiento de voz
const startListening = () => {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const recognition = new SpeechRecognition();
  recognition.lang = 'es-ES';
  // ... configuración
};

// Síntesis de voz
const speak = (texto) => {
  const utterance = new SpeechSynthesisUtterance(texto);
  utterance.lang = 'es-ES';
  speechSynthesis.speak(utterance);
};
```

## Testing

### Backend
```bash
# Ejecutar tests (cuando se implementen)
cd backend/api
python -m pytest
```

### Frontend
```bash
# Ejecutar tests (cuando se implementen)
cd frontend
npm test
```

## Debugging

### Backend
- Logs en consola de Docker: `docker-compose logs api`
- Swagger UI: http://localhost:8000/docs
- Rebuild: `docker-compose up --build api`

### Frontend
- Logs en consola del navegador (F12)
- Hot reload automático en desarrollo
- Rebuild: `docker-compose up --build frontend`

## Comandos Útiles

```bash
# Levantar solo un servicio
docker-compose up api

# Ver logs en tiempo real
docker-compose logs -f

# Parar todos los servicios
docker-compose down

# Rebuild y levantar
docker-compose up --build

# Ejecutar comandos dentro de un contenedor
docker-compose exec api python -c "print('Hola')"
```

## Estructura de Commits

Usar commits descriptivos:
```
feat: agregar endpoint para consultas de IA
fix: corregir error en reconocimiento de voz
docs: actualizar README del backend
refactor: reorganizar estructura de componentes
```

## Próximos Pasos

1. **Base de datos:** Configurar PostgreSQL/MySQL
2. **Autenticación:** Implementar JWT o OAuth
3. **OCR:** Integrar Tesseract
4. **Odoo:** Conectar con API de Odoo
5. **IA:** Implementar lógica de IA para consultas
6. **Testing:** Agregar tests unitarios e integración
7. **CI/CD:** Configurar pipeline de despliegue

---

*Actualiza esta guía conforme evolucione el proyecto.* 