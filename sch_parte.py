# app/schemas/sch_parte.py
from pydantic import BaseModel
from typing import Optional
from app.models.mod_parte import TipoParteEnum

class ParteBase(BaseModel):
    tipo: TipoParteEnum
    nome: str
    cpf_cnpj: str
    email: Optional[str] = None

class ParteCreate(ParteBase):
    pass

class Parte(ParteBase):
    id: str
    transacao_id: str

    class Config:
        orm_mode = True
