import os
import xmlrpc.client
import logging
from dotenv import load_dotenv
from threading import Lock

# --- Configuración de Logging ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Variables Globales de Conexión ---
# Se inicializan a None y se poblarán de forma perezosa.
uid = None
models = None
connection_lock = Lock()

# --- Función de Conexión Refactorizada (Verdaderamente Perezosa) ---
def get_odoo_connection():
    """
    Establece y devuelve una conexión a Odoo de forma perezosa y segura para hilos.
    La configuración (variables de entorno) también se carga de forma perezosa.
    """
    global uid, models
    # Doble chequeo para evitar bloqueos innecesarios
    if models is not None:
        return uid, models

    with connection_lock:
        # Volver a chequear dentro del bloqueo por si otro hilo ya la creó
        if models is not None:
            return uid, models

        logger.info("No hay conexión con Odoo. Intentando conectar y cargar configuración...")

        # 1. Carga condicional de .env (solo para desarrollo)
        if os.getenv("ENV") == "development":
            logger.info("Entorno de desarrollo detectado. Cargando .env...")
            load_dotenv()

        # 2. Carga perezosa de la configuración
        ODOO_HOST = os.getenv("ODOO_HOST")
        ODOO_PORT = os.getenv("ODOO_PORT")
        ODOO_DB = os.getenv("ODOO_DB")
        ODOO_USER = os.getenv("ODOO_USER")
        ODOO_PASSWORD = os.getenv("ODOO_PASSWORD")

        # 3. Validación de la configuración
        if not all([ODOO_HOST, ODOO_DB, ODOO_USER, ODOO_PASSWORD]):
            logger.error("Faltan variables de entorno de Odoo. No se puede conectar.")
            # Logueamos las variables que sí se encontraron para depuración
            logger.error(f"Valores actuales -> HOST: {ODOO_HOST}, DB: {ODOO_DB}, USER: {ODOO_USER}")
            raise ValueError("Las variables de entorno de Odoo son obligatorias.")

        # 4. Intento de conexión
        try:
            protocol = "https" if ODOO_PORT == "443" else "http"
            url = f"{protocol}://{ODOO_HOST}:{ODOO_PORT}"
            
            common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
            local_uid = common.authenticate(ODOO_DB, ODOO_USER, ODOO_PASSWORD, {})
            if not local_uid:
                raise ConnectionRefusedError("Autenticación con Odoo falló. Revisa las credenciales.")

            # Asignación a las variables globales solo en caso de éxito
            uid = local_uid
            models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
            logger.info("Conexión con Odoo establecida exitosamente.")
            return uid, models
        except Exception as e:
            logger.error(f"No se pudo conectar con Odoo durante el intento de conexión: {e}")
            # Reseteamos para que el próximo intento pueda funcionar
            uid = None
            models = None
            raise

# --- Función de Ejecución (Usa la conexión perezosa) ---
def execute_odoo_kw(model, method, args, kwargs, cache_key=None, cache_expiry=3600):
    """
    Ejecuta una llamada a Odoo, obteniendo la conexión de forma perezosa.
    """
    try:
        uid_conn, models_conn = get_odoo_connection()
        ODOO_DB = os.getenv("ODOO_DB")
        ODOO_PASSWORD = os.getenv("ODOO_PASSWORD")

        logger.info(f"Ejecutando en Odoo: model={model}, method={method}, args={args}, kwargs={kwargs}")
        result = models_conn.execute_kw(ODOO_DB, uid_conn, ODOO_PASSWORD, model, method, args, kwargs)
        logger.info(f"Resultado de Odoo: {result}")
        return result
    except xmlrpc.client.Fault as e:
        logger.error(f"Error de Odoo (xmlrpc.client.Fault) al ejecutar {model}.{method}: {e.faultCode} - {e.faultString}")
        raise
    except Exception as e:
        logger.error(f"Error inesperado en execute_odoo_kw al ejecutar {model}.{method}: {e}", exc_info=True)
        raise

# --- Funciones de Lógica de Negocio (Sin Cambios) ---
# No necesitan cambios porque dependen de execute_odoo_kw, que ahora es completamente perezoso.

def get_products():
    return execute_odoo_kw(
        model='product.product',
        method='search_read',
        args=[[]],
        kwargs={'fields': ['name', 'list_price', 'qty_available']},
        cache_key='odoo_products'
    )

def update_product_price(product_id: int, new_price: float):
    return execute_odoo_kw(
        model='product.product',
        method='write',
        args=[[product_id], {'list_price': new_price}],
        kwargs={},
        cache_key=None
    )

def find_product_by_barcode(barcode: str):
    products = execute_odoo_kw(
        model='product.product',
        method='search_read',
        args=[[['barcode', '=', barcode]]],
        kwargs={'fields': ['id', 'name', 'list_price', 'qty_available'], 'limit': 1},
        cache_key=f"product_barcode_search_{barcode}"
    )
    return products[0] if products else None

def find_product_by_name(name: str):
    # Usar % para búsqueda parcial
    search_name = f"%{name}%"
    products = execute_odoo_kw(
        model='product.product',
        method='search_read',
        args=[[['name', 'ilike', search_name]]],
        kwargs={
            'fields': ['id', 'name', 'list_price', 'qty_available'],
            'limit': 1,
            'order': 'name'
        },
        cache_key=f"product_name_search_{name}"
    )
    return products[0] if products else None

def create_stock_movement(product_id: int, quantity: float, source_location_id: int, destination_location_id: int):
    return execute_odoo_kw(
        model='stock.move',
        method='create',
        args=[[{
            'name': 'Movimiento desde API',
            'product_id': product_id,
            'product_uom_qty': quantity,
            'location_id': source_location_id,
            'location_dest_id': destination_location_id,
        }]],
        kwargs={},
        cache_key=None
    )

# ... (el resto de funciones de negocio se mantienen igual)
