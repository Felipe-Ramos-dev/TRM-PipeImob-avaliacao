# app/routers/rou_partes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.sch_parte import Parte, ParteCreate
from app.models.mod_parte import Parte as ParteModel, TipoEnum
from app.models.mod_transacao import Transacao as TransacaoModel
from app.database import get_db
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/api/v1/partes", tags=["Partes"])

@router.post("/transacoes/{transacao_id}", response_model=Parte)
def criar_parte(transacao_id: str, parte: ParteCreate, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    transacao = db.query(TransacaoModel).filter(TransacaoModel.id == transacao_id).first()
    if not transacao:
        raise HTTPException(status_code=404, detail="Transacao nao encontrada")

    db_parte = ParteModel(
        transacao_id=transacao_id,
        tipo=parte.tipo,
        nome=parte.nome,
        cpf_cnpj=parte.cpf_cnpj,
        email=parte.email
    )
    db.add(db_parte)
    db.commit()
    db.refresh(db_parte)
    return db_parte

@router.get("/transacoes/{transacao_id}", response_model=List[Parte])
def listar_partes(transacao_id: str, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    partes = db.query(ParteModel).filter(ParteModel.transacao_id == transacao_id).all()
    return partes

@router.delete("/{parte_id}", status_code=204)
def deletar_parte(parte_id: str, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    parte = db.query(ParteModel).filter(ParteModel.id == parte_id).first()
    if not parte:
        raise HTTPException(status_code=404, detail="Parte nao encontrada")
    db.delete(parte)
    db.commit()
