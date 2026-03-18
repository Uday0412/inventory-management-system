from pydantic import BaseModel

# Response schema
class UserRead(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True

# User Create Schema
class UserCreate(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True
