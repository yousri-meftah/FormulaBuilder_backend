from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.schemas.formula import FormulaCreate, FormulaOut
from src.database import get_db
from src.models.formula import Formula

router = APIRouter()

@router.post("/", response_model=FormulaOut)
def create_formula(formula: FormulaCreate, db: Session = Depends(get_db)):
    db_formula = Formula(**formula.dict())
    db.add(db_formula)
    db.commit()
    db.refresh(db_formula)
    return db_formula
