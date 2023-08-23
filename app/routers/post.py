from .. import models,schemas,utils
from fastapi import FastAPI , HTTPException ,status,Depends,APIRouter
from ..database import  SessionLocal ,get_db
from sqlalchemy.orm import Session
from typing import List
from .. import oauth2 

router = APIRouter(
      prefix="/posts",
      tags= ['posts']
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.PostCreate,db: Session= Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts(title,content,published) VALUES(%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # con.commit()
    print(current_user)  
    new_post = models.Post(**post.model_dump()) 
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post


@router.get("/{id}",response_model=schemas.Post)
def get_post(id :int ,db : Session = Depends(get_db),current_user :int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts where id = %s""",(str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                      detail = f"post with id : {id} is not found"
        )
    return  post 

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id :int , db : Session = Depends(get_db),current_user :int = Depends(oauth2.get_current_user)):
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


@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int , updated_post :schemas.PostCreate, db : Session = Depends(get_db),current_user :int = Depends(oauth2.get_current_user)):
    
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
