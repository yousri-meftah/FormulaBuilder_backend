from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    formulas = relationship("Formula", back_populates="category")
