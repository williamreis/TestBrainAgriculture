from pydantic import BaseModel
from typing import List, Dict


class DashboardStats(BaseModel):
    total_fazendas: int
    total_hectares: float


class GraficoEstado(BaseModel):
    estado: str
    quantidade: int
    percentual: float


class GraficoCultura(BaseModel):
    cultura: str
    quantidade: int
    percentual: float


class GraficoUsoSolo(BaseModel):
    tipo: str
    area: float
    percentual: float


class DashboardData(BaseModel):
    estatisticas: DashboardStats
    grafico_estados: List[GraficoEstado]
    grafico_culturas: List[GraficoCultura]
    grafico_uso_solo: List[GraficoUsoSolo]
