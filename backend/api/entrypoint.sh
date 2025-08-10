#!/bin/sh

# Salir inmediatamente si un comando falla
set -e

# Imprimir un mensaje de depuración para confirmar que el script se está ejecutando
echo "--- Iniciando entrypoint.sh ---"

# Imprimir el valor de la variable de entorno PORT para depuración
echo "Valor de la variable de entorno PORT: $PORT"

# Imprimir el directorio de trabajo actual y listar sus contenidos
echo "Directorio de trabajo actual: $(pwd)"
ls -la

# Ejecutar la aplicación FastAPI con Uvicorn
# exec asegura que Uvicorn reemplace el proceso del shell, convirtiéndose en el proceso principal (PID 1)
# Esto es una buena práctica para el manejo de señales en contenedores.
echo "Lanzando Uvicorn..."
exec uvicorn main:app --host 0.0.0.0 --port "${PORT}"
