from fastapi import FastAPI,Body,HTTPException,status,Response,Depends,APIRouter
from app import schemas
from sqlalchemy.orm import Session
from app.database import engine,get_db
from app import models
from typing import Annotated
from app import utils
from app.oauth2 import get_current_user

app=APIRouter(prefix="/vote",tags=["Vote"])

@app.post("/")
def add_remove_vote(body:Annotated[schemas.Vote,Body()],session:Session=Depends(get_db),current_user =Depends(get_current_user)):
    if body.direction==1:
        post = session.query(models.Post).filter(models.Post.id==body.post_id).first()
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {body.post_id} does not exist")
        vote_query = session.query(models.Vote).filter(models.Vote.post_id==body.post_id,models.Vote.user_id==current_user.id)
        found_vote = vote_query.first()
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="user has already voted on the post")
        vote = models.Vote(post_id=body.post_id,user_id=current_user.id)
        session.add(vote)
        session.commit()
        return {"message":"successfully added vote"}
    else:
        vote_query = session.query(models.Vote).filter(models.Vote.post_id==body.post_id,models.Vote.user_id==current_user.id)
        found_vote = vote_query.first()
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="vote does not exist")
        vote_query.delete(synchronize_session=False)
        session.commit()
        return {"message":"successfully deleted vote"}