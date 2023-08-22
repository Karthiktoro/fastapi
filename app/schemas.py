from datetime import datetime 
from pydantic import BaseModel,EmailStr

class PostBase(BaseModel):
    title : str
    content : str
    published : bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    # title : str
    # id : int
    created_at : datetime

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email : EmailStr
    password :  str