import jwt
from datetime import datetime,timedelta
from fastapi import HTTPException,status,Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import engine,get_db
from app import models
from app import schemas
from app.config import settings
oauth2 = OAuth2PasswordBearer(tokenUrl="login")
SECRET = settings.secret_key
EXPIRE = settings.access_token_expire_minutes
ALGORITHM = settings.algorithm

def create_access_token(body:dict):
    body_copy=body.copy()
    body_copy['expire']=(datetime.now()+timedelta(minutes=EXPIRE)).timestamp()
    encoded_token = jwt.encode(body_copy,SECRET,algorithm=ALGORITHM)
    return encoded_token

def get_current_user(token:str = Depends(oauth2),session:Session=Depends(get_db)):
    credentials_exception=HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="unable to validate credentials")
    token_data = validate_access_token(token,credentials_exception)
    user = session.query(models.User).filter(models.User.id==token_data.id).first()
    return user

def validate_access_token(token:str,credentials_exception:HTTPException):
    try:
        body = jwt.decode(token,SECRET,algorithms=[ALGORITHM])
        print(body)
        user_id= body.get("user_id")
        if user_id is None:
           raise credentials_exception
        token_data = schemas.TokenData(id=user_id)
    except Exception as e:
        print(e,"1")
        raise credentials_exception
    return token_data
    

 

    