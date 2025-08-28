# app/models/mod_parte.py
import enum
import uuid
from sqlalchemy import Column, String, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base

class TipoParteEnum(str, enum.Enum):
    COMPRADOR = "COMPRADOR"
    VENDEDOR = "VENDEDOR"
    CORRETOR = "CORRETOR"

class Parte(Base):
    __tablename__ = "partes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transacao_id = Column(UUID(as_uuid=True), ForeignKey("transacoes.id"), nullable=False)
    tipo = Column(Enum(TipoParteEnum), nullable=False)
    nome = Column(String, nullable=False)
    cpf_cnpj = Column(String, nullable=False)
    email = Column(String, nullable=True)
