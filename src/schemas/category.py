from pydantic import BaseModel

class CategoryCreate(BaseModel):
    name: str

class CategoryOut(CategoryCreate):
    id: int
