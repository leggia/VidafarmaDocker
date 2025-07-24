from fastapi import Security, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import os

security = HTTPBearer()
FIREBASE_CLIENT_ID = os.environ.get("FIREBASE_CLIENT_ID")

if not FIREBASE_CLIENT_ID:
    raise RuntimeError("FIREBASE_CLIENT_ID no está configurado en variables de entorno.")

async def verify_firebase_token(auth: HTTPAuthorizationCredentials = Security(security)):
    try:
        # Verificar el token de ID enviado por el cliente
        decoded_token = id_token.verify_oauth2_token(
            auth.credentials,
            google_requests.Request(),
            FIREBASE_CLIENT_ID
        )

        # Validación adicional
        if "email" not in decoded_token or "sub" not in decoded_token:
            raise HTTPException(status_code=401, detail="Token inválido: campos incompletos")

        return decoded_token

    except ValueError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
