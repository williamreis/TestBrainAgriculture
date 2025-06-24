from pydantic import BaseModel
from typing import Optional


class PropriedadeSafraCulturaBase(BaseModel):
    propriedade_id: int
    safra_id: int
    cultura_id: int


class PropriedadeSafraCulturaCreate(PropriedadeSafraCulturaBase):
    pass


class PropriedadeSafraCulturaUpdate(BaseModel):
    propriedade_id: Optional[int] = None
    safra_id: Optional[int] = None
    cultura_id: Optional[int] = None


class PropriedadeSafraCulturaRead(PropriedadeSafraCulturaBase):
    id: int
    propriedade_nome: Optional[str] = None
    safra_ano: Optional[int] = None
    cultura_nome: Optional[str] = None

    class Config:
        orm_mode = True


class PropriedadeSafraCulturaDetail(BaseModel):
    id: int
    propriedade_id: int
    propriedade_nome: str
    safra_id: int
    safra_ano: int
    cultura_id: int
    cultura_nome: str

    class Config:
        orm_mode = True
