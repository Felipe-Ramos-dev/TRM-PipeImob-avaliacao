### `README.md`

# TRM PipeImob v2.1

## Descrição

Projeto backend em **FastAPI** para gerenciar o ciclo de vida de uma **transação imobiliária**, incluindo:

- CRUD completo de **Transações**, **Partes** e **Comissões**
- Alteração de status de transações com validações de regras de negócio
- Cálculo automático e pagamento de comissões
- Dados de exemplo já populados
- Autenticação via **Bearer token**
- Paginação e filtros nas listagens
- Containerizado com **Docker**


## Tecnologias utilizadas

- **Python 3.10+**
- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy**
- **Pydantic**
- **Docker & docker-compose**





## Explicação resumida dos arquivos principais   
•	main.py → inicializa o FastAPI, inclui routers e autenticação.  
•	models.py → define SQLAlchemy models: Transacao, Parte, Comissao.  
•	schemas.py → Pydantic schemas para validação de entrada e saída.  
•	database.py → conexão com PostgreSQL (Docker) usando SQLAlchemy.  
•	routers/ → endpoints da API.  
•	utils/auth.py → Bearer token simples via variável de ambiente.  
•	Dockerfile / docker-compose.yml → para rodar backend + PostgreSQL.  
•	start_trm.bat → inicia o backend e banco automaticamente.  
•	gerar_zip.py → gera um .zip do projeto no path atual.  
•	README.md → instruções de execução local e Docker.  


## Estrutura do Projeto
`TRM_v2_1/`  
 `│`  
 `├── app/`  
 `│   ├── __init__.py`  
 `│   ├── config.py               # Configurações (DB, token, env)`  
 `│   ├── database.py             # Conexão SQLAlchemy com PostgreSQL`  
 `│   ├── dependencies/`  
 `│   │   ├── __init__.py`  
 `│   │   └── auth.py             # Autenticação Bearer token`  
 `│   ├── models/`  
 `│   │   ├── __init__.py`  
 `│   │   ├── mod_transacao.py`  
 `│   │   ├── mod_parte.py`  
 `│   │   └── mod_comissao.py`  
 `│   ├── schemas/`  
 `│   │   ├── __init__.py`  
 `│   │   ├── sch_transacao.py`  
 `│   │   ├── sch_parte.py`  
 `│   │   └── sch_comissao.py`  
 `│   ├── routers/`  
 `│   │   ├── __init__.py`  
 `│   │   ├── rou_transacoes.py`  
 `│   │   ├── rou_partes.py`  
 `│   │   └── rou_comissoes.py`  
 `│   └── utils/`  
 `│       ├── __init__.py`  
 `│       └── pagination.py       # Funções de paginação e filtros`  
 `│`  
 `├── data/`  
 `│   └── exemplo_dados.py        # Script para popular DB com dados de teste`  
 `│`  
 `├── main.py                     # FastAPI app principal`  
 `├── .env                        # Variáveis de ambiente exemplo`  
 `├── requirements.txt            # Dependências Python`  
 `├── Dockerfile                  # Dockerfile para backend`  
 `├── docker-compose.yml          # Compose com backend + PostgreSQL`  
 `├── README.md                   # Instruções de execução e arquitetura`  
 `├── run_local.bat               # Script para Iniciar TRM PipeImob local`  
 `└── run_docker.bat              # Script para Construir e Iniciar containers Docker`  

## Como rodar

### Local (sem Docker)

1. Criar ambiente virtual Python:

python -m venv .venv
2.	Ativar ambiente:
### Windows
.venv\Scripts\activate

### Linux/macOS
source .venv/bin/activate

3.	Instalar dependências:
pip install -r requirements.txt
4.	Configurar variáveis de ambiente no arquivo .env:
DATABASE_URL=postgresql+psycopg2://usuario:senha@localhost:5432/trm_pipeimob
API_TOKEN=chave_fixa_para_bearer
5.	Criar tabelas e popular dados de exemplo:
python data/exemplo_dados.py
6.	Rodar a aplicação:
python app/main.py
________________________________________

## Com Docker  

1.	Construir containers:
docker-compose build
2.	Subir containers:
docker-compose up
3.	O backend estará disponível em:
http://localhost:8000
________________________________________
### Autenticação  
•	Utiliza Bearer token simples  
•	Adicione no header:  
Authorization: Bearer <API_TOKEN>  
________________________________________
### `Endpoints principais`  
  
### Transações  

•	POST /api/v1/transacoes — criar transação  
•	GET /api/v1/transacoes — listar transações (filtros: status, imovel_codigo, data_criacao; suporta paginação)  
•	GET /api/v1/transacoes/{id}  
•	PUT /api/v1/transacoes/{id} — atualizar  
•	PATCH /api/v1/transacoes/{id}/status — alterar status  
•	DELETE /api/v1/transacoes/{id} 
  
### Partes  
•	POST /api/v1/transacoes/{id}/partes — adicionar parte  
•	DELETE /api/v1/partes/{id} — remover parte  
  
### Comissões  
•	POST /api/v1/transacoes/{id}/comissoes — criar comissão  
•	POST /api/v1/comissoes/{id}/pagar — pagar comissão  
________________________________________
### População de dados de teste  
  
Para popular o banco com Transações, Partes e Comissões de exemplo:  
python data/exemplo_dados.py  
________________________________________
### Arquitetura & Decisões Técnicas 
  
•	Backend estruturado em routers, models e main.py  
•	SQLAlchemy ORM para interação com PostgreSQL  
•	Pydantic para validação de dados  
•	Endpoints de PATCH para alteração de status com validação de regras de negócio  
•	Tratamento de erros retornando status HTTP corretos (422, 404, 200, etc.)  
•	Logs estruturados e paginados para listagens  
•	Scripts .bat para facilitar execução local e com Docker  
________________________________________  
### `Proposta de Deploy na AWS`  
  
•	EC2 ou ECS Fargate para rodar containers Docker  
•	RDS PostgreSQL para banco de dados gerenciado  
•	S3 (opcional) para armazenar arquivos estáticos ou logs  
•	CloudWatch para monitoramento e logs  
•	Secrets Manager para gerenciar token Bearer e credenciais de banco  
•	Load Balancer (ALB) se múltiplas instâncias forem necessárias  
