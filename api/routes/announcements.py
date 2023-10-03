from typing import List
from fastapi import APIRouter, Depends, status
from api.models.user import Announcement, User
from api.schemas.user import CreateAnnouncement, AnnouncementResponse
from database.db import get_db
from utils.oauth2 import get_current_user
from sqlalchemy.orm import Session


announcement_router = APIRouter(prefix="/announcements", tags=["Announcements"])

@announcement_router.post("/", status_code=status.HTTP_201_CREATED, response_model=AnnouncementResponse)
def create_announcement(announcement_data: CreateAnnouncement, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_announcement = Announcement(owner_id=current_user.id, **announcement_data.dict())

    db.add(new_announcement)
    db.commit()
    db.refresh(new_announcement)

    return new_announcement

@announcement_router.get("/", response_model=List[AnnouncementResponse])
def get_all_announcements(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    announcements = db.query(Announcement).offset(skip).limit(limit).all()
    return announcements