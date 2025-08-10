import re
import logging

logger = logging.getLogger(__name__)

# --- Definición de Reglas para el NLU ---
# Cada regla tiene un patrón de regex y la intención correspondiente.
# Los grupos en la regex capturan las entidades.
RULES = [
    {
        "intent": "consultar_precio",
        "pattern": r"cuánto cuesta el|precio de(l)?|valor de(l)?\s+(?P<nombre_producto>.+)",
    },
    {
        "intent": "consultar_stock",
        "pattern": r"tienes|hay|tenemos|stock de\s+(?P<nombre_producto>.+)",
    },
    {
        "intent": "actualizar_precio",
        "pattern": r"actualiza el precio de\s+(?P<nombre_producto>.+)\s+a\s+(?P<precio>[\d\.]+)",
    },
    {
        "intent": "actualizar_stock",
        "pattern": r"(añade|agrega|quita|reduce)\s+(?P<cantidad>-?\d+)\s+(unidades de\s+)?(?P<nombre_producto>.+)",
    },
    {
        "intent": "listar_productos",
        "pattern": r"muéstrame|dame|lista|ver\s+(todos los\s+)?productos",
    },
    {"intent": "saludo", "pattern": r"hola|buenos días|buenas tardes|buenas noches"},
]


async def process_user_intent(user_text: str) -> dict:
    """
    Procesa el texto del usuario usando reglas de regex para extraer intención y entidades.
    """
    if user_text is None:
        logger.warning("process_user_intent received None for user_text.")
        return {"intencion": "desconocido", "entidades": {}}
    user_text = user_text.lower().strip()

    for rule in RULES:
        match = re.search(rule["pattern"], user_text, re.IGNORECASE)
        if match:
            entities = match.groupdict()

            # --- Limpieza y conversión de tipos ---
            if "nombre_producto" in entities:
                entities["nombre_producto"] = entities["nombre_producto"].strip()
            if "precio" in entities:
                try:
                    entities["precio"] = float(entities["precio"])
                except (ValueError, TypeError):
                    # Si la conversión falla, no es una coincidencia válida
                    continue
            if "cantidad" in entities:
                try:
                    # Manejar "quita" o "reduce" como negativo
                    if match.group(1) in ["quita", "reduce"]:
                        entities["cantidad"] = -abs(int(entities["cantidad"]))
                    else:
                        entities["cantidad"] = int(entities["cantidad"])
                except (ValueError, TypeError):
                    continue

            logger.info(
                f"NLU Rule-Based Match: Intent='{rule['intent']}', Entities={entities}"
            )
            return {"intencion": rule["intent"], "entidades": entities}

    # Si ninguna regla coincide
    logger.warning(f"NLU No Match: No se encontró una intención para: '{user_text}'")
    return {"intencion": "desconocido", "entidades": {}}