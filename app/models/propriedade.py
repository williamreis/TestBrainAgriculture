from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Propriedade(Base):
    __tablename__ = "propriedades"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cidade = Column(String, nullable=False)
    estado = Column(String, nullable=False)
    area_total = Column(Float, nullable=False)
    area_agricultavel = Column(Float, nullable=False)
    area_vegetacao = Column(Float, nullable=False)
    produtor_id = Column(Integer, ForeignKey("produtores.id"), nullable=False)
    produtor = relationship("ProdutorRural", back_populates="propriedades")
    culturas = relationship("PropriedadeSafraCultura", back_populates="propriedade") 