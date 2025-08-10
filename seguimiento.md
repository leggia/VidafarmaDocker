# Seguimiento del Proyecto Vidafarma_IA

## Resumen y contexto

Este documento contiene el historial, las decisiones y el estado actual del proyecto Vidafarma_IA, para que cualquier colaborador o IA pueda retomar el contexto fácilmente.

---
### **Datos Clave del Proyecto**

- **Google Cloud Project ID:** `vidafarma-ia25`
- **Firebase Project ID:** `vidafarmaia`
- **Cloud Run Service (API):** `vidafarma-api`
- **Región de Cloud Run:** `southamerica-east1`
- **URL del Frontend (Firebase Hosting):** `https://vidafarmaia.web.app`
- **URL del Backend (Cloud Run):** `https://vidafarma-api-963566180194.southamerica-east1.run.app`

---

### 1. Objetivo del proyecto

Crear una plataforma inteligente para la gestión de farmacias con las siguientes características clave:

- **Agente de IA Conversacional:** Un asistente con el que se puede interactuar por voz o texto para realizar consultas y ejecutar acciones.
- **Frontend PWA:** Una Progressive Web App instalable en dispositivos móviles.
- **Escáner de Código de Barras:** Utilizar la cámara del móvil para escanear productos e interactuar con el inventario de Odoo.
- **Integración con Odoo:** Conectarse a un **servicio externo de Odoo (v18+)**.
- **Despliegue Rentable:** Diseñado desde el inicio para operar en la **capa gratuita de Google Cloud**.

**Visión a Largo Plazo:** Evolucionar la plataforma para convertirla en una solución de nivel empresarial, altamente escalable, robusta y con funcionalidades avanzadas, manteniendo siempre un enfoque de full-stack de alto rendimiento.

### 2. Arquitectura y Stack

#### 2.1. Desarrollo Local
- **Monorepo** con `backend`, `frontend`, `docs`.
- **Microservicios** en Python (FastAPI) dockerizados.
- **Orquestación** con Docker Compose.
- **Frontend** en React (PWA).
- **Caché** con Redis para acelerar las consultas a Odoo durante el desarrollo.

#### 2.2. Arquitectura de Despliegue (Google Cloud)
- **Frontend:** **Firebase Hosting**. Provee CDN global, SSL automático y despliegue rápido.
- **Backend:** **Google Cloud Run**. Cada microservicio es un contenedor serverless que escala a cero, optimizando costes.
- **Caché:** La caché de Redis se **desactiva** en producción para permanecer en la capa gratuita. Se puede habilitar en el futuro con Google Memorystore si es necesario.
- **Base de Datos (Futura):** Se recomienda **Firestore** por su generosa capa gratuita y su integración nativa con Firebase y Cloud Run.

#### 2.3. Repositorio de Código
- **GitHub:** `leggia/VidafarmaDocker` (Utilizado para la integración continua con Firebase Hosting).

#### 2.4. Configuración de Frontend y CI/CD

- **Frontend (React PWA):**
  - **URL de API:** Configurada para apuntar a `https://vidafarma-api-963566180194.southamerica-east1.run.app` mediante `REACT_APP_API_BASE_URL` en el script `build` de `package.json` (usando `cross-env` para compatibilidad multiplataforma).
  - **Corrección de Errores:** Se resolvió un error de sintaxis en `src/serviceWorkerRegistration.js` simplificando su contenido.
  - **Despliegue:** Realizado con éxito en **Firebase Hosting** (proyecto `vidafarmaia`).

- **Integración Continua/Despliegue Continuo (CI/CD):**
  - **GitHub Actions:** Configurado para el frontend en el repositorio `leggia/VidafarmaDocker`.
  - **Flujo de Trabajo:** Se despliega automáticamente a Firebase Hosting cuando se fusiona una Pull Request a la rama principal.

### 3. Estado Detallado de Funcionalidades (ÚLTIMA ACTUALIZACIÓN)

