from fastapi import FastAPI
from core.config import settings
from database.db import engine, Base
from modules.User.router import router as UserRouter
from modules.Inventory.router import router as InventoryRouter

# Ensure models are imported before table creation
from modules.User import models as _user_models  # noqa: F401
from modules.Inventory import models as _inventory_models  # noqa: F401

# Table creation
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
)

app.include_router(UserRouter)
app.include_router(InventoryRouter)

@app.get("/")
async def root():
    return {"message": "welcome to fastapi Enterprice","docs":"/docs",}