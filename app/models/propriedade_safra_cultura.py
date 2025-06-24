from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class PropriedadeSafraCultura(Base):
    __tablename__ = "propriedade_safra_cultura"
    id = Column(Integer, primary_key=True, index=True)
    propriedade_id = Column(Integer, ForeignKey("propriedades.id"), nullable=False)
    safra_id = Column(Integer, ForeignKey("safras.id"), nullable=False)
    cultura_id = Column(Integer, ForeignKey("culturas.id"), nullable=False)

    propriedade = relationship("Propriedade", back_populates="culturas")
    safra = relationship("Safra", back_populates="culturas")
    cultura = relationship("Cultura", back_populates="propriedades") 