from utils.oauth2 import get_current_user
from fastapi import Depends, HTTPException, status
from api.schemas.user import Profile
from api.models.user import UserRole


def is_authenticated(user: Profile = Depends(get_current_user)):
	return user

def is_admin(user: Profile = Depends(is_authenticated)):
	if user.role.name != UserRole.ADMIN.value:
		raise HTTPException(status.HTTP_401_UNAUTHORIZED)

	return user