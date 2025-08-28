# data/exemplo_dados.py
import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy.orm import Session
from app.database import get_db, Base, engine
from app.models.mod_transacao import Transacao
from app.models.mod_parte import Parte
from app.models.mod_comissao import Comissao

def criar_dados_exemplo(db: Session):
    # Transações de exemplo
    t1_id = str(uuid.uuid4())
    t2_id = str(uuid.uuid4())

    transacoes = [
        Transacao(
            id=t1_id,
            imovel_codigo="IMOVEL001",
            valor_venda=Decimal("500000.00"),
            status="CRIADA",
            data_criacao=datetime.now(),
            data_atualizacao=datetime.now()
        ),
        Transacao(
            id=t2_id,
            imovel_codigo="IMOVEL002",
            valor_venda=Decimal("750000.00"),
            status="EM_ANALISE",
            data_criacao=datetime.now(),
            data_atualizacao=datetime.now()
        )
    ]

    for t in transacoes:
        db.add(t)
    db.commit()

    # Partes de exemplo
    partes = [
        # Transação 1
        Parte(
            id=str(uuid.uuid4()),
            transacao_id=t1_id,
            tipo="COMPRADOR",
            nome="João Silva",
            cpf_cnpj="12345678901",
            email="joao@example.com"
        ),
        Parte(
            id=str(uuid.uuid4()),
            transacao_id=t1_id,
            tipo="VENDEDOR",
            nome="Maria Souza",
            cpf_cnpj="10987654321",
            email="maria@example.com"
        ),
        Parte(
            id=str(uuid.uuid4()),
            transacao_id=t1_id,
            tipo="CORRETOR",
            nome="Carlos Pereira",
            cpf_cnpj="98765432100",
            email="carlos@example.com"
        ),
        # Transação 2
        Parte(
            id=str(uuid.uuid4()),
            transacao_id=t2_id,
            tipo="COMPRADOR",
            nome="Ana Lima",
            cpf_cnpj="22334455667",
            email="ana@example.com"
        ),
        Parte(
            id=str(uuid.uuid4()),
            transacao_id=t2_id,
            tipo="VENDEDOR",
            nome="Paulo Rocha",
            cpf_cnpj="33445566778",
            email="paulo@example.com"
        ),
        Parte(
            id=str(uuid.uuid4()),
            transacao_id=t2_id,
            tipo="CORRETOR",
            nome="Fernanda Alves",
            cpf_cnpj="44556677889",
            email="fernanda@example.com"
        )
    ]

    for p in partes:
        db.add(p)
    db.commit()

    # Comissões de exemplo
    comissoes = [
        Comissao(
            id=str(uuid.uuid4()),
            transacao_id=t1_id,
            percentual=Decimal("0.05"),
            valor_calculado=transacoes[0].valor_venda * Decimal("0.05"),
            paga=False
        ),
        Comissao(
            id=str(uuid.uuid4()),
            transacao_id=t2_id,
            percentual=Decimal("0.06"),
            valor_calculado=transacoes[1].valor_venda * Decimal("0.06"),
            paga=False
        )
    ]

    for c in comissoes:
        db.add(c)
    db.commit()

if __name__ == "__main__":
    # Cria todas as tabelas do projeto
    Base.metadata.create_all(bind=engine)
    # Popula DB com dados de exemplo
    with get_db() as db:
        criar_dados_exemplo(db)
    print("Banco de dados populado com dados de exemplo para duas transações completas.")
