from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database.db import get_db

from . import views
from .schemas import (
    CategoryCreate,
    CategoryRead,
    CategoryUpdate,
    ItemCreate,
    ItemRead,
    ItemUpdate,
    StockAdjust,
    StockMovementRead,
)

router = APIRouter(prefix="/inventory", tags=["inventory"])


@router.get("/categories", response_model=list[CategoryRead])
async def get_categories(db: Session = Depends(get_db)):
    return views.list_categories(db)


@router.post("/categories", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
async def create_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    try:
        return views.create_category(db, name=payload.name, description=payload.description)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Category name already exists")


@router.patch("/categories/{category_id}", response_model=CategoryRead)
async def patch_category(category_id: int, payload: CategoryUpdate, db: Session = Depends(get_db)):
    category = views.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    data = payload.dict(exclude_unset=True)
    try:
        return views.update_category(
            db,
            category,
            name=data.get("name"),
            description=data.get("description") if "description" in data else category.description,
        )
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Category name already exists")


@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_category(category_id: int, db: Session = Depends(get_db)):
    category = views.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    views.delete_category(db, category)


@router.get("/items", response_model=list[ItemRead])
async def get_items(db: Session = Depends(get_db)):
    return views.list_items(db)


@router.post("/items", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
async def create_item(payload: ItemCreate, db: Session = Depends(get_db)):
    try:
        return views.create_item(
            db,
            sku=payload.sku,
            name=payload.name,
            description=payload.description,
            category_id=payload.category_id,
            unit=payload.unit,
            min_qty=payload.min_qty,
            initial_qty=payload.initial_qty,
        )
    except IntegrityError:
        raise HTTPException(status_code=400, detail="SKU already exists (or invalid category)")


@router.patch("/items/{item_id}", response_model=ItemRead)
async def patch_item(item_id: int, payload: ItemUpdate, db: Session = Depends(get_db)):
    item = views.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    data = payload.dict(exclude_unset=True)
    try:
        return views.update_item(
            db,
            item,
            sku=data.get("sku"),
            name=data.get("name"),
            description=data.get("description") if "description" in data else item.description,
            category_id=data.get("category_id") if "category_id" in data else item.category_id,
            unit=data.get("unit"),
            min_qty=data.get("min_qty"),
        )
    except IntegrityError:
        raise HTTPException(status_code=400, detail="SKU already exists (or invalid category)")


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_item(item_id: int, db: Session = Depends(get_db)):
    item = views.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    views.delete_item(db, item)


@router.post("/items/{item_id}/adjust", response_model=ItemRead)
async def adjust_item_stock(item_id: int, payload: StockAdjust, db: Session = Depends(get_db)):
    item = views.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item, _movement = views.adjust_stock(
        db, item=item, qty_delta=payload.qty_delta, reason=payload.reason, note=payload.note
    )
    return item


@router.get("/items/{item_id}/movements", response_model=list[StockMovementRead])
async def get_item_movements(item_id: int, db: Session = Depends(get_db)):
    item = views.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return views.list_item_movements(db, item_id=item_id)

