from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from .models import Category, Item, StockMovement


def list_categories(db: Session):
    return db.query(Category).order_by(Category.name.asc()).all()


def get_category(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()


def create_category(db: Session, name: str, description: str | None):
    category = Category(name=name, description=description)
    db.add(category)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    db.refresh(category)
    return category


def update_category(db: Session, category: Category, name: str | None, description: str | None):
    if name is not None:
        category.name = name
    category.description = description
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    db.refresh(category)
    return category


def delete_category(db: Session, category: Category):
    db.delete(category)
    db.commit()


def list_items(db: Session):
    return db.query(Item).order_by(Item.name.asc()).all()


def get_item(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()


def create_item(
    db: Session,
    *,
    sku: str,
    name: str,
    description: str | None,
    category_id: int | None,
    unit: str,
    min_qty: int,
    initial_qty: int,
):
    item = Item(
        sku=sku,
        name=name,
        description=description,
        category_id=category_id,
        unit=unit,
        min_qty=min_qty,
        current_qty=0,
    )
    db.add(item)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    db.refresh(item)

    if initial_qty != 0:
        adjust_stock(
            db,
            item=item,
            qty_delta=initial_qty,
            reason="initial",
            note="Initial stock on item creation",
        )
        db.refresh(item)

    return item


def update_item(
    db: Session,
    item: Item,
    *,
    sku: str | None,
    name: str | None,
    description: str | None,
    category_id: int | None,
    unit: str | None,
    min_qty: int | None,
):
    if sku is not None:
        item.sku = sku
    if name is not None:
        item.name = name
    item.description = description
    item.category_id = category_id
    if unit is not None:
        item.unit = unit
    if min_qty is not None:
        item.min_qty = min_qty

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    db.refresh(item)
    return item


def delete_item(db: Session, item: Item):
    db.delete(item)
    db.commit()


def adjust_stock(
    db: Session,
    *,
    item: Item,
    qty_delta: int,
    reason: str,
    note: str | None,
):
    item.current_qty = int(item.current_qty) + int(qty_delta)
    movement = StockMovement(item_id=item.id, qty_delta=qty_delta, reason=reason, note=note)
    db.add(movement)
    db.commit()
    db.refresh(item)
    db.refresh(movement)
    return item, movement


def list_item_movements(db: Session, item_id: int):
    return (
        db.query(StockMovement)
        .filter(StockMovement.item_id == item_id)
        .order_by(StockMovement.id.desc())
        .all()
    )

