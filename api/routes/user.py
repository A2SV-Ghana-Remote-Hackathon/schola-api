from fastapi import status, HTTPException, Depends, APIRouter
from api.schemas.user import SignUp, Profile
from database.db import get_db
from sqlalchemy.orm import Session
from utils.utils import hash_password
from api.models.user import User
from utils.oauth2 import get_current_user


user_router = APIRouter(prefix="/users", tags=["User"])

@user_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Profile)
def create_user(user: SignUp, db: Session = Depends(get_db)):
    user_data = db.query(User).filter(User.email == user.email).first()
    if user_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="user already exists")
    hashed_password = hash_password(user.password)
    user.password = hashed_password
    new_user = User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@user_router.get("/{id}", response_model=Profile)
async def get_profile(id: int, db: Session = Depends(get_db)):
    user_details = db.query(User).filter(User.id == id).first()
    if user_details:
        return user_details
    else:
        raise HTTPException(status_code=404)

@user_router.get("/profile/me", status_code=status.HTTP_200_OK, response_model=Profile)
def me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return current_user