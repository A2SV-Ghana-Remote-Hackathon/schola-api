from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from api.models.user import Post
from api.schemas.user import CreatePost, PostResponse
from database.db import get_db
from utils.oauth2 import get_current_user

post_router = APIRouter(prefix="/posts", tags=["Post"])

@post_router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post: CreatePost, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    new_post = Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    created_at_str = new_post.created_at.strftime('%Y-%m-%d %H:%M:%S')

    # Directly use PostResponse model for the response
    response_post = PostResponse.from_orm(new_post)
    response_post.created_at = created_at_str 

    return JSONResponse(content=response_post.dict())

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
