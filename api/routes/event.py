from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Response, status, Form, UploadFile, File
from sqlalchemy.orm import Session
from api.models.user import Event, User, Comment
from api.schemas.user import CreateEvent, EventResponse, CreateComment, CommentResponse
from database.db import get_db
from utils.oauth2 import get_current_user
from utils.s3 import upload_file_to_s3


event_router = APIRouter(prefix="/events", tags=["Events"])

@event_router.post("/", status_code=status.HTTP_201_CREATED, response_model=EventResponse)
def create_event(
    title: str = Form(...),
    description: str = Form(...),
    event_date: str = Form(...),
    location: str = Form(...),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    image_url = None
    if image:
        image_url = upload_file_to_s3(image)

    event_data = CreateEvent(
        title=title,
        description=description,
        event_date=event_date,
        location=location,
        image=image_url
    )

    new_event = Event(**event_data.dict())
    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    response_event = EventResponse(
        id=new_event.id,
        title=new_event.title,
        description=new_event.description,
        event_date=new_event.event_date,
        location=new_event.location,
        image=new_event.image,
        comments=[]
    )

    return response_event

@event_router.get("/{event_id}", response_model=EventResponse)
def get_event(event_id: int, response: Response, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    
    response_event = EventResponse(
        id=event.id,
        title=event.title,
        description=event.description,
        event_date=event.event_date,
        location=event.location,
        image=event.image,
        comments=[]
    )

    return response_event

@event_router.get("/", response_model=List[EventResponse])
def get_all_events(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    events = db.query(Event).offset(skip).limit(limit).all()
    return events

@event_router.post("/{event_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_event_comment(comment: CreateComment, event_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    
    new_comment = Comment(content=comment.content, created_at=datetime.now(), event_id=event_id, user_id=current_user.id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

@event_router.get("/{event_id}/comments", response_model=List[CommentResponse], status_code=status.HTTP_200_OK)
def get_event_comments(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    
    comments = db.query(Comment).filter(Comment.event_id == event_id).all()
    return comments