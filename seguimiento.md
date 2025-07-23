# Seguimiento del Proyecto Vidafarma_IA

## Resumen y contexto

Este documento contiene el historial y las decisiones clave tomadas durante la creación del proyecto Vidafarma_IA, para que cualquier colaborador o IA pueda retomar el contexto fácilmente.

---

### 1. Objetivo del proyecto
- Crear una plataforma inteligente para la gestión de una farmacia, con un agente IA capaz de autoaprender y automatizar tareas como compras, inventario, vencimientos, movimientos internos, etc.
- El sistema debe ser escalable, moderno y aprovechar recursos gratuitos de la nube (AWS, Google, HuggingFace, etc.).
- El frontend será una PWA (React) que aproveche cámara y micrófono de los dispositivos móviles.

### 2. Arquitectura y stack
- **Monorepo** con estructura:
  - `/backend` (microservicios: API principal, OCR, integración Odoo, etc.)
  - `/frontend` (PWA en React)
  - `/docs` (documentación adicional)
- **Microservicios** en Python (FastAPI, etc.), cada uno con su Dockerfile.
- **Orquestación** con Docker Compose (y futuro soporte para Kubernetes).
- **Base de datos**: PostgreSQL/MySQL (según necesidades).
- **OCR**: Tesseract local o Google Vision API (free tier).
- **IA**: Modelos ligeros locales y posibilidad de usar servicios cloud.

### 3. Recursos y hardware
- Desarrollo inicial en laptop local (i3, 8GB RAM, 238GB SSD).
- Futuro: migración a hardware con GPU y/o nube.

### 4. Decisiones clave
- Usar Docker para aislar y facilitar el despliegue de cada microservicio.
- Documentar todo en GitHub para facilitar colaboración y onboarding.
- Mantener un archivo de seguimiento del proyecto para no perder contexto al cambiar de carpeta/proyecto en el editor.

### 5. Primeros pasos realizados
- ✅ Creación de la estructura base del monorepo: `backend`, `frontend`, `docs`.
- ✅ Inicialización de la carpeta `frontend` para PWA con React.
- ✅ Planificación de microservicio API principal con FastAPI.

### 6. Progreso actual (ÚLTIMA ACTUALIZACIÓN)
- ✅ **Estructura completa del monorepo creada:**
  - README.md principal con descripción del proyecto
  - .gitignore configurado para Python, Node.js y Docker
  - docker-compose.yml para orquestar servicios
  - Documentación en /docs con decisiones técnicas y guía de desarrollo

- ✅ **Backend API (FastAPI) implementado:**
  - Estructura modular en `/backend/api/app/`
  - Endpoints básicos: health check, consultas de IA, CRUD productos
  - Dockerfile y requirements.txt configurados
  - README.md con documentación del microservicio

- ✅ **Frontend PWA (React) implementado:**
  - Estructura base con package.json y dependencias
  - Componente App.js con funcionalidad de voz (Web Speech API)
  - Estilos CSS modernos y responsive
  - Dockerfile configurado
  - README.md con documentación del frontend

- ✅ **Funcionalidad de voz integrada:**
  - Reconocimiento de voz (voz a texto) en el frontend
  - Endpoint `/api/consulta-ia` en el backend para recibir consultas
  - Interfaz de usuario para consultas por voz o texto
  - Documentación de decisiones técnicas sobre Web Speech API

- ✅ **Documentación completa:**
  - Decisiones técnicas documentadas en `/docs/decisiones-tecnicas.md`
  - Guía de desarrollo en `/docs/guia-desarrollo.md`
  - README.md en cada servicio y en la raíz
  - Estructura preparada para futuros microservicios (OCR, Odoo, IA)

### 7. Siguientes pasos sugeridos
1. **Probar la implementación actual:**
   - Ejecutar `docker-compose up --build` para levantar servicios
   - Verificar que backend (puerto 8000) y frontend (puerto 3000) funcionan
   - Probar funcionalidad de voz en el navegador

2. **Implementar base de datos:**
   - Configurar PostgreSQL/MySQL en docker-compose.yml
   - Crear modelos SQLAlchemy en backend/api
   - Implementar CRUD real para productos

3. **Integrar con Odoo:**
   - Crear microservicio o módulo para conexión con Odoo v18
   - Implementar sincronización de productos e inventario

4. **Implementar OCR:**
   - Crear microservicio OCR con Tesseract
   - Endpoints para procesar facturas (PDF/foto)

5. **Mejorar IA:**
   - Implementar lógica de IA para procesar consultas
   - Conectar con APIs de IA (OpenAI, Google AI, etc.)

---

**Este archivo debe actualizarse con cada avance importante del proyecto.** 