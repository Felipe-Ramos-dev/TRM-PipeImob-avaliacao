# app/schemas/sch_comissao.py
from pydantic import BaseModel
from typing import Optional

class ComissaoBase(BaseModel):
    percentual: float

class ComissaoCreate(ComissaoBase):
    pass

class Comissao(ComissaoBase):
    id: str
    transacao_id: str
    valor_calculado: float
    paga: bool

    class Config:
        orm_mode = True
