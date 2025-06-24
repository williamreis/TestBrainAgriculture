from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import Safra
from app.models.database import SessionLocal
from app.schemas.safra import SafraCreate, SafraRead, SafraUpdate
from typing import List

"""
Rota para gerenciar Safras
"""
router = APIRouter(prefix="/safras", tags=["Safras"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""
Criação de uma nova safra
"""


@router.post("/", response_model=SafraRead, status_code=status.HTTP_201_CREATED)
def create_safra(safra: SafraCreate, db: Session = Depends(get_db)):
    # Verificar se já existe uma safra com o mesmo ano
    existing_safra = db.query(Safra).filter(Safra.ano == safra.ano).first()
    if existing_safra:
        raise HTTPException(status_code=400, detail="Já existe uma safra para este ano")

    db_safra = Safra(**safra.dict())
    db.add(db_safra)
    db.commit()
    db.refresh(db_safra)
    return db_safra


"""
Listar todas as safras
"""


@router.get("/", response_model=List[SafraRead])
def list_safras(db: Session = Depends(get_db)):
    return db.query(Safra).order_by(Safra.ano.desc()).all()


"""
Obter uma safra específica pelo ID
"""


@router.get("/{safra_id}", response_model=SafraRead)
def get_safra(safra_id: int, db: Session = Depends(get_db)):
    safra = db.query(Safra).filter(Safra.id == safra_id).first()
    if not safra:
        raise HTTPException(status_code=404, detail="Safra não encontrada")
    return safra


"""
Atualizar uma safra existente
"""


@router.put("/{safra_id}", response_model=SafraRead)
def update_safra(safra_id: int, safra: SafraUpdate, db: Session = Depends(get_db)):
    db_safra = db.query(Safra).filter(Safra.id == safra_id).first()
    if not db_safra:
        raise HTTPException(status_code=404, detail="Safra não encontrada")

    # Verificar se o novo ano já existe em outra safra
    if safra.ano and safra.ano != db_safra.ano:
        existing_safra = db.query(Safra).filter(Safra.ano == safra.ano).first()
        if existing_safra:
            raise HTTPException(status_code=400, detail="Já existe uma safra para este ano")

    for key, value in safra.dict(exclude_unset=True).items():
        setattr(db_safra, key, value)

    db.commit()
    db.refresh(db_safra)
    return db_safra


"""
Deletar uma safra
"""


@router.delete("/{safra_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_safra(safra_id: int, db: Session = Depends(get_db)):
    db_safra = db.query(Safra).filter(Safra.id == safra_id).first()
    if not db_safra:
        raise HTTPException(status_code=404, detail="Safra não encontrada")
    db.delete(db_safra)
    db.commit()
    return None
