from pydantic import BaseModel, EmailStr
from .base import OurBaseModel
class UserCreate(OurBaseModel):
    username: str
    email: EmailStr
    password: str

class UserOut(OurBaseModel):
    id: int
    username: str
    email: EmailStr
