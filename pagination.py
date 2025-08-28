# app/utils/pagination.py
from fastapi import Query
from typing import Optional, Dict, Any

def get_pagination_params(
    limit: int = Query(10, ge=1, le=100, description="Número máximo de registros retornados"),
    offset: int = Query(0, ge=0, description="Número de registros a pular")
) -> Dict[str, int]:
    """
    Retorna parâmetros de paginação para consultas SQLAlchemy.
    """
    return {"limit": limit, "offset": offset}


def apply_filters(query, model, filters: Optional[Dict[str, Any]] = None):
    """
    Aplica filtros dinâmicos a uma query SQLAlchemy.
    `filters` deve ser um dicionário {campo: valor}.
    """
    if filters:
        for attr, value in filters.items():
            if hasattr(model, attr) and value is not None:
                query = query.filter(getattr(model, attr) == value)
    return query