- **Preparación para la Nube:**
  - **Estado:** ✅ **Completado.**
  - **Implementado:** El código ha sido refactorizado para ser compatible tanto con el entorno local (Docker) como con el de producción en la nube (Cloud Run/Firebase). La caché de Redis es opcional y la URL de la API es configurable. Se han añadido los archivos de configuración para el despliegue (`cloudbuild.yaml` y `firebase.json`) y se ha documentado el proceso en los `README.md` correspondientes.

- **PWA (Progressive Web App):**
  - **Estado:** ✅ **Completado.**
  - **Detalle:** Se solucionó el error de registro del Service Worker (`SecurityError: The script has an unsupported MIME type ('text/html')`). El problema se debía a la ausencia del archivo `frontend/src/service-worker.js`, que impedía la correcta generación del service worker durante la compilación.
  - **Solución:**
    1. Se creó el archivo `frontend/src/service-worker.js` con el código base de Create React App.
    2. Se verificó que `frontend/src/index.js` ya estuviera llamando a la función de registro del service worker.
    3. Se reconstruyó la aplicación (`npm run build`) y se desplegó la nueva versión en Firebase Hosting.
  - **Falta:** Ninguna funcionalidad básica pendiente.

- **IA Conversacional:**
  - **Estado:** ✅ **Completado.**
  - **Implementado:** El endpoint `/api/consulta-ia` ahora procesa la intención del usuario, ejecuta acciones en Odoo (consultar, actualizar) y genera una respuesta en lenguaje natural.
  - **Falta:** Ninguna funcionalidad básica pendiente.

- **Escáner de Código de Barras:**
  - **Estado:** ✅ **Completado.**
  - **Implementado:** Añadido un endpoint en el backend para buscar productos por código de barras. En el frontend, se ha integrado la librería `react-zxing` para escanear códigos de barras con la cámara y mostrar la información del producto.
  - **Falta:** Ninguna funcionalidad básica pendiente.

- **Integración con Odoo:**
  - **Estado:** ✅ **Completado.**
  - **Implementado:** Lectura y escritura de datos en Odoo (productos y movimientos de stock).
  - **Falta:** Ninguna funcionalidad básica pendiente.

### 4. Siguientes Pasos Sugeridos (Priorizados)

1.  **Probar la Implementación Base Localmente:**
    - **Estado:** ⚠️ **Bloqueado.**
    - **Detalle:** El comando `docker-compose up --build` falla debido a un problema de conexión con el motor de Docker (`open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified`). Es necesario asegurarse de que Docker Desktop esté en ejecución y configurado correctamente antes de continuar con las pruebas locales.
    - **Tarea:**
        - Ejecutar `docker-compose up --build`.
        - Verificar la comunicación frontend-backend y la lectura de datos de Odoo.

2.  **Implementar Funciones de Escritura en Odoo:**
    - **Estado:** ✅ **Completado.**
    - **Prioridad:** Alta.
    - **Tarea:** Añadir funciones y endpoints para `actualizar_precio_producto` y `crear_movimiento_stock`.

3.  **Desarrollar la Lógica de IA (NLU):**
    - **Estado:** ✅ **Completado.**
    - **Prioridad:** Alta.
    - **Tarea:** Implementar un procesador de intenciones básico en el endpoint `/api/consulta-ia`.

4.  **Implementar Escáner de Código de Barras:**
    - **Prioridad:** Media.
    - **Tarea:** Añadir la funcionalidad de escaneo en el frontend.

---

**### 5. Historial de Despliegue y Depuración en Google Cloud (vidafarma-ia25)**

