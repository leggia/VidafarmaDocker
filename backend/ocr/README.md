# Microservicio OCR - Vidafarma_IA

## Descripción
Microservicio para reconocimiento óptico de caracteres (OCR) que procesa imágenes y PDFs para extraer texto, especialmente optimizado para facturas de farmacias.

## Tecnologías
- **FastAPI** - Framework web
- **Tesseract** - Motor OCR principal
- **OpenCV** - Procesamiento de imágenes
- **Pillow** - Manipulación de imágenes
- **pdf2image** - Conversión de PDFs a imágenes

## Características
- ✅ Procesamiento de imágenes (JPG, PNG, etc.)
- ✅ Procesamiento de PDFs (múltiples páginas)
- ✅ Extracción de datos específicos de facturas
- ✅ Soporte para español e inglés
- ✅ Preprocesamiento automático de imágenes
- ✅ Medición de confianza del OCR

## Endpoints

### `/api/ocr/image`
**POST** - Procesa una imagen y extrae texto
```bash
curl -X POST "http://localhost:8001/api/ocr/image" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@imagen.jpg"
```

### `/api/ocr/pdf`
**POST** - Procesa un PDF y extrae texto de todas las páginas
```bash
curl -X POST "http://localhost:8001/api/ocr/pdf" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@factura.pdf"
```

### `/api/ocr/invoice`
**POST** - Extrae datos específicos de facturas
```bash
curl -X POST "http://localhost:8001/api/ocr/invoice" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@factura.pdf"
```

## Respuestas

### OCR Result
```json
{
  "text": "Texto extraído...",
  "confidence": 85.5,
  "language": "spa+eng",
  "processing_time": 1.23
}
```

### Invoice Data
```json
{
  "invoice_number": "12345",
  "date": "15/07/2024",
  "total_amount": "1,250.00",
  "supplier": "Farmacia Central",
  "items": []
}
```

## Desarrollo

### Construir imagen
```bash
docker build -t vidafarma_ia-ocr ./backend/ocr
```

### Ejecutar localmente
```bash
cd backend/ocr
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8001
```

### Con Docker Compose
```bash
docker-compose up ocr
```

## Integración con Odoo
El servicio OCR se puede integrar con Odoo para:
- Crear facturas automáticamente desde PDFs
- Extraer datos de proveedores
- Procesar recibos de compra
- Automatizar entrada de inventario

## Optimizaciones
- Preprocesamiento automático de imágenes
- Reducción de ruido
- Mejora de contraste
- Binarización adaptativa
- Soporte multiidioma 