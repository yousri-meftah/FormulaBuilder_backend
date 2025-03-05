from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from .base import Base

class Formula(Base):
    __tablename__ = "formulas"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    is_public = Column(Boolean, default=False)
    expression = Column(String , nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    usage_count = Column(Integer, default=0)  # Track how many times used

    creator = relationship("User", back_populates="formulas")
    category = relationship("Category", back_populates="formulas")
    inputs = relationship("FormulaInput", back_populates="formula", cascade="all, delete") 