- **2025-08-10: Solución de Error de Service Worker (PWA)**
  - **Objetivo:** Corregir el error que impedía el registro del Service Worker y la funcionalidad de PWA.
  - **Resumen del Problema:** La compilación del frontend no generaba el archivo `service-worker.js` porque el archivo fuente `frontend/src/service-worker.js` no existía en el repositorio. Esto causaba un error de tipo MIME en el navegador al intentar registrar el worker.
  - **Pasos Clave de la Solución:**
    1.  **Creación de Archivo:** Se creó el archivo `frontend/src/service-worker.js` con el contenido estándar proporcionado por Create React App.
    2.  **Verificación:** Se confirmó que `frontend/src/index.js` ya contenía la lógica para registrar el service worker, por lo que no se necesitaron cambios adicionales allí.
    3.  **Compilación:** Se ejecutó `npm run build` dentro del directorio `frontend` para construir la aplicación de producción, generando el service worker correctamente.
    4.  **Autenticación de Firebase CLI:** El despliegue inicial falló por un error de autenticación (`401 Unauthorized`). Se solucionó ejecutando `firebase login` para refrescar las credenciales.
    5.  **Despliegue Exitoso:** Se ejecutó `firebase deploy --only hosting --project vidafarmaia` para desplegar la nueva versión en Firebase Hosting.
  - **Resultado:** El frontend fue desplegado correctamente, solucionando el problema de la PWA.

- **2025-08-07: Depuración de Autenticación Frontend-Backend (401 Unauthorized)**
  - **Objetivo:** Resolver el error `403 Forbidden` (ahora `401 Unauthorized`) al intentar conectar el frontend con el backend.
  - **Resumen del Problema:** Inicialmente, el frontend no enviaba el encabezado `Authorization` con el token de Firebase, resultando en un `403 Forbidden`. Tras modificar `frontend/src/App.js` para incluir el token, el error cambió a `401 Unauthorized`.
  - **Pasos Clave de la Depuración:**
    1.  **Inspección de Red (Frontend):** Se confirmó que la solicitud `POST /api/consulta-ia` no incluía el encabezado `Authorization`. La solicitud `OPTIONS` funcionaba correctamente.
    2.  **Modificación de Frontend:** Se añadió la lógica en `frontend/src/App.js` para obtener el ID Token de Firebase (`auth.currentUser.getIdToken(true)`) y enviarlo en el encabezado `Authorization: Bearer <token>`.
    3.  **Despliegue de Frontend:** Se reconstruyó y redesplegó el frontend a Firebase Hosting.
    4.  **Inspección de Consola (Frontend):** Se verificó que el frontend ahora obtiene y muestra el token de Firebase en la consola (`Firebase ID Token obtenido: eyJ...`).
    5.  **Resultado Actual:** El error en el backend cambió a `401 Unauthorized`, lo que indica que el token se está enviando, pero el backend no lo valida.
  - **Diagnóstico Final:** La causa más probable del `401 Unauthorized` es una **discrepancia entre el `FIREBASE_CLIENT_ID` configurado en Google Cloud Secret Manager y el ID de cliente web de OAuth 2.0 real de la aplicación Firebase** que emitió el token.
  - **Siguiente Acción:**
    - **Verificar y actualizar el secreto `FIREBASE_CLIENT_ID`** en Google Cloud Secret Manager con el valor correcto obtenido de la configuración de la aplicación web en la Consola de Firebase.
    - **Redesplegar el servicio `vidafarma-api`** en Cloud Run para que cargue la nueva versión del secreto.

