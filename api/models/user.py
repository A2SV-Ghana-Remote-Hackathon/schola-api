from sqlalchemy import Column, ForeignKey, Integer, String, text, Text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from database.db import Base
from enum import Enum
from sqlalchemy.orm import relationship, backref


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
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    posts = relationship("Post", back_populates="owner")
    comments = relationship("Comment", back_populates="user")


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    content = Column(String, nullable=False)
    post_image = Column(String)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    owner_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")


class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    event_date = Column(String)
    location = Column(String)
    image = Column(String)
    comments = relationship("Comment", back_populates="event", cascade="all, delete-orphan")


class Announcement(Base):
    __tablename__ = 'announcements'
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    image_url = Column(String)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User")


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"))
    event = relationship("Event", back_populates="comments", foreign_keys=[event_id])
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))
    post = relationship("Post", back_populates="comments", foreign_keys=[post_id])
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="comments")
    reply_to_comment_id = Column(Integer, ForeignKey("comments.id"))
    replies = relationship("Comment", backref="parent_comment", remote_side=[id])


class Like(Base):
    __tablename__ = "likes"
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    post_id = Column(
        Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)