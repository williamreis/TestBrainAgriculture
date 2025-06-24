from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship
from .database import Base

class Safra(Base):
    __tablename__ = "safras"
    id = Column(Integer, primary_key=True, index=True)
    ano = Column(Integer, nullable=False)
    culturas = relationship("PropriedadeSafraCultura", back_populates="safra") 