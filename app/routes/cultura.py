from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import Cultura
from app.models.database import SessionLocal
from app.schemas.cultura import CulturaCreate, CulturaRead, CulturaUpdate
from typing import List

"""
Rota para gerenciar Culturas
"""
router = APIRouter(prefix="/culturas", tags=["Culturas"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""
Criação de uma nova cultura
"""


@router.post("/", response_model=CulturaRead, status_code=status.HTTP_201_CREATED)
def create_cultura(cultura: CulturaCreate, db: Session = Depends(get_db)):
    # Verificar se já existe uma cultura com o mesmo nome
    existing_cultura = db.query(Cultura).filter(Cultura.nome == cultura.nome).first()
    if existing_cultura:
        raise HTTPException(status_code=400, detail="Já existe uma cultura com este nome")

    db_cultura = Cultura(**cultura.dict())
    db.add(db_cultura)
    db.commit()
    db.refresh(db_cultura)
    return db_cultura


"""
Listar todas as culturas
"""


@router.get("/", response_model=List[CulturaRead])
def list_culturas(db: Session = Depends(get_db)):
    return db.query(Cultura).order_by(Cultura.nome).all()


"""
Obter uma cultura específica pelo ID
"""


@router.get("/{cultura_id}", response_model=CulturaRead)
def get_cultura(cultura_id: int, db: Session = Depends(get_db)):
    cultura = db.query(Cultura).filter(Cultura.id == cultura_id).first()
    if not cultura:
        raise HTTPException(status_code=404, detail="Cultura não encontrada")
    return cultura


"""
Atualizar uma cultura específica pelo ID
"""


@router.put("/{cultura_id}", response_model=CulturaRead)
def update_cultura(cultura_id: int, cultura: CulturaUpdate, db: Session = Depends(get_db)):
    db_cultura = db.query(Cultura).filter(Cultura.id == cultura_id).first()
    if not db_cultura:
        raise HTTPException(status_code=404, detail="Cultura não encontrada")

    # Verificar se o novo nome já existe em outra cultura
    if cultura.nome and cultura.nome != db_cultura.nome:
        existing_cultura = db.query(Cultura).filter(Cultura.nome == cultura.nome).first()
        if existing_cultura:
            raise HTTPException(status_code=400, detail="Já existe uma cultura com este nome")

    for key, value in cultura.dict(exclude_unset=True).items():
        setattr(db_cultura, key, value)

    db.commit()
    db.refresh(db_cultura)
    return db_cultura


"""
Deletar uma cultura específica pelo ID
"""


@router.delete("/{cultura_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cultura(cultura_id: int, db: Session = Depends(get_db)):
    db_cultura = db.query(Cultura).filter(Cultura.id == cultura_id).first()
    if not db_cultura:
        raise HTTPException(status_code=404, detail="Cultura não encontrada")
    db.delete(db_cultura)
    db.commit()
    return None
