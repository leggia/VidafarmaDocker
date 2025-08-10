# Vidafarma_IA (agente-ia)

Plataforma inteligente para la gestión de farmacias, impulsada por un agente de IA conversacional. Permite la automatización de tareas, consultas de inventario y precios mediante voz, y utiliza la cámara del móvil como un escáner de códigos de barras integrado con Odoo.

## Arquitectura General

- **Monorepo:** Estructura centralizada para facilitar el desarrollo y despliegue.
- **Microservicios:** Cada funcionalidad clave (API, OCR, IA) está aislada en su propio contenedor Docker.
- **Orquestación:** `docker-compose.yml` para gestionar los servicios en desarrollo.
- **Conexión a Odoo:** El sistema se integra con un **servicio externo de Odoo (v18+)** a través de su API XML-RPC, actuando como un cliente inteligente.

---

## Componentes Principales

- **Frontend (`/frontend`):**
  - Una **Progressive Web App (PWA)** construida con React.
  - **Interfaz conversacional:** Permite a los usuarios interactuar con la IA mediante voz y texto.
  - **Escáner de código de barras:** Utiliza la cámara del dispositivo móvil para leer códigos de barras y consultar productos en Odoo.
  - **Soporte offline:** (Futuro) Capacidades básicas sin conexión.

- **Backend (`/backend`):**
  - **API Principal (`/api`):**
    - Construida con **FastAPI**.
    - Gestiona la lógica de negocio y la autenticación.
    - Procesa las intenciones del usuario (ej: "cuál es el precio de X", "actualiza el stock de Y").
    - Se comunica con el servicio externo de Odoo.
  - **Servicio de Odoo (`/api/services/odoo_service.py`):**
    - Cliente XML-RPC para leer y escribir datos en la instancia de Odoo.
    - Cache con **Redis** para optimizar las consultas.
  - **Servicio de OCR (`/ocr`):** (Futuro) Microservicio para extraer texto de documentos (facturas, recetas).

## Inicio Rápido (Desarrollo Local)

### Prerrequisitos
- Docker y Docker Compose
- Git
- Un archivo `.env` configurado a partir de `env.example` con las credenciales de tu servicio de Odoo.

### Pasos
1. **Clonar el repositorio:**
   ```bash
   git clone <URL_DEL_REPO>
   cd VidafarmaDocker
   ```
2. **Configurar variables de entorno:**
   ```bash
   cp env.example .env
   # Edita el archivo .env con tus credenciales de Odoo y otras configuraciones
   ```
3. **Levantar los servicios:**
   ```bash
   docker-compose up --build
   ```
4. **Acceder a los servicios:**
   - **Frontend:** `http://localhost:3000`
   - **API Docs:** `http://localhost:8000/docs`

---

## Despliegue en Google Cloud (Capa Gratuita)

Esta aplicación está diseñada para desplegarse de forma rentable en la capa gratuita de Google Cloud:

- **Frontend (React PWA):** Se despliega en **Firebase Hosting** para obtener un CDN global, SSL automático y un rendimiento excelente sin coste inicial.
- **Backend (Microservicios FastAPI):** Cada microservicio se empaqueta como un contenedor Docker y se despliega en **Google Cloud Run**, un entorno serverless que escala a cero, por lo que solo pagas por el uso real.

### Pasos para el Despliegue

1.  **Configurar Google Cloud y Firebase:**
    - Crea un proyecto en [Google Cloud Console](https://console.cloud.google.com/).
    - Instala la [CLI de `gcloud`](https://cloud.google.com/sdk/docs/install).
    - Instala la [CLI de Firebase](https://firebase.google.com/docs/cli#install_the_firebase_cli) (`npm install -g firebase-tools`).
    - Asocia tu proyecto local con Firebase: `firebase use --add` y selecciona tu proyecto.

2.  **Desplegar el Backend (API) en Cloud Run:**
    - Navega al directorio del microservicio (ej: `cd backend/api`).
    - Construye y sube la imagen del contenedor a Google Container Registry:
      ```bash
      gcloud builds submit --tag gcr.io/<TU_ID_DE_PROYECTO>/vidafarma-api
      ```
    - Despliega la imagen en Cloud Run:
      ```bash
      gcloud run deploy vidafarma-api --image gcr.io/<TU_ID_DE_PROYECTO>/vidafarma-api --platform managed --region <TU_REGION> --allow-unauthenticated
      ```
    - **Nota:** Deberás configurar las variables de entorno de Odoo como "secrets" en Cloud Run para mayor seguridad.

3.  **Desplegar el Frontend en Firebase Hosting:**
    - Navega al directorio del frontend: `cd frontend`.
    - Construye la aplicación de React para producción:
      ```bash
      npm install
      npm run build
      ```
    - Despliega en Firebase:
      ```bash
      firebase deploy --only hosting
      ```

Tras el despliegue, tendrás la URL de tu frontend en Firebase y la URL de tu backend en Cloud Run. Deberás configurar la variable de entorno `REACT_APP_API_BASE_URL` en tu proyecto de Firebase para que apunte a la URL de Cloud Run.

## Documentación
- **Decisiones Técnicas:** `/docs/decisiones-tecnicas.md`
- **Guía de Desarrollo:** `/docs/guia-desarrollo.md`
- **Seguimiento del Proyecto:** `/seguimiento.md`
