from pydantic import BaseModel, EmailStr, Field, conint
from typing import List, Optional
from datetime import datetime


class Profile(BaseModel):
    id: int = Field(...)
    name: str = Field(...)
    email: EmailStr = Field(...)
    bio: str = Field(...)
    profile_image: Optional[str] = Field(None)
    username: str = Field(...)
    role: str = Field(...)

    class Config:
        from_attributes = True


class SignUp(BaseModel):
    name: str = Field(..., min_length=4)
    email: EmailStr = Field(...)
    bio: str = Field(...)
    profile_image: Optional[str] = Field(None)
    username: str = Field(...,min_length=4)
    password: str = Field(...,min_length=8) 

    class Config:
        from_attributes = True


class Login(BaseModel):
    username: str = Field(...)
    password: str = Field(...)

    class Config:
        from_attributes = True

    
class CreateComment(BaseModel):
    content: str

    class Config:
        from_attributes = True


class CommentResponse(BaseModel):
    id: int
    content: str
    created_at: str
    owner: Profile
    

class CreatePost(BaseModel):
    content: str
    post_image: Optional[str] = Field(None)
    community_id: Optional[int]

    class Config:
        from_attributes = True


class PostResponse(BaseModel):
    id: int
    content: str
    post_image: Optional[str] = Field(None)
    created_at: str
    owner: Profile
    comments: List[CommentResponse]

    class Config:
        from_attributes = True

    
class CreateEvent(BaseModel):
    title: str
    description: str
    event_date: str
    image: Optional[str] = Field(None)
    location: str

    class Config:
        from_attributes = True


class EventResponse(CreateEvent):
    id: int

    class Config:
        from_attributes = True


class CreateAnnouncement(BaseModel):
    content: str

    class Config:
        from_attributes = True


class AnnouncementResponse(BaseModel):
    id: int
    content: str
    created_at: datetime
    updated_at: datetime
    owner: Profile

    class Config:
        from_attributes = True


class CreatePost(BaseModel):
    content: str
    post_image: Optional[str] = Field(None)

    class Config:
        from_attributes = True


class PostResponse(BaseModel):
    id: int
    content: str
    post_image: Optional[str] = Field(None)

    class Config:
        from_attributes = True


class CreateCommunity(BaseModel):
    name: str
    description: str

    class Config:
        from_attributes = True


class CommunityResponse(BaseModel):
    id: int
    name: str
    description: str
    posts: List[PostResponse]
    owner: Profile

    class Config:
        from_attributes = True


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)

    class Config:
        from_attributes = True
        

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None
