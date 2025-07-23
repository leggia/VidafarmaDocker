import os
import xmlrpc.client
import json
import redis
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

ODOO_HOST = os.getenv("ODOO_HOST", "localhost")
ODOO_PORT = os.getenv("ODOO_PORT", "443")
ODOO_DB = os.getenv("ODOO_DB", "agenteia_odoo")
ODOO_USER = os.getenv("ODOO_USER", "odoo")
ODOO_PASSWORD = os.getenv("ODOO_PASSWORD", "odoo")

# Usar HTTPS para instancias remotas, HTTP para locales
protocol = "https" if ODOO_PORT == "443" else "http"
url = f"{protocol}://{ODOO_HOST}:{ODOO_PORT}"
common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(ODOO_DB, ODOO_USER, ODOO_PASSWORD, {})
models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

# Configuración de Redis
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

def get_from_cache(key):
    data = redis_client.get(key)
    if data:
        return json.loads(data.decode('utf-8'))
    return None

def set_to_cache(key, data, expiry=3600):
    redis_client.set(key, json.dumps(data), ex=expiry)

def get_products():
    try:
        products = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'product.product', 'search_read', [[]], {'fields': ['name', 'list_price', 'qty_available']})
        return products
    except Exception as e:
        print(f"Error obteniendo productos: {e}")
        return []

def get_inventory_movements():
    try:
        moves = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'stock.move', 'search_read', [[]], {'fields': ['id', 'date', 'product_id', 'product_uom_qty', 'location_id', 'location_dest_id', 'state']})
        return moves
    except Exception as e:
        return []

def get_purchase_orders():
    try:
        purchases = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'purchase.order', 'search_read', [[]], {'fields': ['id', 'date_order', 'partner_id', 'state', 'order_line']})
        return purchases
    except Exception as e:
        return []

def get_sales_orders():
    try:
        sales = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'sale.order', 'search_read', [[]], {'fields': ['id', 'date_order', 'partner_id', 'state', 'order_line']})
        return sales
    except Exception as e:
        return []

def get_partners():
    try:
        partners = models.execute_kw(ODOO_DB, uid, ODOO_PASSWORD, 'res.partner', 'search_read', [[]], {'fields': ['id', 'name', 'customer_rank', 'supplier_rank']})
        return partners
    except Exception as e:
        return [] 