from fastapi import FastAPI
from src.routes import auth, formula,user,category
from src.database import engine
from src.models.base import Base
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title='Formulas builder',
    description='FastApi formula builder Project',
    version='1.0.0',
    docs_url='/',
)
origins = [
    "http://localhost",
    "http://localhost:5173",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(formula.router, prefix="/formula", tags=["Formulas"])
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(category.router, prefix="/categories", tags=["Categories"])


@app.get("/")
def root():
    return {"message": "Custom Formula Sharing API"}
