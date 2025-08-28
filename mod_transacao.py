# app/models/mod_transacao.py
import enum
import uuid
from sqlalchemy import Column, String, Enum, DateTime, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base

class StatusEnum(str, enum.Enum):
    CRIADA = "CRIADA"
    EM_ANALISE = "EM_ANALISE"
    APROVADA = "APROVADA"
    FINALIZADA = "FINALIZADA"
    CANCELADA = "CANCELADA"

class Transacao(Base):
    __tablename__ = "transacoes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    imovel_codigo = Column(String, nullable=False)
    valor_venda = Column(Numeric(12,2), nullable=False)
    status = Column(Enum(StatusEnum), default=StatusEnum.CRIADA, nullable=False)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    data_atualizacao = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
