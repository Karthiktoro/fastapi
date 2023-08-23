from random import randrange
from typing import Optional,List
from urllib import response
from fastapi import FastAPI , HTTPException ,status,Depends
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session

from app import schemas
# from .database import engine
from .routers import post,user,auth

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while(True):
    try:
        con = psycopg2.connect(host= 'localhost' , database= 'fastapi' , user="postgres",password="password",cursor_factory=RealDictCursor)
        cursor = con.cursor()
        print("connection to database established")
        break
    except Exception as error:
        print("connection to database failed")
        print("error" , error)
        time.sleep(2)

my_posts= [{"title":"title of post 1" , "content": "content of post 1" , "id" : 1},
           {"title":"title of post 2" , "content": "content of post 2" , "id" : 2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p
        
def find_index(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i
        
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Hello world "}

@app.get("/posts",response_model=List[schemas.Post])
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return  posts

@app.get("/posts/latest")
def get_latest_post():
    post = my_posts(len(my_posts)-1)
    return  post


