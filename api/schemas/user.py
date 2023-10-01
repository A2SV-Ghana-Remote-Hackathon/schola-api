from pydantic import BaseModel, EmailStr, Field
from typing import Optional


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

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
