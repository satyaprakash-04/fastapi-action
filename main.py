from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Demo FastAPI with GH Actions CI")

# simple in-memory "db"
_items = {
    1: {"id": 1, "name": "apple", "price": 0.75},
    2: {"id": 2, "name": "banana", "price": 0.5},
}

class ItemIn(BaseModel):
    name: str
    price: float

class ItemOut(ItemIn):
    id: int

@app.get("/")
async def read_root():
    return {"message": "Hello from FastAPI!"}

@app.get("/items/{item_id}", response_model=ItemOut)
async def get_item(item_id: int):
    item = _items.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/items/", response_model=ItemOut, status_code=201)
async def create_item(item_in: ItemIn):
    new_id = max(_items.keys(), default=0) + 1
    item = {"id": new_id, **item_in.dict()}
    _items[new_id] = item
    return item

@app.put("/items/{item_id}", response_model=ItemOut)
async def update_item(item_id: int, item_in: ItemIn):
    if item_id not in _items:
        raise HTTPException(status_code=404, detail="Item not found")
    _items[item_id].update(item_in.dict())
    return _items[item_id]

@app.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: int):
    if item_id not in _items:
        raise HTTPException(status_code=404, detail="Item not found")
    del _items[item_id]
    return None
