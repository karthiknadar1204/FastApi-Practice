from fastapi import Depends,FastAPI, Response,status,HTTPException,APIRouter
from sqlalchemy.orm import Session
from typing import Optional,List
from .. import models,schemas,oauth2
from ..database import engine,SessionLocal

postRouter=APIRouter(
    prefix='/posts',
    tags=['posts']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()








# @app.get('/sqlalchemy')
# async def test_posts(db: Session = Depends(get_db)):
#     posts=db.query(models.Post).all()
#     return {"data":posts}












# Get POSTS
@postRouter.get('/', response_model=List[schemas.returnPost])
async def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, search: Optional[str] = ""):
    print(limit)
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).all()


    return posts















# Create new post
@postRouter.post('/', response_model=schemas.returnPost)
async def create_posts(post:schemas.POST,db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    print(post.dict())
    new_post=models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post















# Get post by id
@postRouter.get('/{id}',response_model=schemas.returnPost)
async def get_post(id: int,db: Session = Depends(get_db)):
    post=db.query(models.Post).filter(models.Post.id==id).first()
    print(post)
    if post is None:
        raise HTTPException(status_code=404, detail=f"Post with ID {id} not found")
    return post















# Delete posts by id
@postRouter.delete('/{id}')
async def delete_post(id:int,db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post {id} does not exist")

    if post.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)











# Update post
@postRouter.put('/posts/{id}',response_model=schemas.returnPost)
async def update_post(id: int, post: schemas.POST, db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    existing_post = post_query.first()

    if existing_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} not found")
    
    if existing_post.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform action")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()








