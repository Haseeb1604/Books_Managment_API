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

class _BookBase(BaseModel):
    title: str
    price: int
    auther: str
    publisher: str

class Book(_BookBase):
    pass
 
class BookOut(_BookBase):
    id: int
    created_At: datetime

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