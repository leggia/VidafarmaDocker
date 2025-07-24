from fastapi import Security, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

security = HTTPBearer()

async def verify_firebase_token(auth: HTTPAuthorizationCredentials = Security(security)):
    try:
        decoded_token = id_token.verify_oauth2_token(
            auth.credentials, google_requests.Request(), "TU_FIREBASE_CLIENT_ID"
        )
        return decoded_token
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido")