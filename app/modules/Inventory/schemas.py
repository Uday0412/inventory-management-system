from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str
    description: str | None = None

    class Config:
        orm_mode = True


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

    class Config:
        orm_mode = True


class CategoryRead(CategoryBase):
    id: int


class ItemBase(BaseModel):
    sku: str
    name: str
    description: str | None = None
    category_id: int | None = None
    unit: str = "pcs"
    min_qty: int = 0

    class Config:
        orm_mode = True


class ItemCreate(ItemBase):
    initial_qty: int = 0


class ItemUpdate(BaseModel):
    sku: str | None = None
    name: str | None = None
    description: str | None = None
    category_id: int | None = None
    unit: str | None = None
    min_qty: int | None = None

    class Config:
        orm_mode = True


class ItemRead(ItemBase):
    id: int
    current_qty: int


class StockAdjust(BaseModel):
    qty_delta: int
    reason: str = "adjustment"
    note: str | None = None


class StockMovementRead(BaseModel):
    id: int
    item_id: int
    qty_delta: int
    reason: str
    note: str | None

    class Config:
        orm_mode = True

