# Frontend PWA (React)

Aplicación web progresiva para Vidafarma_IA. Permite interacción con cámara, micrófono y consultas por voz a la IA.

## Estructura sugerida
- `public/` Archivos estáticos
- `src/` Código fuente React
  - `components/` Componentes reutilizables
  - `hooks/` Hooks personalizados (incluyendo voz)
  - `services/` Lógica para consumir APIs y voz

## Funcionalidad de voz
- Utiliza la Web Speech API para reconocimiento y síntesis de voz.
- Permite consultas habladas a la IA (ejemplo: “¿Precio del ibuprofeno?”).

Documenta aquí cualquier decisión técnica relevante para el frontend.

## Despliegue

Este frontend está configurado para ser desplegado en Firebase Hosting. Para desplegarlo, sigue estos pasos:

1.  **Asegúrate de tener Firebase CLI instalado y configurado.**

2.  **Navega al directorio `frontend`**

3.  **Instala las dependencias:**

    ```bash
    npm install
    ```

4.  **Construye la aplicación:**

    ```bash
    npm run build
    ```

5.  **Despliega en Firebase:**

    ```bash
    firebase deploy --only hosting
    ``` 