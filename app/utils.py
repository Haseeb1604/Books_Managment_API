from passlib.context import CryptoContext

pwd_context = CryptoContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(password:str, hashed_password:str):
    return pwd_context.verify(password, hashed_password)