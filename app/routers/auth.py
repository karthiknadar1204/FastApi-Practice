from fastapi import Depends,FastAPI, Response,status,HTTPException,APIRouter
from sqlalchemy.orm import Session
from typing import Optional,List
from .. import models,schemas,utils,oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import engine,SessionLocal

authRouter=APIRouter(tags=["Authentication"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@authRouter.post('/login',response_model=schemas.Token)
async def login(user_credentials: OAuth2PasswordRequestForm =Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    
    access_token=oauth2.create_access_token(data={"user_id":user.id})

    return {"access_token":access_token,"token_type":"bearer"}







