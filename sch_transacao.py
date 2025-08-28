# app/schemas/sch_transacao.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.models.mod_transacao import StatusEnum

class TransacaoBase(BaseModel):
    imovel_codigo: str
    valor_venda: float

class TransacaoCreate(TransacaoBase):
    pass

class TransacaoUpdate(TransacaoBase):
    status: Optional[StatusEnum]

class Transacao(TransacaoBase):
    id: str
    status: StatusEnum
    data_criacao: datetime
    data_atualizacao: datetime

    class Config:
        orm_mode = True

class TransacaoStatusUpdate(BaseModel):
    status: StatusEnum
    motivo_cancelamento: Optional[str] = None
