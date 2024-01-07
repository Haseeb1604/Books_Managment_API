from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class _UserBase(BaseModel):
    name: str
    email: EmailStr
    usertype: Optional[str] = "normal"

class UserCreate(_UserBase):
    password: str
    
class UserOut(_UserBase):
    id: int
    created_At: datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class _Publisher(BaseModel):
    name: str

class Publisher(_Publisher):
    id: int
    created_At: datetime

class _Auther(BaseModel):
    name: str

class Auther(_Auther):
    id: int
    created_At: datetime

class _BookBase(BaseModel):
    title: str
    price: int

class Book(_BookBase):
    auther_id: int
    publisher_id: int
 
class BookOut(_BookBase):
    id: int
    created_At: datetime
    owner: UserOut
    auther: Auther
    publisher: Publisher