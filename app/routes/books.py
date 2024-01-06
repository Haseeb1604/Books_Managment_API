from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Any, List, Optional
from app import models, schemas

from ..Database import get_db

router = APIRouter(
    prefix="/books",
    tags=["books"]
)

@router.get("/", response_model=List[schemas.BookOut])
def get_books(db: Session = Depends(get_db)):
    posts = db.query(models.Books).all()
    return posts

@router.get("/{id}", response_model=schemas.BookOut)
def get_book(id: int, db: Session = Depends(get_db)):
    book = db.query(models.Books).filter(models.Books.id == id).all()
    if not book:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Book with ID {id} not found"
        )
    return book

@router.post("/", response_model=schemas.BookOut, status_code=status.HTTP_201_CREATED)
def create_item( book: schemas.Book, db: Session = Depends(get_db)):
    new_book = models.Books(**book.dict())
    
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book