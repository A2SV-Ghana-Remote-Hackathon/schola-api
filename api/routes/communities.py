from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from database.db import get_db
from api.models.user import Community, Post, User, Comment
from api.schemas.user import CreateCommunity, CommunityResponse, PostResponse, CreatePost, CreateComment, CommentResponse
from utils.oauth2 import get_current_user

community_router = APIRouter(prefix="/communities", tags=["Communities"])

@community_router.post("/", response_model=CommunityResponse)
def create_community(community_create: CreateCommunity, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    community = db.query(Community).filter(Community.name == community_create.name).first()
    if community:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="community already exists")
    new_community = Community(owner_id=current_user.id, **community_create.dict(exclude={"owner"}))
    db.add(new_community)
    db.commit()
    db.refresh(new_community)

    return new_community

@community_router.post("/join/{community_id}", status_code=status.HTTP_202_ACCEPTED)
def join_community(community_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    community = db.query(Community).filter(Community.id == community_id).first()
    if community is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Community not found")
    
    if community in current_user.joined_communities:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is already a member of this community")
    
    community.members.append(current_user)
    db.commit()
    db.refresh(community)

    return {"message": "User successfully joined the community"}
    

@community_router.get("/{community_id}", response_model=CommunityResponse)
def get_community(community_id: int, db: Session = Depends(get_db)):
    community = db.query(Community).filter(Community.id == community_id).first()
    if community is None:
        raise HTTPException(status_code=404, detail="Community not found")
    
    return community

@community_router.get("/", response_model=List[CommunityResponse])
def get_all_communities(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    communities = db.query(Community).offset(skip).limit(limit).all()
    return communities

@community_router.get("/my_communities/", response_model=List[CommunityResponse])
def get_user_communities(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_communities = current_user.joined_communities
    return user_communities

def is_user_member_of_community(community: Community, user: User) -> bool:
    return user in community.members

@community_router.post("/{community_id}/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_community_post(community_id: int, post: CreatePost, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    community = db.query(Community).filter(Community.id == community_id).first()
    if not community:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Community not found")

    if not is_user_member_of_community(community, current_user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not a member of this community")

    new_post = Post(content=post.content, post_image=post.post_image, created_at=datetime.now(), owner=current_user, community_id=community_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@community_router.get("/{community_id}/posts/{post_id}", response_model=PostResponse)
def get_community_post(community_id: int, post_id: int, db: Session = Depends(get_db)):
    community = db.query(Community).filter(Community.id == community_id).first()
    if not community:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Community not found")
    post = db.query(Post).filter(Post.id == post_id, Post.community_id == community_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found in the community")
    return post

@community_router.post("/{community_id}/posts/{post_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_community_post_comment(community_id: int, comment: CreateComment, post_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    community = db.query(Community).filter(Community.id == community_id).first()
    if not community:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Community not found")
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    new_comment = Comment(content=comment.content, created_at=datetime.now(), post_id=post_id, user_id=current_user.id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

@community_router.get("/{community_id}/posts/{post_id}/comments", response_model=list[CommentResponse], status_code=status.HTTP_200_OK)
def get_community_post_comments(community_id: int, post_id: int, db: Session = Depends(get_db)):
    community = db.query(Community).filter(Community.id == community_id).first()
    if not community:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Community not found")
    post = db.query(Post).filter(Post.id == post_id, Post.community_id == community_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    comments = db.query(Comment).filter(Comment.post_id == post_id).all()
    return comments

@community_router.get("/all/search", response_model=List[CommunityResponse])
def search_communities(name: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    communities = db.query(Community).filter(func.lower(Community.name).contains(func.lower(name))).all()
    if not communities:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No communities found")
    return communities