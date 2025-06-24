from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from app.models import PropriedadeSafraCultura, Propriedade, Safra, Cultura
from app.models.database import SessionLocal
from app.schemas.propriedade_safra_cultura import (
    PropriedadeSafraCulturaCreate,
    PropriedadeSafraCulturaRead,
    PropriedadeSafraCulturaUpdate,
    PropriedadeSafraCulturaDetail
)
from typing import List

"""
Rota para gerenciar Propriedade Safra Cultura
"""
router = APIRouter(prefix="/propriedade-safra-cultura", tags=["Propriedade-Safra-Cultura"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""
Criação de uma nova associação entre Propriedade, Safra e Cultura
"""


@router.post("/", response_model=PropriedadeSafraCulturaRead, status_code=status.HTTP_201_CREATED)
def create_propriedade_safra_cultura(
        psc: PropriedadeSafraCulturaCreate,
        db: Session = Depends(get_db)
):
    # Verificar se a propriedade existe
    propriedade = db.query(Propriedade).filter(Propriedade.id == psc.propriedade_id).first()
    if not propriedade:
        raise HTTPException(status_code=404, detail="Propriedade não encontrada")

    # Verificar se a safra existe
    safra = db.query(Safra).filter(Safra.id == psc.safra_id).first()
    if not safra:
        raise HTTPException(status_code=404, detail="Safra não encontrada")

    # Verificar se a cultura existe
    cultura = db.query(Cultura).filter(Cultura.id == psc.cultura_id).first()
    if not cultura:
        raise HTTPException(status_code=404, detail="Cultura não encontrada")

    # Verificar se já existe esta associação
    existing = db.query(PropriedadeSafraCultura).filter(
        PropriedadeSafraCultura.propriedade_id == psc.propriedade_id,
        PropriedadeSafraCultura.safra_id == psc.safra_id,
        PropriedadeSafraCultura.cultura_id == psc.cultura_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Esta associação já existe"
        )

    db_psc = PropriedadeSafraCultura(**psc.dict())
    db.add(db_psc)
    db.commit()
    db.refresh(db_psc)
    return db_psc


"""
Listar todas as associações entre Propriedade, Safra e Cultura
"""


@router.get("/", response_model=List[PropriedadeSafraCulturaDetail])
def list_propriedade_safra_cultura(db: Session = Depends(get_db)):
    return db.query(PropriedadeSafraCultura).options(
        joinedload(PropriedadeSafraCultura.propriedade),
        joinedload(PropriedadeSafraCultura.safra),
        joinedload(PropriedadeSafraCultura.cultura)
    ).all()


"""
Obter uma associação específica entre Propriedade, Safra e Cultura pelo ID
"""


@router.get("/{psc_id}", response_model=PropriedadeSafraCulturaDetail)
def get_propriedade_safra_cultura(psc_id: int, db: Session = Depends(get_db)):
    psc = db.query(PropriedadeSafraCultura).options(
        joinedload(PropriedadeSafraCultura.propriedade),
        joinedload(PropriedadeSafraCultura.safra),
        joinedload(PropriedadeSafraCultura.cultura)
    ).filter(PropriedadeSafraCultura.id == psc_id).first()

    if not psc:
        raise HTTPException(status_code=404, detail="Associação não encontrada")
    return psc


"""
Atualizar uma associação existente entre Propriedade, Safra e Cultura
"""


@router.put("/{psc_id}", response_model=PropriedadeSafraCulturaRead)
def update_propriedade_safra_cultura(
        psc_id: int,
        psc: PropriedadeSafraCulturaUpdate,
        db: Session = Depends(get_db)
):
    db_psc = db.query(PropriedadeSafraCultura).filter(PropriedadeSafraCultura.id == psc_id).first()
    if not db_psc:
        raise HTTPException(status_code=404, detail="Associação não encontrada")

    update_data = psc.dict(exclude_unset=True)

    # Validar entidades relacionadas se fornecidas
    if 'propriedade_id' in update_data:
        propriedade = db.query(Propriedade).filter(Propriedade.id == update_data['propriedade_id']).first()
        if not propriedade:
            raise HTTPException(status_code=404, detail="Propriedade não encontrada")

    if 'safra_id' in update_data:
        safra = db.query(Safra).filter(Safra.id == update_data['safra_id']).first()
        if not safra:
            raise HTTPException(status_code=404, detail="Safra não encontrada")

    if 'cultura_id' in update_data:
        cultura = db.query(Cultura).filter(Cultura.id == update_data['cultura_id']).first()
        if not cultura:
            raise HTTPException(status_code=404, detail="Cultura não encontrada")

    # Verificar duplicação se todos os campos foram fornecidos
    if len(update_data) == 3:
        existing = db.query(PropriedadeSafraCultura).filter(
            PropriedadeSafraCultura.propriedade_id == update_data['propriedade_id'],
            PropriedadeSafraCultura.safra_id == update_data['safra_id'],
            PropriedadeSafraCultura.cultura_id == update_data['cultura_id'],
            PropriedadeSafraCultura.id != psc_id
        ).first()

        if existing:
            raise HTTPException(status_code=400, detail="Esta associação já existe")

    for key, value in update_data.items():
        setattr(db_psc, key, value)

    db.commit()
    db.refresh(db_psc)
    return db_psc


"""
Deletar uma associação entre Propriedade, Safra e Cultura
"""


@router.delete("/{psc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_propriedade_safra_cultura(psc_id: int, db: Session = Depends(get_db)):
    db_psc = db.query(PropriedadeSafraCultura).filter(PropriedadeSafraCultura.id == psc_id).first()
    if not db_psc:
        raise HTTPException(status_code=404, detail="Associação não encontrada")
    db.delete(db_psc)
    db.commit()
    return None
