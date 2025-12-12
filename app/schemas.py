from pydantic import BaseModel,EmailStr
from datetime import datetime
from pydantic.types import conint
class Post(BaseModel):
    title:str
    content:str
    published:bool=True
class UserOut(BaseModel):
    email:EmailStr
    id:int
    created_at:datetime
    class Config:
        from_attributes=True

class PostResponse(Post):
    id:int
    created_at:datetime
    owner_id:int
    owner:UserOut
    class Config:
        from_attributes=True

class PostOut(BaseModel):
    Post:PostResponse
    Votes:int
    class Config:
        from_attributes=True

class User(BaseModel):
    email:EmailStr
    password:str


class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:int

class Vote(BaseModel):
    post_id:int
    direction:conint(ge=0,le=1)