FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

# Usar la forma "shell" de CMD para permitir la expansión de la variable de entorno $PORT
CMD uvicorn main:app --host 0.0.0.0 --port $PORT