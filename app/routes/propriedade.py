from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import Propriedade, ProdutorRural
from app.models.database import SessionLocal
from app.schemas.propriedade import PropriedadeCreate, PropriedadeRead, PropriedadeUpdate
from typing import List

"""
Rota para gerenciar Propriedades
"""
router = APIRouter(prefix="/propriedades", tags=["Propriedades"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def validar_areas_propriedade(area_total: float, area_agricultavel: float, area_vegetacao: float):
    if area_agricultavel + area_vegetacao > area_total:
        raise HTTPException(
            status_code=400,
            detail="Soma das áreas agricultável e vegetação não pode ultrapassar a área total"
        )


"""
Criação de uma nova propriedade
"""


@router.post("/", response_model=PropriedadeRead, status_code=status.HTTP_201_CREATED)
def create_propriedade(propriedade: PropriedadeCreate, db: Session = Depends(get_db)):
    # Verificar se o produtor existe
    produtor = db.query(ProdutorRural).filter(ProdutorRural.id == propriedade.produtor_id).first()
    if not produtor:
        raise HTTPException(status_code=404, detail="Produtor não encontrado")

    # Validar áreas
    validar_areas_propriedade(
        propriedade.area_total,
        propriedade.area_agricultavel,
        propriedade.area_vegetacao
    )

    db_propriedade = Propriedade(**propriedade.dict())
    db.add(db_propriedade)
    db.commit()
    db.refresh(db_propriedade)
    return db_propriedade


"""
Listar todas as propriedades
"""


@router.get("/", response_model=List[PropriedadeRead])
def list_propriedades(db: Session = Depends(get_db)):
    return db.query(Propriedade).all()


"""
Obter uma propriedade específica pelo ID
"""


@router.get("/{propriedade_id}", response_model=PropriedadeRead)
def get_propriedade(propriedade_id: int, db: Session = Depends(get_db)):
    propriedade = db.query(Propriedade).filter(Propriedade.id == propriedade_id).first()
    if not propriedade:
        raise HTTPException(status_code=404, detail="Propriedade não encontrada")
    return propriedade


"""
Atualizar uma propriedade existente
"""


@router.put("/{propriedade_id}", response_model=PropriedadeRead)
def update_propriedade(propriedade_id: int, propriedade: PropriedadeUpdate, db: Session = Depends(get_db)):
    db_propriedade = db.query(Propriedade).filter(Propriedade.id == propriedade_id).first()
    if not db_propriedade:
        raise HTTPException(status_code=404, detail="Propriedade não encontrada")

    # Preparar dados para validação
    update_data = propriedade.dict(exclude_unset=True)
    area_total = update_data.get('area_total', db_propriedade.area_total)
    area_agricultavel = update_data.get('area_agricultavel', db_propriedade.area_agricultavel)
    area_vegetacao = update_data.get('area_vegetacao', db_propriedade.area_vegetacao)

    # Validar áreas se alguma foi fornecida
    if 'area_total' in update_data or 'area_agricultavel' in update_data or 'area_vegetacao' in update_data:
        validar_areas_propriedade(area_total, area_agricultavel, area_vegetacao)

    for key, value in update_data.items():
        setattr(db_propriedade, key, value)

    db.commit()
    db.refresh(db_propriedade)
    return db_propriedade


"""
Deletar uma propriedade existente
"""


@router.delete("/{propriedade_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_propriedade(propriedade_id: int, db: Session = Depends(get_db)):
    db_propriedade = db.query(Propriedade).filter(Propriedade.id == propriedade_id).first()
    if not db_propriedade:
        raise HTTPException(status_code=404, detail="Propriedade não encontrada")
    db.delete(db_propriedade)
    db.commit()
    return None
