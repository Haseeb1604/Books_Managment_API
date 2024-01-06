from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Any, List, Optional
from app import models, schemas

from ..Database import get_db


router = APIRouter(
    prefix="/books",
    tags=["books"]
)

@router.get("/", response_model=List[schemas.Book])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Books).all()
    return posts
