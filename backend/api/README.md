# Microservicio API (FastAPI)

Este microservicio es el núcleo de la lógica de negocio de Vidafarma_IA. Expone endpoints REST para el frontend y orquesta la integración con IA, OCR y Odoo.

## Estructura sugerida
- `app/` Código fuente principal (FastAPI)
- `Dockerfile` Imagen para despliegue
- `requirements.txt` Dependencias Python

## Endpoints principales
- CRUD de productos, inventario, compras
- Consultas inteligentes vía IA
- Integración con OCR y Odoo

Documenta aquí cualquier decisión técnica relevante para este microservicio.

## Despliegue

Este microservicio está configurado para ser desplegado en Google Cloud Run. Para desplegarlo, sigue estos pasos:

1.  **Asegúrate de tener Google Cloud SDK instalado y configurado.**

2.  **Navega al directorio `backend/api`**

3.  **Ejecuta el siguiente comando:**

    ```bash
    gcloud builds submit --config cloudbuild.yaml .
    ```

Esto construirá la imagen de Docker, la subirá a Google Container Registry y la desplegará en Cloud Run. 