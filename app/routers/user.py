from fastapi import Depends,FastAPI, Response,status,HTTPException,APIRouter
from sqlalchemy.orm import Session
from .. import models,schemas,utils
from ..database import engine,SessionLocal

userRouter=APIRouter(
    prefix='/users',
    tags=['users']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@userRouter.post('/', status_code=status.HTTP_201_CREATED,response_model=schemas.returnUser)
def create_user(user:schemas.UserCreate,db: Session = Depends(get_db)):

    hashed_password=utils.hash(user.password)
    user.password=hashed_password

    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@userRouter.get('/{id}',response_model=schemas.returnUser)
def get_user(id:int,db: Session = Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=404,detail="User Not Found")

    return user