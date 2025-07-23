from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from .services.ocr_service import OCRService

app = FastAPI(title="Vidafarma_IA OCR Service", version="1.0.0")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar servicio OCR
ocr_service = OCRService()

# Modelos Pydantic
class OCRResult(BaseModel):
    text: str
    confidence: float
    language: str
    processing_time: float

class InvoiceData(BaseModel):
    invoice_number: Optional[str] = None
    date: Optional[str] = None
    total_amount: Optional[str] = None
    supplier: Optional[str] = None
    items: List[dict] = []

# Endpoints básicos
@app.get("/")
def read_root():
    return {"msg": "Vidafarma_IA OCR Service funcionando", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "ocr"}

# Endpoint para procesar imágenes
@app.post("/api/ocr/image", response_model=OCRResult)
async def process_image(file: UploadFile = File(...)):
    """
    Procesa una imagen y extrae texto usando OCR
    """
    try:
        # Validar tipo de archivo
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="El archivo debe ser una imagen")
        
        # Procesar imagen
        result = await ocr_service.process_image(file)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para procesar PDFs
@app.post("/api/ocr/pdf", response_model=List[OCRResult])
async def process_pdf(file: UploadFile = File(...)):
    """
    Procesa un PDF y extrae texto de todas las páginas
    """
    try:
        # Validar tipo de archivo
        if file.content_type != 'application/pdf':
            raise HTTPException(status_code=400, detail="El archivo debe ser un PDF")
        
        # Procesar PDF
        results = await ocr_service.process_pdf(file)
        return results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint para extraer datos de facturas
@app.post("/api/ocr/invoice", response_model=InvoiceData)
async def extract_invoice_data(file: UploadFile = File(...)):
    """
    Extrae datos específicos de facturas (número, fecha, monto, proveedor)
    """
    try:
        # Procesar archivo
        if file.content_type == 'application/pdf':
            results = await ocr_service.process_pdf(file)
            text = "\n".join([r.text for r in results])
        else:
            result = await ocr_service.process_image(file)
            text = result.text
        
        # Extraer datos de factura
        invoice_data = ocr_service.extract_invoice_data(text)
        return invoice_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 