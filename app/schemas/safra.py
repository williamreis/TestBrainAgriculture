from pydantic import BaseModel, validator
from typing import Optional


class SafraBase(BaseModel):
    ano: int

    """
    Validações para Safra
    """

    @validator('ano')
    def ano_valido(cls, v):
        if v < 1900 or v > 2100:
            raise ValueError('Ano deve estar entre 1900 e 2100')
        return v


class SafraCreate(SafraBase):
    pass


class SafraUpdate(BaseModel):
    ano: Optional[int] = None


class SafraRead(SafraBase):
    id: int

    class Config:
        orm_mode = True
