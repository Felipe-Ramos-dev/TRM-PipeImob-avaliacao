# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/trm_pipeimob")
API_TOKEN = os.getenv("API_TOKEN", "minha_chave_bearer_fixa")
