from pydantic import BaseModel, EmailStr, Field, conint
from typing import List, Optional
from datetime import datetime


class Profile(BaseModel):
    id: int = Field(...)
    name: str = Field(...)
    email: EmailStr = Field(...)
    bio: str = Field(...)
    profile_image: Optional[str] = Field(...)
    username: str = Field(...)
    role: str = Field(...)

    class Config:
        orm_mode = True


class SignUp(BaseModel):
    name: str = Field(..., min_length=4)
    email: EmailStr = Field(...)
    bio: str = Field(...)
    profile_image: Optional[str] = Field(...)
    username: str = Field(...,min_length=4)
    password: str = Field(...,min_length=8)

    class Config:
        orm_mode = True


class Login(BaseModel):
    username: str = Field(...)
    password: str = Field(...)

    class Config:
        orm_mode = True

class CreatePost(BaseModel):
    content: str
    post_image: str

    class Config:
        orm_mode = True

class Comment(BaseModel):
    id: int
    content: str
    created_at: str
    owner: Profile
    profile_image: str

class PostResponse(BaseModel):
    id: int
    content: str
    profile_image: Optional[str]
    created_at: datetime
    owner: Profile
    comments: List[Comment]

    class Config:
        orm_mode = True

    
class CreateEvent(BaseModel):
    title: str
    description: str
    event_date: str
    image: Optional[str]
    location: str

    class Config:
        orm_mode = True


class EventResponse(CreateEvent):
    id: int

    class Config:
        orm_mode = True


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)

    class Config:
        orm_mode = True
        

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
