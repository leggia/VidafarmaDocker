import logging

logger = logging.getLogger(__name__)
logger.info("Iniciando main.py...")

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
# Corregido: Importaciones relativas a la nueva estructura plana
from auth import verify_firebase_token
from services.odoo_service import (
    get_products,
    update_product_price, create_stock_movement,
    find_product_by_name, find_product_by_barcode
)
from services.ia_service import process_user_intent

app = FastAPI(title="Vidafarma_IA API", version="1.0.0")

# CORS
origins = [
    "http://localhost:3000",
    "https://vidafarmaia.web.app",
    "https://vidafarmaia.firebaseapp.com"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos
class ConsultaIA(BaseModel):
    texto: str
    tipo: Optional[str] = "general"

class ProductPriceUpdate(BaseModel):
    new_price: float

class StockMovementCreate(BaseModel):
    product_id: int
    quantity: float
    source_location_id: int
    destination_location_id: int

# --- Action Dispatcher --- 
def execute_action(nlu_result: dict):
    """Ejecuta la acción correspondiente basada en la intención y entidades."""
    intencion = nlu_result.get('intencion')
    entidades = nlu_result.get('entidades', {})
    nombre_producto = entidades.get('nombre_producto')

    if not intencion:
        return {"respuesta": "No pude entender tu petición. ¿Puedes reformularla?"}

    # --- Lógica para cada intención ---
    if intencion == "saludo":
        return {"respuesta": "¡Hola! Soy tu asistente de farmacia. ¿En qué puedo ayudarte?"}

    if intencion == "listar_productos":
        productos = get_products()
        if not productos:
            return {"respuesta": "No encontré productos en el inventario."}
        
        lista_productos = ", ".join([p['name'] for p in productos[:10]]) # Limita a 10 para brevedad
        return {"respuesta": f"Aquí tienes algunos productos: {lista_productos}."}

    if not nombre_producto:
        return {"respuesta": "Por favor, especifica el nombre del producto."}

    # --- Acciones que requieren buscar el producto ---
    producto = find_product_by_name(nombre_producto)
    if not producto:
        return {"respuesta": f"No encontré el producto '{nombre_producto}'."}

    if intencion == "consultar_precio":
        return {"respuesta": f"El precio de {producto['name']} es S/ {producto['list_price']:.2f}."}

    if intencion == "consultar_stock":
        return {"respuesta": f"Tenemos {int(producto['qty_available'])} unidades de {producto['name']} en stock."}

    if intencion == "actualizar_precio":
        nuevo_precio = entidades.get('precio')
        if not nuevo_precio:
            return {"respuesta": "No especificaste el nuevo precio."}
        
        update_product_price(producto['id'], nuevo_precio)
        return {"respuesta": f"He actualizado el precio de {producto['name']} a S/ {nuevo_precio:.2f}."}

    # Nota: La creación de movimientos de stock es más compleja y requiere IDs de ubicación.
    # Esta implementación es una simplificación.
    if intencion == "actualizar_stock":
        cantidad = entidades.get('cantidad')
        if not cantidad:
            return {"respuesta": "No especificaste la cantidad a actualizar."}
        
        # Asumimos ubicaciones predeterminadas (ej: 1=Stock, 2=Cliente)
        # Esto debería ser más robusto en una implementación real
        origen_id = 1 if cantidad < 0 else 2
        destino_id = 2 if cantidad < 0 else 1

        create_stock_movement(producto['id'], abs(cantidad), origen_id, destino_id)
        return {"respuesta": f"He actualizado el stock de {producto['name']} en {cantidad} unidades."}

    return {"respuesta": "No pude realizar la acción solicitada."}

# --- Endpoints ---
@app.get("/")
def read_root():
    return {"msg": "Vidafarma_IA API funcionando", "version": "1.0.0"}

@app.post("/api/consulta-ia")
async def consulta_ia(consulta: ConsultaIA, user=Depends(verify_firebase_token)):
    try:
        nlu_result = await process_user_intent(consulta.texto)
        respuesta = execute_action(nlu_result)
        return {
            "consulta": consulta.texto,
            "respuesta_ia": respuesta,
            "resultado_nlu": nlu_result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/odoo/product/barcode/{barcode}")
def odoo_product_by_barcode(barcode: str, user=Depends(verify_firebase_token)):
    producto = find_product_by_barcode(barcode)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado.")
    return producto

@app.put("/api/odoo/product/{product_id}/price")
def odoo_update_product_price(product_id: int, price_update: ProductPriceUpdate, user=Depends(verify_firebase_token)):
    result = update_product_price(product_id, price_update.new_price)
    if not result:
        raise HTTPException(status_code=404, detail="Producto no encontrado o error al actualizar.")
    return {"status": "ok", "message": f"Precio del producto {product_id} actualizado a {price_update.new_price}"}

@app.post("/api/odoo/stock/movement")
def odoo_create_stock_movement(movement: StockMovementCreate, user=Depends(verify_firebase_token)):
    result = create_stock_movement(
        movement.product_id,
        movement.quantity,
        movement.source_location_id,
        movement.destination_location_id
    )
    if not result:
        raise HTTPException(status_code=500, detail="Error al crear el movimiento de stock.")
    return {"status": "ok", "message": "Movimiento de stock creado.", "movement_id": result}
