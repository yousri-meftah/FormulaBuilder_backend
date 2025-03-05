from typing import Dict
from fastapi import HTTPException


def safe_eval(expression: str, variables: Dict[str, float]) -> float:
    allowed_globals = {"__builtins__": {}, "sqrt": lambda x: x ** 0.5}
    try:
        return eval(expression, allowed_globals, variables)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error in calculation: {str(e)}")
