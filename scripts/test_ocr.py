import requests
import os

BASE_URL = "http://localhost:8001/api/ocr"
imagen_path = r"C:\Users\WINDOWS\OneDrive\Documentos\Proyecto_automatizacion\data\factura.png"      # Cambia por la ruta real de tu imagen
pdf_path = r"C:\Users\WINDOWS\OneDrive\Documentos\Proyecto_automatizacion\data\factura_ejemplo.pdf"        # Cambia por la ruta real de tu PDF

def test_image():
    with open(imagen_path, "rb") as f:
        files = {"file": (os.path.basename(imagen_path), f, "image/png")}  # Cambia a image/jpeg si es JPG
        response = requests.post(f"{BASE_URL}/image", files=files)
        print("Respuesta /image:", response.status_code)
        print(response.json())

def test_pdf():
    with open(pdf_path, "rb") as f:
        files = {"file": (os.path.basename(pdf_path), f, "application/pdf")}
        response = requests.post(f"{BASE_URL}/pdf", files=files)
        print("Respuesta /pdf:", response.status_code)
        print(response.json())

def test_invoice():
    with open(pdf_path, "rb") as f:
        files = {"file": (os.path.basename(pdf_path), f, "application/pdf")}
        response = requests.post(f"{BASE_URL}/invoice", files=files)
        print("Respuesta /invoice:", response.status_code)
        print(response.json())

if __name__ == "__main__":
    print("Imagen existe:", os.path.isfile(imagen_path), "Tamaño:", os.path.getsize(imagen_path) if os.path.isfile(imagen_path) else 0)
    print("PDF existe:", os.path.isfile(pdf_path), "Tamaño:", os.path.getsize(pdf_path) if os.path.isfile(pdf_path) else 0)
    print("Probando OCR de imagen...")
    test_image()
    print("\nProbando OCR de PDF...")
    test_pdf()
    print("\nProbando extracción de datos de factura...")
    test_invoice() 