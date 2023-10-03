from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.db import get_db
from api.models.user import Community, User
from api.schemas.user import CreateCommunity, CommunityResponse
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