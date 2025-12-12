from fastapi import Body,HTTPException,status,Response,Depends,APIRouter,Query
from app import schemas
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import engine,get_db
from app import models
from typing import Annotated
from app.oauth2 import get_current_user


app=APIRouter(prefix="/posts",tags=["Posts"])

@app.get("/",response_model=list[schemas.PostOut])
def get_posts(search:Annotated[str,Query()]="",session:Session = Depends(get_db),current_user =Depends(get_current_user),limit:Annotated[int,Query()]=10,skip:Annotated[int,Query()]=0):
    results2 = session.query(models.Post,func.count(models.Vote.post_id).label("Votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit=limit).offset(offset=skip).all()
    # print(results2)
    # cursor.execute("""select * from posts""")
    # posts = cursor.fetchall()
    return results2
@app.post("/",status_code=201,response_model=schemas.PostResponse)
def create_post(body:Annotated[schemas.Post,Body()],session:Session = Depends(get_db),current_user =Depends(get_current_user)):
    print('current_user',current_user)
    new_post = models.Post(owner_id=current_user.id,**body.model_dump())
    print('new_post',new_post)
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    # cursor.execute(""" Insert into posts (title,content,published) values (%s,%s,%s) returning *""",(body.title,body.content,body.published) )
    # result = cursor.fetchone()
    # conn.commit()
    return new_post

@app.get("/{post_id}",response_model=schemas.PostResponse)
def get_post(post_id:int,session:Session=Depends(get_db),current_user =Depends(get_current_user)):
    result = session.query(models.Post).filter(models.Post.id==post_id).first()

    # cursor.execute("""select * from posts where "Id" = %s""",(post_id,))
    # result = cursor.fetchone()
    if not result:
        raise HTTPException(status_code=404,detail=f"post with {post_id} does not exist")
    return result

@app.delete("/{post_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id:int,session:Session=Depends(get_db),current_user =Depends(get_current_user)):
    result_query = session.query(models.Post).filter(models.Post.id==post_id)
    # cursor.execute("""delete from posts where posts."Id" = %s returning *""",(post_id,))
    # deleted_post = cursor.fetchone()
    if result_query.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {post_id} does not exist")
    if result_query.first().owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"not authorised to perform required action")
    result_query.delete(synchronize_session=False)
    session.commit()
    # conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/{post_id}",response_model=schemas.PostResponse)
def update_post(post_id:int,body:Annotated[schemas.Post,Body()],session:Session=Depends(get_db),current_user =Depends(get_current_user)):
    result_query = session.query(models.Post).filter(models.Post.id==post_id)

    # cursor.execute("""update posts set title= %s,"content" = %s,published = %s where posts."Id"= %s returning *""",(post.title,post.content,post.published,post_id))
    # updated_post =cursor.fetchone()
    # conn.commit()
    if result_query.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {post_id} does not exist")
    # updated_post = models.Post(**body.model_dump())
    if result_query.first().owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"not authorised to perform required action")
    
    result_query.update(body.model_dump(),synchronize_session=False)
    session.commit()
    return result_query.first()
