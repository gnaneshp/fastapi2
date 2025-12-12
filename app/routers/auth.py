from fastapi import FastAPI,Body,HTTPException,status,Depends,APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from app import schemas
from sqlalchemy.orm import Session
from app.database import engine,get_db
from app import models
from typing import Annotated
from app import utils
from app import oauth2


app=APIRouter(tags=["Authentication"])

@app.post("/login",response_model=schemas.Token)
def login(body:Annotated[OAuth2PasswordRequestForm,Depends()],session:Session=Depends(get_db)):
    user = session.query(models.User).filter(models.User.email==body.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
    if not utils.verify(body.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
    encoded_token = oauth2.create_access_token({"user_id":user.id})
    return {"access_token":encoded_token,"token_type":"Bearer"}