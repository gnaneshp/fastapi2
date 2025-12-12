from fastapi import FastAPI,Body,HTTPException,status,Response,Depends,APIRouter
from app import schemas
from sqlalchemy.orm import Session
from app.database import engine,get_db
from app import models
from typing import Annotated
from app import utils
from app.oauth2 import get_current_user

app=APIRouter(prefix="/users",tags=["Users"])

@app.post("/",status_code=201,response_model=schemas.UserOut)
def create_post(body:Annotated[schemas.User,Body()],session:Session = Depends(get_db),current_user =Depends(get_current_user)):
    body.password = utils.hash(body.password)
    new_user = models.User(**body.model_dump())
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    # cursor.execute(""" Insert into posts (title,content,published) values (%s,%s,%s) returning *""",(body.title,body.content,body.published) )
    # result = cursor.fetchone()
    # conn.commit()
    return new_user

@app.get("/{user_id}",response_model=schemas.UserOut)
def get_user(user_id:int,session:Annotated[Session,Depends(get_db)],current_user =Depends(get_current_user)):
    user = session.query(models.User).filter(models.User.id==user_id).first()
    return user