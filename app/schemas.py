from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional
from pydantic.types import conint


class User(BaseModel):
    name: str
    email: EmailStr
    password: str


class CurrentUser(User):
    id: int


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class ResponseUser(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        orm_mode = True


# Base Post model
class Post(BaseModel):
    title: str
    content: str
    published: bool = True


class ResponsePost(Post):
    id: int
    owner_id: int
    created_at: datetime
    owner: ResponseUser

    class Config:
        orm_mode = True


class PostVote(BaseModel):
    Post: ResponsePost
    votes: int

    class Config:
        orm_mode = True


class CreatePost(Post):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
