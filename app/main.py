from random import randrange
from typing import Optional,List
from urllib import response
from fastapi import FastAPI , HTTPException ,status,Depends
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models , schemas
from sqlalchemy.orm import Session
from .database import engine , SessionLocal ,get_db

models.Base.metadata.create_all(bind=engine)

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

@app.get("/")
async def root():
    return {"message": "Hello world "}


@app.get("/posts",response_model=List[schemas.Post])
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return  posts

@app.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post: schemas.PostCreate,db: Session= Depends(get_db)):
    # cursor.execute("""INSERT INTO posts(title,content,published) VALUES(%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # con.commit()  
    new_post = models.Post(**post.dict()) 
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post

@app.get("/posts/latest")
def get_latest_post():
    post = my_posts(len(my_posts)-1)
    return  post

@app.get("/posts/{id}",response_model=schemas.Post)
def get_post(id :int ,db : Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts where id = %s""",(str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                      detail = f"post with id : {id} is not found"
        )
    return  post 

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id :int , db : Session = Depends(get_db)):
        # cursor.execute("""DELETE FROM posts WHERE id = %s returning*""",(str(id)),)
        # delete_post = cursor.fetchone()
        # con.commit()
        delete_post =  db.query(models.Post).filter(models.Post.id==id)
        if delete_post == None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
         detail=f"post with id : {id} is not found")
        delete_post.delete(synchronize_session=False)
        db.commit()
        return {"message " : delete_post}


@app.put("/posts/{id}",response_model=schemas.Post)
def update_post(id:int , updated_post :schemas.PostCreate, db : Session = Depends(get_db)):
    
    # cursor.execute("""UPDATE posts SET title=%s ,content=%s, published=%s WHERE id = %s RETURNING*""",(post.title,post.content,post.published,str(id)))
    # updated_post = cursor.fetchone()
    # con.commit()

    post_query =db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} is not found")
    
    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return  post_query.first()


@app.post("/users",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_user(user: schemas.UserCreate , db: Session= Depends(get_db)):

        new_user = models.User(**user.dict()) 
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return  new_user
