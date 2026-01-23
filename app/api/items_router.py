from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

from app.core.models.item import Item



# Simularemos una base de datos con una lista
fake_db: List[Item] = []

router = APIRouter()

@router.post("/items", response_model=Item, status_code=201)
async def create_item(item: Item):
    fake_db.append(item)
    return item

@router.get("/items", response_model=List[Item])
async def read_items():
    return fake_db

@router.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item: Item):
    for idx, existing_item in enumerate(fake_db):
        if existing_item.id == item_id:
            fake_db[idx] = item
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@router.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: int):
    for idx, existing_item in enumerate(fake_db):
        if existing_item.id == item_id:
            del fake_db[idx]
            return
    raise HTTPException(status_code=404, detail="Item not found")
