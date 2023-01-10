from pydantic import BaseModel, EmailStr
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr
    password: str


class User(BaseModel):
    id: int
    email: EmailStr
    # skipping password
    created_at: datetime

    class Config:
        orm_mode = True
