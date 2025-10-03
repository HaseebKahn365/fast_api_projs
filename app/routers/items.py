from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..config.database import get_db
# SQLAlchemy model
from ..models.sql_models import Item as ItemModel
# Pydantic schemas
from ..models.schemas import ItemCreate, Item as ItemSchema
from ..routers.auth import get_current_user
from sqlalchemy.future import select
from typing import List

router = APIRouter()

@router.post("/items/", response_model=ItemSchema)
async def create_item(item: ItemCreate, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    db_item = ItemModel(**item.dict(), owner_id=current_user.id)
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item

@router.get("/items/", response_model=List[ItemSchema])
async def read_items(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ItemModel).offset(skip).limit(limit))
    items = result.scalars().all()
    return items

@router.get("/items/{item_id}", response_model=ItemSchema)
async def read_item(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ItemModel).where(ItemModel.id == item_id))
    item = result.scalars().first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.put("/items/{item_id}", response_model=ItemSchema)
async def update_item(item_id: int, item: ItemCreate, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(ItemModel).where(ItemModel.id == item_id))
    db_item = result.scalars().first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    if db_item.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    for key, value in item.dict().items():
        setattr(db_item, key, value)
    await db.commit()
    await db.refresh(db_item)
    return db_item

@router.delete("/items/{item_id}")
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(ItemModel).where(ItemModel.id == item_id))
    db_item = result.scalars().first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    if db_item.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    await db.delete(db_item)
    await db.commit()
    return {"message": "Item deleted"}