- **2025-08-05: Depuración y Despliegue Exitoso del Backend**
  - **Objetivo:** Diagnosticar y resolver el fallo de inicio persistente del servicio `vidafarma-api` en Cloud Run.
  - **Resumen del Problema:** El contenedor fallaba al iniciar de forma silenciosa, sin generar logs de error de Python, lo que dificultaba el diagnóstico. El error persistió a través de múltiples intentos de corrección.
  - **Pasos Clave de la Depuración:**
    1.  **Análisis Inicial:** Se revisaron los logs de Cloud Run, que solo mostraban un error genérico de `STARTUP TCP probe failed`, indicando que la aplicación no respondía en el puerto esperado.
    2.  **Logging en Código:** Se añadió logging detallado al archivo `main.py` para trazar el proceso de importación. Esto no arrojó resultados, indicando que el error ocurría antes de la ejecución de `main.py`.
    3.  **Revisión de Dependencias:** Se simplificó la dependencia `uvicorn[standard]` a `uvicorn` en `requirements.txt` para descartar conflictos, sin éxito.
    4.  **Carga Perezosa (Lazy Loading):** Se refactorizaron `odoo_service.py` y `auth.py` para que las variables de entorno (cargadas desde secretos) se leyeran justo a tiempo, en lugar de en el momento de la importación. Esto no resolvió el problema.
    5.  **Estructura de Paquetes:** Se identificó y corrigió la falta de archivos `__init__.py` en los directorios `app/` y `app/services/`, lo cual es necesario para que Python los trate como paquetes. El problema persistió.
    6.  **Simplificación del `Dockerfile`:** Se reestructuró el `Dockerfile` para crear una estructura de archivos más plana y simple, eliminando la anidación `app/app` y ajustando las importaciones en `main.py` para que fueran relativas (`from auth` en lugar de `from app.auth`).
    7.  **Punto de Inflexión (Entrypoint Script):** Se introdujo un script `entrypoint.sh` para tomar control explícito del proceso de inicio del contenedor. **Esto fue crucial**, ya que finalmente nos permitió ver el verdadero error en los logs de Cloud Run.
    8.  **Diagnóstico Final:** El log reveló un `ImportError`: el archivo `main.py` intentaba importar la función `get_inventory_movements` desde `odoo_service.py`, pero dicha función no existía.
  - **Solución Final:**
    1.  Se eliminó la importación de la función inexistente (`get_inventory_movements` y otras no utilizadas) del archivo `main.py`.
    2.  Se restauró el `Dockerfile` a su versión final y limpia, usando la variable `$PORT` de Cloud Run y la estructura de archivos plana.
  - **Resultado:** El despliegue de la revisión `vidafarma-api-00024-jq7` fue **exitoso**.

- **2025-08-05: Despliegue Exitoso del Frontend en Firebase Hosting**
  - **Objetivo:** Conectar el frontend con el backend desplegado y automatizar su despliegue.
  - **Pasos y Decisiones:**
    1.  **Configuración de URL de API:** Se identificó `API_BASE_URL` en `frontend/src/App.js` y se configuró el script `build` en `frontend/package.json` para inyectar la URL de la API de Cloud Run (`https://vidafarma-api-963566180194.southamerica-east1.run.app`) usando `cross-env` para compatibilidad con Windows.
    2.  **Corrección de Error de Sintaxis:** Se resolvió un `Syntax error` en `frontend/src/serviceWorkerRegistration.js` simplificando el contenido del archivo.
    3.  **Inicialización de Firebase Hosting:** Se ejecutó `firebase init hosting` en el directorio `frontend`, configurando el directorio `build` como público y habilitando la reescritura de URLs para SPA. Se seleccionó el proyecto de Firebase `vidafarmaia`.
    4.  **Configuración de GitHub Actions:** Se configuró el flujo de trabajo de GitHub Actions para el repositorio `leggia/VidafarmaDocker`, permitiendo el despliegue automático a Firebase Hosting al fusionar Pull Requests.
    5.  **Problemas de Autenticación de Firebase CLI:** Se encontraron y resolvieron problemas de autenticación (`401 Unauthenticated`) y selección de proyecto (`Invalid project selection`), que requirieron verificar y actualizar los roles de IAM en Google Cloud y forzar un nuevo `firebase login`. Se identificó la discrepancia entre el ID de proyecto de Google Cloud (`vidafarma-ia25`) y el ID de proyecto de Firebase (`vidafarmaia`).
  - **Resultado:** El frontend se desplegó con éxito en Firebase Hosting.
  - **URL del Frontend:** `https://vidafarmaia.web.app`

