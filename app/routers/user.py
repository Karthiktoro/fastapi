from .. import models,schemas,utils
from fastapi import FastAPI , HTTPException ,status,Depends,APIRouter
from ..database import  SessionLocal ,get_db
from sqlalchemy.orm import Session


router = APIRouter(
      prefix="/users",
      tags= ['users']

)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate , db: Session= Depends(get_db)):


        hashed_password = utils.hash(user.password)  #hash the password user.password
        user.password = hashed_password
        new_user = models.User(**user.dict()) 
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return  new_user

@router.get("/{id}")
def get_user(id : int,db: Session= Depends(get_db)):
    user = db.query(models.User).filter(models.User.id== id).first()
    if not user:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                              detail=f"user with id : {id} not found") 
    return user

@router.get("/")
def get_user(db: Session= Depends(get_db)):
    user = db.query(models.User).all()
    return user