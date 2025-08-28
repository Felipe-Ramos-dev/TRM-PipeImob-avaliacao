@echo off
REM Build e run TRM PipeImob via Docker

echo Construindo e iniciando containers Docker...
docker-compose up --build
pause
