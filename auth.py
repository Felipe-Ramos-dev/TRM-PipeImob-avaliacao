# app/dependencies/auth.py
from fastapi import Header, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import API_TOKEN

bearer_scheme = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)):
    token = credentials.credentials
    if token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Token inválido")
    return True
