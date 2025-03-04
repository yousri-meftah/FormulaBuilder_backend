from datetime import timedelta
from sqlalchemy.orm import Session
from ..models import User as UserModel
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from ..schemas.auth import TokenResponse
from ..auth import get_password_hash  as hash_password,create_access_token,verify_password
from ..config import Settings


async def get_token(data: OAuth2PasswordRequestForm, db: Session):
    user = db.query(UserModel).filter(UserModel.email == data.username).first()
    if not user :
        raise HTTPException(
            status_code=400,
            detail="Email is not registered with us.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    password = hash_password(data.password)
    if not verify_password(data.password , user.password) :
        raise HTTPException(
            status_code=400,
            detail="Invalid Login Credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return await _get_user_token(user=user)





async def _get_user_token(user: UserModel, refresh_token=None):
    payload = {"id": str(user.id)}
    access_token_expiry = timedelta(minutes=Settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(payload, access_token_expiry)
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=access_token_expiry.seconds,  # in seconds
    )