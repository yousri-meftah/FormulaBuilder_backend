from fastapi import APIRouter, status, Depends, Header, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from ..controllers.auth import get_token
from ..schemas.base import OurBaseModelOut
from ..schemas.user import UserOut
from src import models 
from ..auth import get_current_user
from src.auth import get_password_hash
from src.models import User
from src.schemas import user


router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.post("/register", response_model=UserOut)
def register(user: user.UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    print(user)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    return db_user



@router.post("/login", status_code=status.HTTP_200_OK)
async def authenticate_user(
    data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    return await get_token(data=data, db=db)



# @router.post("/reset-password")
# def reset(
#     reset_data: resetPassword,
#     db: Session = Depends(get_db)
# ):
#     if reset_data.password != reset_data.confirmPass:
#         return OurBaseModelOut(
#             status=status.HTTP_400_BAD_REQUEST,
#             message="Passwords do not match."
#         )

#     try:
#         reset_password(db, reset_data.code, reset_data.password)
#         return OurBaseModelOut(
#             status=status.HTTP_200_OK,
#             message="Password reset successfully.",
#         )
#     except HTTPException as e:
#         return OurBaseModelOut(
#             status=e.status_code,
#             message=e.detail
#         )
#     except Exception as e:
#         return OurBaseModelOut(
#             status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             message="An error occurred during password reset."
#         )


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=UserOut
)
def get_user_detail(User: models.User = Depends(get_current_user)):
    if User is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    account_status = User.status.name
    roles = User.Employee_roles
    employee_fields = User.__dict__
    employee_fields.pop('status')
    employee_fields.pop('password')
    return UserOut(
        **employee_fields,
        account_status=account_status,
        roles=[role.role.name for role in roles],
        status = status.HTTP_200_OK,
        message = "User found."
    )