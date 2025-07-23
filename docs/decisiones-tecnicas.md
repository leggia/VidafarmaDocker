# Decisiones Técnicas - Vidafarma_IA

## Arquitectura General

### Monorepo
- **Decisión:** Usar estructura de monorepo para facilitar el desarrollo y mantenimiento.
- **Justificación:** Permite compartir código, configuraciones y documentación entre microservicios.
- **Alternativas consideradas:** Repositorios separados (más complejo para desarrollo inicial).

### Microservicios
- **Decisión:** Arquitectura de microservicios para escalabilidad y mantenibilidad.
- **Justificación:** Permite escalar servicios independientemente (OCR, IA, Odoo).
- **Alternativas consideradas:** Monolito (menos flexible para futuras integraciones).

## Backend

### FastAPI
- **Decisión:** FastAPI como framework principal para el microservicio API.
- **Justificación:** 
  - Rendimiento alto (basado en Starlette y Pydantic).
  - Documentación automática (Swagger/OpenAPI).
  - Soporte nativo para async/await.
  - Validación automática con Pydantic.
- **Alternativas consideradas:** Django (más pesado), Flask (menos funcionalidades).

### Python 3.11
- **Decisión:** Python 3.11 como versión base.
- **Justificación:** Balance entre estabilidad y características modernas.
- **Alternativas consideradas:** Python 3.12 (más nuevo, menos estable).

## Frontend

### React
- **Decisión:** React para el frontend PWA.
- **Justificación:** 
  - Ecosistema maduro y amplio.
  - Fácil integración con Web Speech API.
  - Buena documentación y comunidad.
- **Alternativas consideradas:** Vue.js, Svelte (menos maduros para PWA).

### Web Speech API
- **Decisión:** Usar Web Speech API nativa para reconocimiento y síntesis de voz.
- **Justificación:** 
  - Sin dependencias externas.
  - Gratuito y fácil de implementar.
  - Funciona en la mayoría de navegadores modernos.
- **Alternativas consideradas:** 
  - Whisper (requiere backend, más recursos).
  - APIs cloud (Google Speech, Azure Speech - costo).

## Infraestructura

### Docker
- **Decisión:** Docker para containerización de todos los servicios.
- **Justificación:** 
  - Consistencia entre entornos de desarrollo y producción.
  - Fácil despliegue y escalabilidad.
  - Aislamiento de dependencias.
- **Alternativas consideradas:** Virtualización tradicional (más compleja).

### Docker Compose
- **Decisión:** Docker Compose para orquestación local.
- **Justificación:** 
  - Fácil configuración para desarrollo.
  - Permite definir dependencias entre servicios.
- **Alternativas consideradas:** Kubernetes (overkill para desarrollo inicial).

## Base de Datos

### Pendiente de decisión
- **Opciones consideradas:** PostgreSQL, MySQL, SQLite (desarrollo).
- **Criterios:** Compatibilidad con Odoo, rendimiento, facilidad de uso.

## Integración con Odoo

### API REST/XML-RPC
- **Decisión:** Usar APIs nativas de Odoo para integración.
- **Justificación:** 
  - Método oficial y documentado.
  - Permite sincronización bidireccional.
- **Alternativas consideradas:** Webhooks, integración directa a base de datos.

## OCR

### Tesseract (futuro)
- **Decisión:** Tesseract como solución OCR local inicial.
- **Justificación:** 
  - Open source y gratuito.
  - Funciona bien para texto simple.
  - Puede ejecutarse localmente.
- **Alternativas consideradas:** 
  - Google Vision API (mejor precisión, costo).
  - Azure Computer Vision (similar a Google).

## IA

### Pendiente de decisión
- **Opciones consideradas:** 
  - Modelos locales ligeros (para consultas simples).
  - APIs cloud (OpenAI, Google AI) para consultas complejas.
- **Criterios:** Costo, precisión, latencia, privacidad.

## Seguridad

### CORS
- **Decisión:** Configurar CORS apropiadamente para desarrollo.
- **Justificación:** Permite comunicación segura entre frontend y backend.

### Autenticación
- **Pendiente:** Definir estrategia de autenticación (JWT, OAuth, etc.).

## Monitoreo y Logging

### Pendiente de decisión
- **Opciones consideradas:** 
  - Logging básico con Python logging.
  - Integración con servicios de monitoreo (Prometheus, Grafana).

## Documentación

### README.md en cada servicio
- **Decisión:** Documentación clara en cada microservicio y componente.
- **Justificación:** Facilita onboarding y mantenimiento.

### Markdown
- **Decisión:** Usar Markdown para toda la documentación.
- **Justificación:** Fácil de leer, escribir y versionar en GitHub.

---

*Este documento debe actualizarse con cada decisión técnica importante del proyecto.* 