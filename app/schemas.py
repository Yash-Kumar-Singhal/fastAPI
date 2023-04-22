
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, conint

class UserCreate(BaseModel):
    email:EmailStr 
    password:str

class UserResponse(BaseModel):
    id:int 
    email:EmailStr
    created_at:datetime

    class Config:
        orm_mode = True

class UserLogin(UserCreate):
    pass


class PostBase(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    content: str


class PostResponse(PostBase):
    # we are not sending id in the response
    # already inherited from PostBase
    # title: str
    # content: str
    # published: bool
    created_at: datetime
    user_id:int
    id:int
    user:UserResponse

    class Config:
        orm_mode = True

class PostVote(BaseModel):
    Post:PostResponse
    votes: int

    class Config:
        orm_mode = True




class TokenResponse(BaseModel):
    access_token:str
    token_type:str

    class Config:
        orm_mode = True

class TokenData(BaseModel):
    id:Optional[str]=None



class Vote(BaseModel):
    post_id:int 
    dir:conint(ge=0,le=1) # type: ignore
