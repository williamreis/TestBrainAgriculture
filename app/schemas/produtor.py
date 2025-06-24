from pydantic import BaseModel, validator
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

    class Config:
        orm_mode = True
