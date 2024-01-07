from jose import jwt, JWTError
from datetime import datetime, timedelta
from app.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRES_MINUTES = settings.ACCESS_TOKEN_EXPIRES_MINUTES

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_MINUTES)
    to_encode.update({'exp': expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt