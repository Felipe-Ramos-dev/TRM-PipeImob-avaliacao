# app/models/mod_comissao.py
import uuid
from sqlalchemy import Column, Numeric, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base

class Comissao(Base):
    __tablename__ = "comissoes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transacao_id = Column(UUID(as_uuid=True), ForeignKey("transacoes.id"), nullable=False)
    percentual = Column(Numeric(5,4), nullable=False)
    valor_calculado = Column(Numeric(12,2), nullable=False)
    paga = Column(Boolean, default=False)
