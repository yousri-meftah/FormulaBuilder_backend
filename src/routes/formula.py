from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.schemas.formula import FormulaCreate, FormulaOut
from src.models import FormulaInput
from src.database import get_db
from src.models.formula import Formula
from typing import List
from sqlalchemy import desc
from ..auth import get_current_user
from src import models
from typing import Dict
from src.utils import safe_eval
router = APIRouter()

@router.post("/", response_model=FormulaOut)
def create_formula(formula: FormulaCreate, db: Session = Depends(get_db),User: models.User = Depends(get_current_user)):
    db_formula = Formula(
        creator_id = User.id,
        name=formula.name,
        description=formula.description,
        category_id=formula.category_id,
    )
    db.add(db_formula)
    db.flush()
    for input_data in formula.inputs:
        db_input = FormulaInput(
            formula_id=db_formula.id,
            name=input_data.name,
            symbol=input_data.symbol,
            coefficient=input_data.coefficient,
            description=input_data.description,
        )
        db.add(db_input)
    
    
    db.commit()
    return db_formula

@router.get("/", response_model=List[FormulaOut])
def get_formulas(db: Session = Depends(get_db)):
    formulas = db.query(Formula).all()
    
    for formula in formulas:
        formula.inputs = db.query(FormulaInput).filter(FormulaInput.formula_id == formula.id).all()
    
    return formulas



@router.get("/top-rated", response_model=List[FormulaOut])
def get_top_rated_formulas(db: Session = Depends(get_db)):
    return  db.query(Formula).order_by(desc(Formula.id)).limit(3).all()

@router.get("/popular", response_model=List[FormulaOut])
def get_popular_formulas(db: Session = Depends(get_db)):
    return db.query(Formula).order_by(desc(Formula.usage_count)).limit(3).all()



@router.post("/{formula_id}/execute")
def execute_formula(formula_id: int, inputs: Dict[str, float], db: Session = Depends(get_db)):
    # Retrieve formula
    formula = db.query(Formula).filter(Formula.id == formula_id).first()
    if not formula:
        raise HTTPException(status_code=404, detail="Formula not found")

    # Retrieve related inputs
    formula_inputs = db.query(FormulaInput).filter(FormulaInput.formula_id == formula_id).all()

    if not formula_inputs:
        raise HTTPException(status_code=400, detail="No inputs found for this formula")

    # Compute sum of coefficients and divide by total coefficients
    total_sum = sum(input.coefficient for input in formula_inputs)
    total_count = len(formula_inputs)

    if total_count == 0:
        raise HTTPException(status_code=400, detail="Invalid formula: no coefficients")

    result = total_sum / total_count

    # Increment usage count
    formula.usage_count += 1
    db.commit()

    return {"formula_id": formula.id, "result": result}


@router.get("/{formula_id}", response_model=FormulaOut)
def get_formula(formula_id: int, db: Session = Depends(get_db)):
    formula = db.query(Formula).filter(Formula.id == formula_id).first()
    if not formula:
        raise HTTPException(status_code=404, detail="Formula not found")
    formula.inputs = db.query(FormulaInput).filter(FormulaInput.formula_id == formula_id).all()
    return formula