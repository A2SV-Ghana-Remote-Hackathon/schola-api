from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from api.models.user import Event, User
from api.schemas.user import CreateEvent, EventResponse
from database.db import get_db
from utils.oauth2 import get_current_user


event_router = APIRouter(prefix="/events", tags=["Events"])

@event_router.post("/", status_code=status.HTTP_201_CREATED, response_model=EventResponse)
def create_event(event_data: CreateEvent, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
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
        image=new_event.image
    )

    return response_event

@event_router.get("/{event_id}/", response_model=EventResponse)
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



