# app/routers/rou_comissoes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.sch_comissao import Comissao, ComissaoCreate
from app.models.mod_comissao import Comissao as ComissaoModel
from app.models.mod_transacao import Transacao as TransacaoModel
from app.database import get_db
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/api/v1/comissoes", tags=["Comissoes"])


@router.post("/transacoes/{transacao_id}", response_model=Comissao)
def criar_comissao(transacao_id: str, comissao: ComissaoCreate, db: Session = Depends(get_db),
                   user: str = Depends(get_current_user)):
    transacao = db.query(TransacaoModel).filter(TransacaoModel.id == transacao_id).first()
    if not transacao:
        raise HTTPException(status_code=404, detail="Transacao nao encontrada")

    valor_calculado = transacao.valor_venda * comissao.percentual
    db_comissao = ComissaoModel(
        transacao_id=transacao_id,
        percentual=comissao.percentual,
        valor_calculado=valor_calculado,
        paga=False
    )
    db.add(db_comissao)
    db.commit()
    db.refresh(db_comissao)
    return db_comissao


@router.post("/{comissao_id}/pagar", response_model=Comissao)
def pagar_comissao(comissao_id: str, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    comissao = db.query(ComissaoModel).filter(ComissaoModel.id == comissao_id).first()
    if not comissao:
        raise HTTPException(status_code=404, detail="Comissao nao encontrada")
    if comissao.paga:
        raise HTTPException(status_code=400, detail="Comissao ja foi paga")

    comissao.paga = True
    db.commit()
    db.refresh(comissao)
    return comissao


@router.get("/transacoes/{transacao_id}", response_model=List[Comissao])
def listar_comissoes(transacao_id: str, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    comissoes = db.query(ComissaoModel).filter(ComissaoModel.transacao_id == transacao_id).all()
    return comissoes
