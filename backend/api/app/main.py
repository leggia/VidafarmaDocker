from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.odoo_service import get_products, get_inventory_movements, get_purchase_orders, get_sales_orders, get_partners

app = FastAPI(title="Vidafarma_IA API", version="1.0.0")

# Modelos Pydantic para validación
class ConsultaIA(BaseModel):
    texto: str
    tipo: Optional[str] = "general"

class Producto(BaseModel):
    nombre: str
    precio: float
    stock: int

# Endpoints básicos
@app.get("/")
def read_root():
    return {"msg": "Vidafarma_IA API funcionando", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "api"}

# Endpoint para consultas de IA (recibe texto de voz o escrito)
@app.post("/api/consulta-ia")
def consulta_ia(consulta: ConsultaIA):
    """
    Endpoint para consultas de IA. Recibe texto (de voz o escrito) y responde.
    """
    try:
        # Aquí irá la lógica de IA para procesar la consulta
        # Por ahora, respuesta simple
        respuesta = f"Consulta recibida: {consulta.texto}. Respuesta de IA pendiente."
        
        return {
            "consulta": consulta.texto,
            "respuesta": respuesta,
            "tipo": consulta.tipo
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoints CRUD básicos (ejemplo con productos)
@app.get("/api/productos")
def get_productos():
    """Obtener lista de productos"""
    # Aquí irá la lógica para obtener productos de la base de datos
    return {"productos": []}

@app.post("/api/productos")
def crear_producto(producto: Producto):
    """Crear un nuevo producto"""
    # Aquí irá la lógica para crear productos
    return {"mensaje": "Producto creado", "producto": producto}

@app.get("/api/odoo/productos")
def odoo_productos():
    """Obtener productos desde Odoo"""
    return {"productos": get_products()}

@app.get("/api/odoo/inventario")
def odoo_inventario():
    """Obtener movimientos de inventario desde Odoo"""
    return {"movimientos": get_inventory_movements()}

@app.get("/api/odoo/compras")
def odoo_compras():
    """Obtener órdenes de compra desde Odoo"""
    return {"compras": get_purchase_orders()}

@app.get("/api/odoo/ventas")
def odoo_ventas():
    """Obtener órdenes de venta desde Odoo"""
    return {"ventas": get_sales_orders()}

@app.get("/api/odoo/partners")
def odoo_partners():
    """Obtener partners/clientes desde Odoo"""
    return {"partners": get_partners()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 