from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from app.auth import verify_firebase_token
from app.services.odoo_service import (
    get_products, get_inventory_movements, 
    get_purchase_orders, get_sales_orders, get_partners
)

app = FastAPI(title="Vidafarma_IA API", version="1.0.0")

# CORS
origins = [
    "http://localhost:3000",
    "https://TUDOMINIO.firebaseapp.com",
    "https://TUDOMINIO.web.app"
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

class Producto(BaseModel):
    nombre: str
    precio: float
    stock: int

# Endpoints públicos
@app.get("/")
def read_root():
    return {"msg": "Vidafarma_IA API funcionando", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "api"}

@app.post("/api/consulta-ia")
def consulta_ia(consulta: ConsultaIA):
    try:
        respuesta = f"Consulta recibida: {consulta.texto}. Respuesta de IA pendiente."
        return {
            "consulta": consulta.texto,
            "respuesta": respuesta,
            "tipo": consulta.tipo
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# CRUD de productos (demo)
@app.get("/api/productos")
def get_productos():
    return {"productos": []}

@app.post("/api/productos")
def crear_producto(producto: Producto):
    return {"mensaje": "Producto creado", "producto": producto}

# Rutas protegidas con Firebase Auth
@app.get("/api/protegido")
def endpoint_protegido(user=Depends(verify_firebase_token)):
    return {"msg": f"Hola {user['email']}"}

# Odoo integraciones
@app.get("/api/odoo/productos")
def odoo_productos():
    return {"productos": get_products()}

@app.get("/api/odoo/inventario")
def odoo_inventario():
    return {"movimientos": get_inventory_movements()}

@app.get("/api/odoo/compras")
def odoo_compras():
    return {"compras": get_purchase_orders()}

@app.get("/api/odoo/ventas")
def odoo_ventas():
    return {"ventas": get_sales_orders()}

@app.get("/api/odoo/partners")
def odoo_partners():
    return {"partners": get_partners()}
