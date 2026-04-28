import os
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-only-secret-key-change-me')
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
revoked_tokens = set()

from domain.interfaces.service_interfaces import IJWTService

class JWTService(IJWTService):
    def create_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire =  datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({'exp': expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)

    def revoke_token(self, token: str):
        revoked_tokens.add(token)

    def is_token_revoked(self, token: str) -> bool:
        return token in revoked_tokens

    def decode_token(self, token: str) -> dict:
        if self.is_token_revoked(token):
            raise HTTPException(status_code=401, detail="Токен відкликано")
        try:
            payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            raise HTTPException(status_code=401, detail="Невірний токен")

def get_current_user(token: str = Depends(oauth2_scheme)):
    service = JWTService()
    payload = service.decode_token(token)
    user_id = payload.get('sub')
    if user_id is None:
        raise HTTPException(status_code=401, detail="Невірний токен")
    return int(user_id)