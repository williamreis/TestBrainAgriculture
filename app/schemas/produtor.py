from pydantic import BaseModel, ConfigDict
from typing import Optional


class ProdutorBase(BaseModel):
    nome: str
    cpf_cnpj: str


class ProdutorCreate(ProdutorBase):
    pass


class ProdutorUpdate(BaseModel):
    nome: Optional[str] = None
    cpf_cnpj: Optional[str] = None


class ProdutorRead(ProdutorBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
