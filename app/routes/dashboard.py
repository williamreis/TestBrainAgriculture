from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Propriedade, PropriedadeSafraCultura, Cultura
from app.models.database import SessionLocal
from app.schemas.dashboard import (
    DashboardData,
    DashboardStats,
    GraficoEstado,
    GraficoCultura,
    GraficoUsoSolo
)
from typing import List

"""
Rota para o Dashboard
"""
router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""
Endpoint para obter dados do dashboard
"""


@router.get("/", response_model=DashboardData)
def get_dashboard_data(db: Session = Depends(get_db)):
    # Estatísticas gerais
    total_fazendas = db.query(func.count(Propriedade.id)).scalar()
    total_hectares = db.query(func.sum(Propriedade.area_total)).scalar() or 0.0

    # Gráfico por estado
    estados_data = db.query(
        Propriedade.estado,
        func.count(Propriedade.id).label('quantidade')
    ).group_by(Propriedade.estado).all()

    grafico_estados = []
    for estado, quantidade in estados_data:
        percentual = (quantidade / total_fazendas * 100) if total_fazendas > 0 else 0
        grafico_estados.append(GraficoEstado(
            estado=estado,
            quantidade=quantidade,
            percentual=round(percentual, 2)
        ))

    # Gráfico por cultura plantada
    culturas_data = db.query(
        Cultura.nome,
        func.count(PropriedadeSafraCultura.id).label('quantidade')
    ).join(PropriedadeSafraCultura).group_by(Cultura.nome).all()

    total_culturas = sum(qtd for _, qtd in culturas_data)
    grafico_culturas = []
    for cultura, quantidade in culturas_data:
        percentual = (quantidade / total_culturas * 100) if total_culturas > 0 else 0
        grafico_culturas.append(GraficoCultura(
            cultura=cultura,
            quantidade=quantidade,
            percentual=round(percentual, 2)
        ))

    # Gráfico por uso do solo
    area_agricultavel = db.query(func.sum(Propriedade.area_agricultavel)).scalar() or 0.0
    area_vegetacao = db.query(func.sum(Propriedade.area_vegetacao)).scalar() or 0.0

    grafico_uso_solo = []
    if total_hectares > 0:
        grafico_uso_solo.extend([
            GraficoUsoSolo(
                tipo="Área Agricultável",
                area=area_agricultavel,
                percentual=round((area_agricultavel / total_hectares) * 100, 2)
            ),
            GraficoUsoSolo(
                tipo="Área de Vegetação",
                area=area_vegetacao,
                percentual=round((area_vegetacao / total_hectares) * 100, 2)
            )
        ])

    return DashboardData(
        estatisticas=DashboardStats(
            total_fazendas=total_fazendas,
            total_hectares=round(total_hectares, 2)
        ),
        grafico_estados=grafico_estados,
        grafico_culturas=grafico_culturas,
        grafico_uso_solo=grafico_uso_solo
    )


"""
Endpoint para obter estatísticas do dashboard
"""


@router.get("/estatisticas", response_model=DashboardStats)
def get_estatisticas(db: Session = Depends(get_db)):
    total_fazendas = db.query(func.count(Propriedade.id)).scalar()
    total_hectares = db.query(func.sum(Propriedade.area_total)).scalar() or 0.0

    return DashboardStats(
        total_fazendas=total_fazendas,
        total_hectares=round(total_hectares, 2)
    )


"""
Endpoint para obter gráficos por estado, cultura e uso do solo
"""


@router.get("/grafico-estados", response_model=List[GraficoEstado])
def get_grafico_estados(db: Session = Depends(get_db)):
    total_fazendas = db.query(func.count(Propriedade.id)).scalar()

    estados_data = db.query(
        Propriedade.estado,
        func.count(Propriedade.id).label('quantidade')
    ).group_by(Propriedade.estado).all()

    grafico_estados = []
    for estado, quantidade in estados_data:
        percentual = (quantidade / total_fazendas * 100) if total_fazendas > 0 else 0
        grafico_estados.append(GraficoEstado(
            estado=estado,
            quantidade=quantidade,
            percentual=round(percentual, 2)
        ))

    return grafico_estados


"""
Endpoint para obter gráfico de culturas plantadas
"""


@router.get("/grafico-culturas", response_model=List[GraficoCultura])
def get_grafico_culturas(db: Session = Depends(get_db)):
    culturas_data = db.query(
        Cultura.nome,
        func.count(PropriedadeSafraCultura.id).label('quantidade')
    ).join(PropriedadeSafraCultura).group_by(Cultura.nome).all()

    total_culturas = sum(qtd for _, qtd in culturas_data)
    grafico_culturas = []
    for cultura, quantidade in culturas_data:
        percentual = (quantidade / total_culturas * 100) if total_culturas > 0 else 0
        grafico_culturas.append(GraficoCultura(
            cultura=cultura,
            quantidade=quantidade,
            percentual=round(percentual, 2)
        ))

    return grafico_culturas


"""
Endpoint para obter gráfico de uso do solo
"""


@router.get("/grafico-uso-solo", response_model=List[GraficoUsoSolo])
def get_grafico_uso_solo(db: Session = Depends(get_db)):
    total_hectares = db.query(func.sum(Propriedade.area_total)).scalar() or 0.0
    area_agricultavel = db.query(func.sum(Propriedade.area_agricultavel)).scalar() or 0.0
    area_vegetacao = db.query(func.sum(Propriedade.area_vegetacao)).scalar() or 0.0

    grafico_uso_solo = []
    if total_hectares > 0:
        grafico_uso_solo.extend([
            GraficoUsoSolo(
                tipo="Área Agricultável",
                area=area_agricultavel,
                percentual=round((area_agricultavel / total_hectares) * 100, 2)
            ),
            GraficoUsoSolo(
                tipo="Área de Vegetação",
                area=area_vegetacao,
                percentual=round((area_vegetacao / total_hectares) * 100, 2)
            )
        ])

    return grafico_uso_solo
