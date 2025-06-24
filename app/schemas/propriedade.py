from pydantic import BaseModel, field_validator, ConfigDict
from typing import Optional


class PropriedadeBase(BaseModel):
    nome: str
    cidade: str
    estado: str
    area_total: float
    area_agricultavel: float
    area_vegetacao: float
    produtor_id: int

    """
    Validações para Propriedade
    """

    @field_validator('area_total', 'area_agricultavel', 'area_vegetacao')
    @classmethod
    def areas_positivas(cls, v):
        if v <= 0:
            raise ValueError('Área deve ser maior que zero')
        return v

    """
    Validações para Propriedade / Conforme as regras de negócio
    - Garantir que a soma das áreas agricultável e de vegetação não ultrapasse a área total da fazenda.
    """

    @field_validator('area_agricultavel', 'area_vegetacao')
    @classmethod
    def validar_soma_areas(cls, v, info):
        if info.data and 'area_total' in info.data and 'area_agricultavel' in info.data:
            area_agricultavel = info.data['area_agricultavel']
            area_total = info.data['area_total']
            if area_agricultavel + v > area_total:
                raise ValueError('Soma das áreas agricultável e vegetação não pode ultrapassar a área total')
        return v


class PropriedadeCreate(PropriedadeBase):
    pass


class PropriedadeUpdate(BaseModel):
    nome: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    area_total: Optional[float] = None
    area_agricultavel: Optional[float] = None
    area_vegetacao: Optional[float] = None


class PropriedadeRead(PropriedadeBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
