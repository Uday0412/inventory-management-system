# Routes
from fastapi import APIRouter,Depends
from . schemas import UserRead
from database.db import get_db
from sqlalchemy.orm import Session
from . import views

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

# http://localhost:8000/users/get-users/

@router.get("/get-users", response_model=list[UserRead])
async def read_users(db:Session=Depends(get_db)):
    users = views.get_users(db)
    return users