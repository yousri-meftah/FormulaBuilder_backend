from fastapi import FastAPI
from src.routes import auth, formula,user
from src.database import engine
from src.models.base import Base

app = FastAPI()


app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(formula.router, prefix="/formula", tags=["Formulas"])
app.include_router(user.router, prefix="/users", tags=["Users"])

@app.get("/")
def root():
    return {"message": "Custom Formula Sharing API"}
