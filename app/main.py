from fastapi import Depends,FastAPI, Response,status,HTTPException
# from fastapi.params import Body
# from pydantic import BaseModel
from passlib.context import CryptContext
# from typing import Optional,List
# from random import randrange
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time
# from sqlalchemy.orm import Session
from . import models,schemas,utils
from .database import engine,SessionLocal
from .routers import post,user,auth,vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware


pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
models.Base.metadata.create_all(bind=engine)

app=FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.include_router(post.postRouter)
app.include_router(user.userRouter)
app.include_router(auth.authRouter)
app.include_router(vote.voteRouter)

# ***********************POST CREATION START***************************


# class POST(BaseModel):
#     title:str
#     content:str
#     published:bool=True
    # rating: Optional[int]=None





# **************** PURE SQL-python WITHOUT ORM START ******************        

# while True:
#     try:
#         conn = psycopg2.connect(
#             host='localhost',
#             database='fastapi',
#             user='postgres',
#             password='guruji1*',
#             cursor_factory=RealDictCursor
#         )
#         cursor = conn.cursor()
#         print("Database connection was successful")
#         break
#     except Exception as error:
#         print("Database connection failed")
#         print("Error:", error)
#         time.sleep(10)

# my_posts=[
#     {"title":"karthik","content":"content of post 1","id":1},
#     {"title":"suresh","content":"content of post 2","id":2},
#     {"title":"Nadar","content":"content of post 3","id":3}
# ]

# @app.get("/")
# async def root():
#     return {"message": "Hello, welcome to my api!!!"}

    


# Get POSTS
# @app.get('/posts')
# async def get_posts():
#     cursor.execute("""SELECT * FROM posts""")   
#     posts=cursor.fetchall()
#     print(posts)
#     return {'data':posts}


# # Create new post
# @app.post('/posts')
# async def create_posts(post: POST):
#     cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
#                    (post.title, post.content, post.published))
#     new_post = cursor.fetchone()
#     conn.commit()
#     return {"data": new_post}



# # Get post by id
# @app.get('/posts/{id}')
# async def get_post(id: int):
#     cursor.execute("""SELECT * from posts where id=%s """,(str(id),))
#     post=cursor.fetchone()
#     if post is None:
#         raise HTTPException(status_code=404, detail=f"Post with ID {id} not found")
#     return {"post_detail": post}




# # Delete posts by id
# @app.delete('/posts/{id}')
# async def delete_post(id:int):
#     cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""",(str(id),))
#     deleted_post=cursor.fetchone()
#     conn.commit()

#     if deleted_post==None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post {id} does not exist")

#     return Response(status_code=status.HTTP_204_NO_CONTENT)


# # Update post
# @app.put('/posts/{id}')
# async def update_post(id:int,post:POST):
#     cursor.execute("""UPDATE posts SET title=%s ,content=%s, published=%s WHERE id=%s RETURNING *""",(post.title,post.content,post.published,str(id)))
#     updated_post=cursor.fetchone()
#     conn.commit()

#     if updated_post==None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} not found")

    # return {"data":updated_post}

# **************** PURE SQL-python WITHOUT ORM END ******************  
































# ***************** ORM sqlalchemy-python Start ************************
# @app.get('/sqlalchemy')
# async def test_posts(db: Session = Depends(get_db)):
#     posts=db.query(models.Post).all()
#     return {"data":posts}



# Get POSTS
# @app.get('/posts',response_model=List[schemas.returnPost])
# async def get_posts(db: Session = Depends(get_db)):
#     posts=db.query(models.Post).all()
#     return posts








# # Create new post
# @app.post('/posts', response_model=schemas.returnPost)
# async def create_posts(post:schemas.POST,db: Session = Depends(get_db)):
#     print(post.dict())
#     new_post=models.Post(**post.dict())
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)
#     return new_post









# # Get post by id
# @app.get('/posts/{id}',response_model=schemas.returnPost)
# async def get_post(id: int,db: Session = Depends(get_db)):
#     post=db.query(models.Post).filter(models.Post.id==id).first()
#     print(post)
#     if post is None:
#         raise HTTPException(status_code=404, detail=f"Post with ID {id} not found")
#     return post











# # Delete posts by id
# @app.delete('/posts/{id}')
# async def delete_post(id:int,db: Session = Depends(get_db)):
#     post=db.query(models.Post).filter(models.Post.id==id)

#     if post.first() == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post {id} does not exist")

#     post.delete(synchronize_session=False)
#     db.commit()
#     return Response(status_code=status.HTTP_204_NO_CONTENT)







# # Update post
# @app.put('/posts/{id}',response_model=schemas.returnPost)
# async def update_post(id: int, post: schemas.POST, db: Session = Depends(get_db)):
#     post_query = db.query(models.Post).filter(models.Post.id == id)
#     existing_post = post_query.first()

#     if existing_post is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} not found")

#     post_query.update(post.dict(), synchronize_session=False)
#     db.commit()
#     return post_query.first()
# ***************** ORM sqlalchemy-python End ************************


# ***********************POST CREATION END***************************
































# ********** USER AUTH START ************

# @app.post('/users', status_code=status.HTTP_201_CREATED,response_model=schemas.returnUser)
# def create_user(user:schemas.UserCreate,db: Session = Depends(get_db)):

#     hashed_password=pwd_context.hash(user.password)
#     user.password=hashed_password

#     new_user=models.User(**user.dict())
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user


# @app.get('/users/{id}',response_model=schemas.returnUser)
# def get_user(id:int,db: Session = Depends(get_db)):
#     user=db.query(models.User).filter(models.User.id==id).first()
#     if not user:
#         raise HTTPException(status_code=404,detail="User Not Found")

#     return user