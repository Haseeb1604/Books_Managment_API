from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str
    usertype: Optional[str] = "normal"

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    usertype: str
    created_At: datetime

class _BookBase(BaseModel):
    title: str
    price: int
    auther: str
    publisher: str
    created_At: datetime

class Book(_BookBase):
    id: int
 
class BookOut(_BookBase):
    pass

