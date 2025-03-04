from pydantic import BaseModel
from typing import Dict, Optional

class FormulaCreate(BaseModel):
    name: str
    variables: Dict[str, float]
    logic: str
    is_public: Optional[bool] = False

class FormulaOut(FormulaCreate):
    id: int
    creator_id: int

    class Config:
        orm_mode = True
