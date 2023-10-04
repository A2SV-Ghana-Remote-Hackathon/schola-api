from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, Form, HTTPException, Response, UploadFile, status, File
from sqlalchemy.orm import Session
from api.models.user import Post, User, Comment
from api.schemas.user import CreatePost, PostResponse, CreateComment, CommentResponse
from database.db import get_db
from utils.oauth2 import get_current_user
from utils.s3 import upload_file_to_s3


post_router = APIRouter(prefix="/posts", tags=["Post"])

@post_router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(content: str = Form(...), file: UploadFile = File(None), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if file:
        image_url = upload_file_to_s3(file)
    else:
        image_url = None

    new_post = Post(content=content, post_image=image_url, created_at=datetime.now(), owner=current_user)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@post_router.get("/{post_id}/", response_model=PostResponse)
def get_post(post_id: int, response: Response, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@post_router.get("/", response_model=List[PostResponse])
def get_all_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    posts = db.query(Post).offset(skip).limit(limit).all()
    return posts

@post_router.post("/{post_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_user_post_comment(comment: CreateComment, post_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    new_comment = Comment(content=comment.content, post_id=post_id, user_id=current_user.id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

@post_router.get("/{post_id}/comments", response_model=list[CommentResponse], status_code=status.HTTP_200_OK)
def get_user_post_comments(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    comments = db.query(Comment).filter(Comment.post_id == post_id).all()
    return comments