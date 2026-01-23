# app/api/items_router.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from dependency_injector.wiring import Provide, inject

 
from app.core.container import Container
from app.core.interfaces.i_item_service import IItemService
from app.core.models.item import Item
from app.core.exceptions import NotFoundError

router = APIRouter(
    prefix="/items",
    tags=["items"],
)

@router.get("/test")
@inject
async def read_root_items():
    return {"message": "Items API working!"}

@router.get("/", response_model=List[Item])
@inject
def list_items(service: IItemService = Depends(Provide[Container.item_service])):
    return service.list()

@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED)
@inject
def create_item(
    body: Item,
    service: IItemService = Depends(Provide[Container.item_service]),
):
    return service.create(body)

@router.put("/{item_id}", response_model=Item)
@inject
def update_item(
    item_id: int,
    body: Item,
    service: IItemService = Depends(Provide[Container.item_service]),
):
    try:
        return service.update(item_id, body)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
def delete_item(
    item_id: int,
    service: IItemService = Depends(Provide[Container.item_service]),
):
    try:
        service.delete(item_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
