from sqlalchemy import Column, Integer, ForeignKey
from .base import Base

class Star(Base):
    __tablename__ = "stars"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    formula_id = Column(Integer, ForeignKey("formulas.id"))
