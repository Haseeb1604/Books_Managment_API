from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Any, List, Optional
from app import models, schemas
from ..Database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# HTTP_201_CREATED
# HTTP_204_NO_CONTENT (After Deletion)
# HTTP_403_FORBIDDEN (Un Autherized)
# HTTP_404_NOT_FOUND
# HTTP_409_CONFLICT (Already Exists)

@router.post("/", response_model=schemas.UserOut)
def create_item(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.Users(**user.dict())
    user = db.query(models.Users).filter(models.Users.email == new_user.email).first()
    if user:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = f"User with {user.email} email address already exists"
        )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/", response_model=List[schemas.UserOut])
def read_items(db: Session = Depends(get_db)):
    users = db.query(models.Users).all()
    return users

@router.get("/{id}", response_model=schemas.UserOut)
def read_items(id:int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user.id} does not exist"
        )
    return user