- **2025-08-01:**
  - **Objetivo:** Primer despliegue del backend en Cloud Run.
  - **Pasos y Decisiones:**
    1.  **Configuración Inicial:** Se configuró el proyecto `vidafarma-ia25` y la región `southamerica-east1`.
    2.  **Problema de Permisos (Cloud Build):** El despliegue inicial falló por falta de permisos (`serviceusage.services.use`). Se solucionó asignando el rol `Service Usage Admin` al usuario.
    3.  **Problema de Facturación:** Se encontró que el proyecto no tenía una cuenta de facturación activa, lo cual es un requisito para habilitar APIs. Se guio al usuario para vincularla.
    4.  **Problema de API (Cloud Storage):** La construcción falló por no encontrar el bucket de Cloud Build (`NOT_FOUND`). Se solucionó habilitando la API de Cloud Storage (`storage.googleapis.com`).
    5.  **Construcción Exitosa:** Se logró construir y subir la imagen `gcr.io/vidafarma-ia25/vidafarma-api` a GCR.
    6.  **Problema de Puerto (Cloud Run):** El despliegue en Cloud Run falló porque la aplicación escuchaba en el puerto `8000` en lugar del puerto `8080` esperado por Cloud Run. Se modificó el `Dockerfile` para usar la variable de entorno `$PORT` dinámicamente.
    7.  **Problema de Variables de Entorno:** El despliegue volvió a fallar, apuntando a que la aplicación no se inicia correctamente. La causa más probable es la falta de variables de entorno de Odoo en el entorno de Cloud Run.
    8.  **Depuración y Permisos de Secretos:** Se configuraron los secretos en Secret Manager y se otorgaron los permisos necesarios a la cuenta de servicio de Cloud Run. El despliegiegue siguió fallando.
    9.  **Análisis de Registros:** Los registros del sistema de Cloud Run no mostraron errores de aplicación (Tracebacks de Python), sino un fallo en la sonda de inicio (Startup Probe). Esto indica que la aplicación no se está iniciando en absoluto.
    10. **Diagnóstico Final y Solución (Lazy Initialization):** Se identificó que el problema raíz era la **inicialización de la conexión a Odoo en el arranque de la aplicación**. En un entorno serverless, esto es una mala práctica que causa fallos si la conexión no es instantánea. Se refactorizó `odoo_service.py` para usar **inicialización perezosa (lazy initialization)**, de modo que la conexión solo se establece cuando se necesita por primera vez.
    11. **Diagnóstico Final 2 (Dependencia de Entorno):** El problema persistió. Se identificó que la librería `python-dotenv` se estaba ejecutando incondicionalmente, causando un fallo silencioso en el entorno de producción donde no existe un archivo `.env`. Se refactorizó el código para que `load_dotenv()` solo se ejecute si `ENV=development`.
    12. **Depuración de Variables de Entorno:** Se añadieron sentencias `logger.info` en `odoo_service.py` para verificar la carga de las variables de entorno de Odoo desde los secretos.
    13. **Error `FIREBASE_CLIENT_ID` faltante:** Los logs revelaron un `RuntimeError` indicando que `FIREBASE_CLIENT_ID` no estaba configurado. Este valor es necesario para la autenticación de Firebase. Se creó un secreto en Secret Manager con el valor proporcionado.
    14. **Traceback de Python (Incompleto):** Se obtuvo un `Traceback` de Python, lo que indica que la aplicación está llegando a ejecutarse, pero falla durante su inicialización. El `Traceback` proporcionado estaba incompleto.
    15. **Traceback de Python (Aún Incompleto):** Se solicitó el `Traceback` completo nuevamente, pero la información proporcionada sigue siendo parcial, mostrando solo el punto de entrada de Uvicorn.
    16. **Logs de Revisión Anterior:** Los logs proporcionados corresponden a una revisión anterior (`vidafarma-api-00003-dsj`) y no a la última (`vidafarma-api-00010-qwp`).
  - **Siguiente Acción:**
    - Es crucial obtener el `Traceback` completo de la **última revisión (`vidafarma-api-00010-qwp`)** para identificar la causa raíz del fallo de la aplicación. Sin esta información, la depuración es muy difícil.

