from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models import ProdutorRural
from app.models.database import SessionLocal
from app.schemas.produtor import ProdutorCreate, ProdutorRead, ProdutorUpdate
from typing import List
from app.services.validators import validar_cpf_cnpj

"""
Rota para gerenciar Produtores Rurais
"""
router = APIRouter(prefix="/produtores", tags=["Produtores"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""
Criação de um novo produtor rural
"""


@router.post("/", response_model=ProdutorRead, status_code=status.HTTP_201_CREATED)
def create_produtor(produtor: ProdutorCreate, db: Session = Depends(get_db)):
    if not validar_cpf_cnpj(produtor.cpf_cnpj):
        raise HTTPException(status_code=400, detail="CPF ou CNPJ inválido")
    
    try:
        db_produtor = ProdutorRural(**produtor.model_dump())
        db.add(db_produtor)
        db.commit()
        db.refresh(db_produtor)
        return db_produtor
    except IntegrityError as e:
        db.rollback()
        if "UNIQUE constraint failed" in str(e) and "cpf_cnpj" in str(e):
            raise HTTPException(status_code=400, detail="CPF ou CNPJ já cadastrado")
        raise HTTPException(status_code=400, detail="Erro ao criar produtor")


"""
Listar todos os produtores rurais
"""


@router.get("/", response_model=List[ProdutorRead])
def list_produtores(db: Session = Depends(get_db)):
    return db.query(ProdutorRural).all()


"""
Obter um produtor rural específico pelo ID
"""


@router.get("/{produtor_id}", response_model=ProdutorRead)
def get_produtor(produtor_id: int, db: Session = Depends(get_db)):
    produtor = db.query(ProdutorRural).filter(ProdutorRural.id == produtor_id).first()
    if not produtor:
        raise HTTPException(status_code=404, detail="Produtor não encontrado")
    return produtor


"""
Atualizar um produtor rural específico pelo ID
"""


@router.put("/{produtor_id}", response_model=ProdutorRead)
def update_produtor(produtor_id: int, produtor: ProdutorUpdate, db: Session = Depends(get_db)):
    db_produtor = db.query(ProdutorRural).filter(ProdutorRural.id == produtor_id).first()
    if not db_produtor:
        raise HTTPException(status_code=404, detail="Produtor não encontrado")
    
    if produtor.cpf_cnpj and not validar_cpf_cnpj(produtor.cpf_cnpj):
        raise HTTPException(status_code=400, detail="CPF ou CNPJ inválido")
    
    try:
        for key, value in produtor.model_dump(exclude_unset=True).items():
            setattr(db_produtor, key, value)
        db.commit()
        db.refresh(db_produtor)
        return db_produtor
    except IntegrityError as e:
        db.rollback()
        if "UNIQUE constraint failed" in str(e) and "cpf_cnpj" in str(e):
            raise HTTPException(status_code=400, detail="CPF ou CNPJ já cadastrado")
        raise HTTPException(status_code=400, detail="Erro ao atualizar produtor")


"""
Deletar um produtor rural específico pelo ID
"""


@router.delete("/{produtor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_produtor(produtor_id: int, db: Session = Depends(get_db)):
    db_produtor = db.query(ProdutorRural).filter(ProdutorRural.id == produtor_id).first()
    if not db_produtor:
        raise HTTPException(status_code=404, detail="Produtor não encontrado")
    db.delete(db_produtor)
    db.commit()
    return None
