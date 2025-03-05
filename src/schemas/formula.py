from .base import OurBaseModel
from typing import Dict, Optional
from typing import List, Dict, Optional

class FormulaInputCreate(OurBaseModel):
    name: str
    symbol: str
    coefficient: float
    description: Optional[str] = None

class FormulaCreate(OurBaseModel):
    name: str
    description: str
    category_id: int
    inputs: List[FormulaInputCreate]

class FormulaOut(FormulaCreate):
    id: int
    usage_count: int