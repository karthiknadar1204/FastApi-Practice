from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint







class UserCreate(BaseModel):
    email:EmailStr
    password:str

class returnUser(BaseModel):
    id: int
    email: EmailStr
    created_at:datetime
    class Config:
        from_attributes = True
 

class userLogin(BaseModel):
    email:EmailStr
    password:str










# **** POST schemas start ****
class POST(BaseModel):
    title:str
    content:str
    published:bool=True


class returnPost(POST):
    title:str
    content:str
    published:bool=True
    id: int
    owner_id:int
    created_at:datetime
    owner:returnUser
    class Config:
        from_attributes = True 

#  **** POST schemas end ****








class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id:Optional[str]=None









class Vote(BaseModel):
    post_id:int
    dir:conint(le=1)
