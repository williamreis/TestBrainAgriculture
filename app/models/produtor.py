from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .database import Base


class ProdutorRural(Base):
    __tablename__ = "produtores"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cpf_cnpj = Column(String, unique=True, nullable=False, index=True)
    propriedades = relationship("Propriedade", back_populates="produtor")
