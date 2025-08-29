# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from app.routers import rou_transacoes, rou_partes, rou_comissoes
from app.database import Base, engine, get_db
from sqlalchemy.orm import Session
import uvicorn

# Criação das tabelas no banco
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TRM PipeImob v2.1",
    description="API para gerenciamento de transações imobiliárias, partes e comissões",
    version="2.1"
)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ajuste para produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(rou_transacoes.router, prefix="/api/v1/transacoes", tags=["Transações"])
app.include_router(rou_partes.router, prefix="/api/v1/partes", tags=["Partes"])
app.include_router(rou_comissoes.router, prefix="/api/v1/comissoes", tags=["Comissões"])

# Health check
@app.get("/health", tags=["Health"])
def health(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1")
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
