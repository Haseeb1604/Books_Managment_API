from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Any, List, Optional
from app import models, schemas

from . import oauth2

from app.Database import get_db

router = APIRouter(
    prefix="/books",
    tags=["books"]
)

# HTTP_201_CREATED
# HTTP_204_NO_CONTENT (After Deletion)
# HTTP_403_FORBIDDEN (Un Autherized)
# HTTP_404_NOT_FOUND
# HTTP_409_CONFLICT (Already Exists)

@router.get("/", response_model=List[schemas.BookOut])
def get_books(db: Session = Depends(get_db)):
    posts = db.query(models.Books).all()
    return posts

@router.get("/{id}",  response_model=schemas.BookOut)
def get_single_book(
    id: int, response: Response, 
    db: Session = Depends(get_db)
    ):
    
    book = db.query(models.Books).filter(models.Books.id == id).first()
    if not book:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Book with ID {id} not found"
        )
    return book

@router.post("/", response_model=schemas.BookOut, status_code=status.HTTP_201_CREATED)
def create_item(
    book: schemas.Book, 
    db: Session = Depends(get_db),
    current_user: schemas.CurrentUser = Depends(oauth2.get_current_user)
    ):
    new_book = models.Books(
        owner_id = current_user.id,
        **book.dict()
        )
    
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book

@router.delete("/{id}")
def delete_book( 
    id: int, 
    db: Session = Depends(get_db),
    current_user: schemas.CurrentUser = Depends(oauth2.get_current_user)
    ):

    book = db.query(models.Books).filter(models.Books.id == id)

    if book.first() is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Book with ID {id} not found"
        )

    if (book.first().owner_id != current_user.id) and (current_user.usertype == "normal"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail= f"Not autherized to perfrom requested operation"
            )
    
    book.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.BookOut)
def update_book(
    id: int, book: schemas.Book,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
    ):
    
    book_query = db.query(models.Books).filter(models.Books.id == id)

    if book_query.first() is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Book with ID {id} not found"
        )

    if (book_query.first().owner_id != current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail= f"Not autherized to perfrom requested operation"
            )

    book_query.update(book.dict(), synchronize_session=False)
    db.commit()

    return book_query.first()