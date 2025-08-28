# app/routers/rou_transacoes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.sch_transacao import Transacao, TransacaoCreate, TransacaoUpdate, TransacaoStatusUpdate
from app.models.mod_transacao import Transacao as TransacaoModel, StatusEnum
from app.database import get_db
from app.dependencies.auth import get_current_user
from app.utils.pagination import paginate

router = APIRouter(prefix="/api/v1/transacoes", tags=["Transacoes"])


@router.post("/", response_model=Transacao)
def criar_transacao(transacao: TransacaoCreate, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    db_transacao = TransacaoModel(
        imovel_codigo=transacao.imovel_codigo,
        valor_venda=transacao.valor_venda,
        status=StatusEnum.CRIADA
    )
    db.add(db_transacao)
    db.commit()
    db.refresh(db_transacao)
    return db_transacao


@router.get("/", response_model=List[Transacao])
def listar_transacoes(
        status: Optional[StatusEnum] = None,
        imovel_codigo: Optional[str] = None,
        skip: int = 0,
        limit: int = 10,
        db: Session = Depends(get_db),
        user: str = Depends(get_current_user)
):
    query = db.query(TransacaoModel)
    if status:
        query = query.filter(TransacaoModel.status == status)
    if imovel_codigo:
        query = query.filter(TransacaoModel.imovel_codigo == imovel_codigo)
    return paginate(query, skip=skip, limit=limit)


@router.get("/{transacao_id}", response_model=Transacao)
def obter_transacao(transacao_id: str, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    transacao = db.query(TransacaoModel).filter(TransacaoModel.id == transacao_id).first()
    if not transacao:
        raise HTTPException(status_code=404, detail="Transacao nao encontrada")
    return transacao


@router.put("/{transacao_id}", response_model=Transacao)
def atualizar_transacao(transacao_id: str, transacao: TransacaoUpdate, db: Session = Depends(get_db),
                        user: str = Depends(get_current_user)):
    db_transacao = db.query(TransacaoModel).filter(TransacaoModel.id == transacao_id).first()
    if not db_transacao:
        raise HTTPException(status_code=404, detail="Transacao nao encontrada")
    for key, value in transacao.dict(exclude_unset=True).items():
        setattr(db_transacao, key, value)
    db.commit()
    db.refresh(db_transacao)
    return db_transacao


@router.patch("/{transacao_id}/status", response_model=Transacao)
def atualizar_status(transacao_id: str, status_update: TransacaoStatusUpdate, db: Session = Depends(get_db),
                     user: str = Depends(get_current_user)):
    db_transacao = db.query(TransacaoModel).filter(TransacaoModel.id == transacao_id).first()
    if not db_transacao:
        raise HTTPException(status_code=404, detail="Transacao nao encontrada")

    # Regras de transição
    status_atual = db_transacao.status
    novo_status = status_update.status

    valid_transitions = {
        StatusEnum.CRIADA: [StatusEnum.EM_ANALISE, StatusEnum.CANCELADA],
        StatusEnum.EM_ANALISE: [StatusEnum.APROVADA, StatusEnum.CANCELADA],
        StatusEnum.APROVADA: [StatusEnum.FINALIZADA, StatusEnum.CANCELADA],
        StatusEnum.FINALIZADA: [],
        StatusEnum.CANCELADA: []
    }

    if novo_status not in valid_transitions.get(status_atual, []):
        raise HTTPException(status_code=422, detail=f"Transicao invalida de {status_atual} para {novo_status}")

    db_transacao.status = novo_status
    db.commit()
    db.refresh(db_transacao)
    return db_transacao


@router.delete("/{transacao_id}", status_code=204)
def deletar_transacao(transacao_id: str, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    db_transacao = db.query(TransacaoModel).filter(TransacaoModel.id == transacao_id).first()
    if not db_transacao:
        raise HTTPException(status_code=404, detail="Transacao nao encontrada")
    db.delete(db_transacao)
    db.commit()
