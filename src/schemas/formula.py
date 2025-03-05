from .base import OurBaseModel
from typing import Dict, Optional

class FormulaCreate(OurBaseModel):
    name: str
    variables: Dict[str, float]
    logic: str
    is_public: Optional[bool] = False

class FormulaOut(FormulaCreate):
    id: int
    creator_id: int
