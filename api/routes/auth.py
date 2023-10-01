from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database.db import get_db
from api.schemas.user import Token
from api.models.user import User
from utils.oauth2 import create_access_token
from utils.utils import verify_password


auth_router = APIRouter(tags=["Authentication"])


@auth_router.post("/login", status_code=status.HTTP_200_OK, response_model=Token)
def login_user(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = (
        db.query(User)
        .filter(User.email == user_credentials.username)
        .first()
    )

    if not user or not verify_password(user_credentials.password, user.password):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=f"invalid credentials")

    access_token = create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}