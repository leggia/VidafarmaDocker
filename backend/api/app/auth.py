import logging
import os
from fastapi import Security, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import firebase_admin
from firebase_admin import credentials, auth

logger = logging.getLogger(__name__)
security = HTTPBearer()

# --- Inicialización de Firebase Admin ---
# Esto se ejecuta solo una vez cuando se carga el módulo.
if not firebase_admin._apps:
    # En un entorno de producción (Cloud Run), las credenciales se infieren automáticamente
    # del entorno de ejecución. Sin embargo, debemos especificar el ID del proyecto de Firebase
    # para que la validación del token (audiencia) funcione correctamente.
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
        'projectId': 'vidafarmaia',
    })
    logger.info("Firebase Admin SDK inicializado para el proyecto 'vidafarmaia'.")

async def verify_firebase_token(auth_header: HTTPAuthorizationCredentials = Security(security)):
    """
    Verifica el token de ID de Firebase usando el SDK de Firebase Admin.
    """
    if not auth_header or not auth_header.credentials:
        raise HTTPException(status_code=403, detail="No se proporcionó un token de autenticación.")

    id_token = auth_header.credentials
    try:
        # Verificar el token de ID enviado por el cliente
        decoded_token = auth.verify_id_token(id_token)

        # Validación adicional (opcional, pero recomendada)
        if "email" not in decoded_token or "sub" not in decoded_token:
            logger.warning(f"Token inválido para {decoded_token.get('email')}: campos incompletos.")
            raise HTTPException(status_code=401, detail="Token inválido: campos incompletos")

        return decoded_token

    except auth.InvalidIdTokenError as e:
        logger.error(f"El token de ID no es válido: {e}")
        raise HTTPException(status_code=401, detail="El token de ID no es válido.")
    except Exception as e:
        logger.error(f"Error inesperado durante la verificación del token: {e}")
        raise HTTPException(status_code=500, detail="Error del servidor al verificar la autenticación.")