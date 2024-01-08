from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Any, List, Optional
from app import models, schemas, utils

from . import oauth2

from ..Database import get_db

# HTTP_201_CREATED
# HTTP_204_NO_CONTENT (After Deletion)
# HTTP_403_FORBIDDEN (Un Autherized)
# HTTP_404_NOT_FOUND
# HTTP_409_CONFLICT (Already Exists)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    new_user = models.Users(**user.dict())
    new_user.password = utils.hash(new_user.password)
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
def read_users(
    db: Session = Depends(get_db),
    current_user: schemas.CurrentUser = Depends(oauth2.get_current_user)
    ):
    if current_user.usertype == "normal":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail= f"Not autherized to perfrom requested operation"
            )
    users = db.query(models.Users).all()
    return users

@router.get("/{id}", response_model=schemas.UserOut)
def read_user(
    id:int, db: Session = Depends(get_db),
    current_user: schemas.CurrentUser = Depends(oauth2.get_current_user)
    ):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user.id} does not exist"
        )
    if current_user.id != user.id and current_user.usertype != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail= f"Not autherized to perfrom requested operation"
            )
    return user

@router.delete("/{id}")
def delete_user(
    id: int, db: Session = Depends(get_db),
    current_user: schemas.CurrentUser = Depends(oauth2.get_current_user)
    ):
    if current_user.id!= id and current_user.usertype!= "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail= f"Not autherized to perfrom requested operation"
            )
    user = db.query(models.Users).filter(models.Users.id == id)
    if user.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {id} does not exist"
        )
    user.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", status_code=status.HTTP_201_CREATED ,response_model=schemas.Auther)
def update_user(
    id: int, user: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: schemas.CurrentUser = Depends(oauth2.get_current_user)
    ):

    if current_user.id!= id and current_user.usertype!= "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail= f"Not autherized to perfrom requested operation"
            )

    user_query = db.query(models.Users).filter(models.Users.id == id)
    if user_query.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user.id} does not exist"
        )
    
    user_query.update(user.dict(), synchronize_session=False)
    db.commit()

    return user_query.first()