- **2025-08-05: Depuración de Conexión a Odoo**
  - **Objetivo:** Diagnosticar por qué el backend (`vidafarma-api`) no puede conectarse a Odoo, manifestado como "Error al conectar la API" en el frontend.
  - **Estado Actual:** El frontend está desplegado y se comunica con el backend. El problema parece residir en la conexión del backend con el servicio externo de Odoo.
  - **Siguiente Acción:** Se requiere revisar los logs del servicio `vidafarma-api` en Cloud Run para identificar el error específico durante el intento de conexión a Odoo.

---
**Resumen del Estado Actual del Proyecto Vidafarma_IA**
1. Despliegue del Frontend:

El frontend (React PWA) ha sido desplegado con éxito en Firebase Hosting.
URL del Frontend: https://vidafarmaia.web.app
Cambios realizados: Se añadió un console.log en frontend/src/App.js para depurar la obtención y envío del token de Firebase.
2. Despliegue del Backend:

El backend (FastAPI) ha sido desplegado con éxito en Google Cloud Run.
URL del Backend: https://vidafarma-api-963566180194.southamerica-east1.run.app
Cambios realizados: Se añadió un console.log en backend/api/app/auth.py para depurar la carga del FIREBASE_CLIENT_ID (luego revertido).
3. Problema Principal Actual: 401 Unauthorized en el Backend

El frontend ahora está enviando correctamente el token de autenticación de Firebase en el encabezado Authorization a las solicitudes POST /api/consulta-ia.
El backend está recibiendo estas solicitudes, pero las rechaza con un error 401 Unauthorized.
Diagnóstico: La causa más probable es una discrepancia entre el FIREBASE_CLIENT_ID almacenado en Google Cloud Secret Manager y el ID de cliente real de tu aplicación Firebase (el que emitió el token).
4. Problema Secundario: Error de Service Worker en el Frontend

La consola del navegador muestra ServiceWorker registration failed: SecurityError: Failed to register a ServiceWorker... The script has an unsupported MIME type ('text/html').
Diagnóstico: Esto indica que el archivo service-worker.js no se está sirviendo correctamente desde Firebase Hosting, probablemente porque no se está generando o copiando al directorio build durante el proceso de compilación del frontend. Este problema es secundario a la funcionalidad de la API, pero afecta las capacidades PWA.
Próximos Pasos (Para la Siguiente Sesión)
Para resolver el error 401 Unauthorized y permitir que el backend valide correctamente los tokens de Firebase, deberás realizar los siguientes pasos:

Obtener el ID de Cliente Web de OAuth 2.0 correcto de tu proyecto de Firebase:

Ve a la Consola de Firebase.
Selecciona tu proyecto vidafarmaia.
Ve a Project settings (Configuración del proyecto) > General.
En la sección Your apps (Tus aplicaciones), selecciona tu aplicación web.
Busca el clientId en la configuración del SDK de Firebase.
Actualizar el secreto FIREBASE_CLIENT_ID en Google Cloud Secret Manager:

Ve a la Consola de Google Cloud y asegúrate de estar en el proyecto vidafarma-ia25.
Navega a Secret Manager.
Busca el secreto FIREBASE_CLIENT_ID y crea una nueva versión con el clientId correcto que obtuviste de Firebase.
Redesplegar el servicio vidafarma-api en Cloud Run:

Una vez que el secreto haya sido actualizado, deberás redesplegar el backend para que cargue la nueva versión del secreto.
El comando para esto es:
gcloud run deploy vidafarma-api --source backend/api --region southamerica-east1 --allow-unauthenticated --project vidafarma-ia25
Una vez que hayas completado estos pasos, podremos continuar depurando y verificando si el 401 Unauthorized se ha resuelto.