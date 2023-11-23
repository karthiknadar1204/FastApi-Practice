from fastapi import Depends,FastAPI, Response,status,HTTPException,APIRouter
from sqlalchemy.orm import Session
from typing import Optional,List
from .. import models,schemas,oauth2
from ..database import engine,SessionLocal

voteRouter=APIRouter(
    prefix='/vote',
    tags=['votes']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@voteRouter.post("/",status_code=status.HTTP_201_CREATED)
async def vote(vote:schemas.Vote,db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):

    vote_query=db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,models.Vote.user_id==current_user.id)
    found_vote=vote_query.first()

    if vote.dir==1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        new_vote=models.Vote(post_id=vote.post_id,user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"You have successfully up-voted the post"}

    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"You have successfully down-voted the post"}
