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
    prefix="/publisher",
    tags=["publisher"],
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Publisher)
def create_publisher(
    publisher: schemas._Publisher, 
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
    ):
    new_publisher = models.Publisher(**publisher.dict())
    publisher = db.query(models.Publisher).filter(models.Publisher.name == new_publisher.name).first()
    if publisher:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = f"Publisher with {publisher.name} name already exists"
        )
    db.add(new_publisher)
    db.commit()
    db.refresh(new_publisher)
    return new_publisher

@router.get("/", response_model=List[schemas.Publisher])
def read_publishers(db: Session = Depends(get_db)):
    publisher = db.query(models.Publisher).all()
    return publisher

@router.get("/{id}", response_model=schemas.Publisher)
def read_publisher(id:int, db: Session = Depends(get_db)):
    publisher = db.query(models.Publisher).filter(models.Publisher.id == id).first()
    if publisher is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Publisher with ID {id} does not exist"
        )
    return publisher

@router.delete("/{id}")
def delete_publisher(
    id: int, db: Session = Depends(get_db),
    current_user: schemas.CurrentUser = Depends(oauth2.get_current_user)
    ):

    if current_user.usertype != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this auther"
        )

    publisher_query = db.query(models.Publisher).filter(models.Publisher.id == id)
    if publisher_query.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Auther with ID {id} does not exist"
        )
    publisher_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}', status_code=status.HTTP_201_CREATED ,response_model=schemas.Publisher)
def update_publisher(
    id: int, publisher: schemas._Publisher,
    db: Session = Depends(get_db),
    current_user: schemas.CurrentUser = Depends(oauth2.get_current_user)
    ):
    if current_user.usertype != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this auther"
        )

    publisher_query = db.query(models.Publisher).filter(models.Publisher.id == id)
    if publisher_query.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Auther with ID {id} does not exist"
        )
    
    publisher_query.update(publisher.dict(), synchronize_session=False)
    db.commit()

    return publisher_query.first()