@echo off
REM Run TRM PipeImob locally

echo Iniciando TRM PipeImob local...

REM Ativar ambiente virtual
call .venv\Scripts\activate

REM Setar variáveis de ambiente do .env
for /f "tokens=1,2 delims==" %%a in (.env) do set %%a=%%b

REM Executar FastAPI
uvicorn main:app --reload --host 0.0.0.0 --port 8000

pause
