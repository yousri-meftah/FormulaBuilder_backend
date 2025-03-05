from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from .base import Base

class FormulaInput(Base):
    __tablename__ = "formula_inputs"

    id = Column(Integer, primary_key=True, index=True)
    formula_id = Column(Integer, ForeignKey("formulas.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)  # Variable name (e.g., "Math")
    symbol = Column(String, nullable=False)  # Symbol (e.g., "x")
    coefficient = Column(Float, nullable=False, default=1.0)  # Coefficient (default 1.0)
    description = Column(String, nullable=True)  # Variable description (optional)

    formula = relationship("Formula", back_populates="inputs")
