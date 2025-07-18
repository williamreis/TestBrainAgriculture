from pydantic import BaseModel, ConfigDict
from typing import Optional


class CulturaBase(BaseModel):
    nome: str


class CulturaCreate(CulturaBase):
    pass


class CulturaUpdate(BaseModel):
    nome: Optional[str] = None


class CulturaRead(CulturaBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
