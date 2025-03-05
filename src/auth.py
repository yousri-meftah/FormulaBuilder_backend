from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta, datetime
from fastapi import Depends, HTTPException
from starlette.authentication import AuthCredentials, UnauthenticatedUser
from jose import jwt, JWTError
from .database import get_db
from sqlalchemy.orm import Session
from .config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
SPECIAL_CHARACTERS = ["@", "#", "$", "%", "=", ":", "?", ".", "/", "|", "~", ">"]


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def is_password_strong_enough(password: str) -> bool:
    if len(password) < 8:
        return False

    if not any(char.isupper() for char in password):
        return False

    if not any(char.islower() for char in password):
        return False

    if not any(char.isdigit() for char in password):
        return False

    if not any(char in SPECIAL_CHARACTERS for char in password):
        return False

    return True


async def create_access_token(data: dict, expiry: timedelta):
    payload = data.copy()
    expire_in = datetime.now() + expiry
    payload.update({"exp": expire_in})
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def get_token_payload(token: str):

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None


# i get rid of , db=None inside the below paramter
def get_current_user(token: str = Depends(oauth2_scheme), db : Session = Depends(get_db)):
    payload = get_token_payload(token)
    if not payload or type(payload) is not dict:
        return None

    user_id = payload.get("id", None)
    if not user_id:
        return None

    id = int(user_id)
    from .routes.user import get_user
    user = get_user(id,db)

    return user


class JWTAuth:

    async def authenticate(self, conn):
        guest = AuthCredentials(["unauthenticated"]), UnauthenticatedUser()

        if "authorization" not in conn.headers:
            return guest

        token = conn.headers.get("authorization").split(" ")[1]  # Bearer token_hash
        if not token:
            return guest

        user = get_current_user(token=token)
        if not user:
            return guest

        return AuthCredentials("authenticated"), user
