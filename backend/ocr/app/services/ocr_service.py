import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import io
import time
import re
from pdf2image import convert_from_bytes
from typing import List, Optional
import os

class OCRService:
    def __init__(self):
        # Configurar Tesseract
        pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
        
        # Configurar idiomas (español + inglés)
        self.languages = 'spa+eng'
        
        # Configuración OCR
        self.config = '--oem 3 --psm 6'
    
    async def process_image(self, file) -> dict:
        """
        Procesa una imagen y extrae texto usando OCR
        """
        start_time = time.time()
        
        try:
            # Leer archivo
            contents = await file.read()
            
            # Convertir a imagen PIL
            image = Image.open(io.BytesIO(contents))
            
            # Preprocesar imagen
            processed_image = self._preprocess_image(image)
            
            # Extraer texto
            text = pytesseract.image_to_string(
                processed_image, 
                lang=self.languages, 
                config=self.config
            )
            
            # Obtener confianza
            confidence = self._get_confidence(processed_image)
            
            processing_time = time.time() - start_time
            
            return {
                "text": text.strip(),
                "confidence": confidence,
                "language": self.languages,
                "processing_time": round(processing_time, 2)
            }
            
        except Exception as e:
            raise Exception(f"Error procesando imagen: {str(e)}")
    
    async def process_pdf(self, file) -> List[dict]:
        """
        Procesa un PDF y extrae texto de todas las páginas
        """
        start_time = time.time()
        results = []
        
        try:
            # Leer archivo
            contents = await file.read()
            
            # Convertir PDF a imágenes
            images = convert_from_bytes(contents)
            
            for i, image in enumerate(images):
                page_start_time = time.time()
                
                # Preprocesar imagen
                processed_image = self._preprocess_image(image)
                
                # Extraer texto
                text = pytesseract.image_to_string(
                    processed_image, 
                    lang=self.languages, 
                    config=self.config
                )
                
                # Obtener confianza
                confidence = self._get_confidence(processed_image)
                
                page_processing_time = time.time() - page_start_time
                
                results.append({
                    "text": text.strip(),
                    "confidence": confidence,
                    "language": self.languages,
                    "processing_time": round(page_processing_time, 2),
                    "page": i + 1
                })
            
            return results
            
        except Exception as e:
            raise Exception(f"Error procesando PDF: {str(e)}")
    
    def _preprocess_image(self, image):
        """
        Preprocesa la imagen para mejorar el OCR usando PIL
        """
        # Convertir a escala de grises si es necesario
        if image.mode != 'L':
            image = image.convert('L')
        
        # Mejorar contraste
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2.0)
        
        # Mejorar nitidez
        image = image.filter(ImageFilter.SHARPEN)
        
        # Reducir ruido
        image = image.filter(ImageFilter.MedianFilter(size=3))
        
        return image
    
    def _get_confidence(self, image) -> float:
        """
        Obtiene la confianza del OCR
        """
        try:
            # Obtener datos de confianza
            data = pytesseract.image_to_data(
                image, 
                lang=self.languages, 
                config=self.config,
                output_type=pytesseract.Output.DICT
            )
            
            # Calcular confianza promedio
            confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
            
            if confidences:
                return round(sum(confidences) / len(confidences), 2)
            else:
                return 0.0
                
        except:
            return 0.0
    
    def extract_invoice_data(self, text: str) -> dict:
        """
        Extrae datos específicos de facturas del texto OCR
        """
        invoice_data = {
            "invoice_number": None,
            "date": None,
            "total_amount": None,
            "supplier": None,
            "items": []
        }
        
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Buscar número de factura
            if not invoice_data["invoice_number"]:
                invoice_match = re.search(r'(?:factura|invoice|recibo|ticket)\s*#?\s*(\d+)', line, re.IGNORECASE)
                if invoice_match:
                    invoice_data["invoice_number"] = invoice_match.group(1)
            
            # Buscar fecha
            if not invoice_data["date"]:
                date_match = re.search(r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})', line)
                if date_match:
                    invoice_data["date"] = date_match.group(1)
            
            # Buscar monto total
            if not invoice_data["total_amount"]:
                total_match = re.search(r'(?:total|suma|amount)\s*:?\s*\$?\s*([\d,]+\.?\d*)', line, re.IGNORECASE)
                if total_match:
                    invoice_data["total_amount"] = total_match.group(1)
            
            # Buscar proveedor (líneas que contengan palabras clave de farmacias)
            if not invoice_data["supplier"]:
                supplier_keywords = ['farmacia', 'pharmacy', 'droguería', 'laboratorio', 'distribuidor']
                if any(keyword in line.lower() for keyword in supplier_keywords):
                    invoice_data["supplier"] = line.strip()
        
        return invoice_data 