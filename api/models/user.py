from sqlalchemy import Column, Integer, String, text, Text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from database.db import Base
from enum import Enum


class UserRole(Enum):
    USER = 'user'
    ADMIN = 'admin'


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    bio = Column(Text)
    profile_image = Column(String)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(String, default=UserRole.USER.value)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))