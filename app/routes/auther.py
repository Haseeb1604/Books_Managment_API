from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from ..Database import get_db

# HTTP_201_CREATED
# HTTP_204_NO_CONTENT (After Deletion)
# HTTP_403_FORBIDDEN (Un Autherized)
# HTTP_404_NOT_FOUND
# HTTP_409_CONFLICT (Already Exists)

router = APIRouter(
    prefix="/auther",
    tags=["Auther"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Auther)
def create_auther(auther: schemas._Auther, db: Session = Depends(get_db)):
    new_auther = models.Auther(**auther.dict())
    auther = db.query(models.Auther).filter(models.Auther.name == new_auther.name).first()
    if auther:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = f"Auther with {auther.name} name already exists"
        )
    db.add(new_auther)
    db.commit()
    db.refresh(new_auther)
    return new_auther

@router.get("/", response_model=List[schemas.Auther])
def read_authers(db: Session = Depends(get_db)):
    auther = db.query(models.Auther).all()
    return auther

@router.get("/{id}", response_model=schemas.Auther)
def read_auther(id:int, db: Session = Depends(get_db)):
    auther = db.query(models.Auther).filter(models.Auther.id == id).first()
    if auther is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Auther with ID {auther.id} does not exist"
        )
    return auther