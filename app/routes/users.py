from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Any, List, Optional
from app import models, schemas


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/", response_model=Any)
def read_items(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    filter: str = None,
    order_by: str = None,
    include: str = None,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:

    if crud.user.is_superuser(current_user):
        items = crud.item.get_multi(db, skip=skip, limit=limit,filter=filter,order_by=order_by,include=include)
    else:
        items = crud.item.get_multi_by_owner(
            db=db,   skip=skip, limit=limit,filter=filter
        )

    return items


@router.post("/", response_model=Any)
def create_item(
    *,
    db: Session = Depends(deps.get_db),
    item_in: schemas.itemCreate,

) -> Any:

    item = crud.item.create_with_owner(db=db, obj=item_in)
    return item


@router.get("/{id}", response_model=schemas.item)
def read_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get item by ID.
    """
    item = crud.item.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="item not found")

    return item


@router.delete("/{id}", response_model=schemas.item)
def delete_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an item.
    """
    item = crud.item.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="item not found")

    item = crud.item.remove(db=db, id=id)
    return item
