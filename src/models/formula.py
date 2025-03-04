from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from .base import Base

class Formula(Base):
    __tablename__ = "formulas"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    variables = Column(JSON) 
    logic = Column(String)    
    is_public = Column(Boolean, default=False)
    creator_id = Column(Integer, ForeignKey("users.id"))

    creator = relationship("User", back_populates="formulas")
