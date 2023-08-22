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
<<<<<<< HEAD
    password :  str
=======
    password :  str

class UserOut(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime
    
    class Config:
        orm_mode = True
>>>>>>> 0815ff361e1ecc162849136dcd0b6593b74e6540
