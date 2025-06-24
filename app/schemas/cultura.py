from pydantic import BaseModel
from typing import Optional


class CulturaBase(BaseModel):
    nome: str


class CulturaCreate(CulturaBase):
    pass


class CulturaUpdate(BaseModel):
    nome: Optional[str] = None


class CulturaRead(CulturaBase):
    id: int

    class Config:
        orm_mode = True
