@echo off
title Teste Boletos

echo ===============================
echo    INICIANDO PROJETO TESTE BOLETOS
echo ===============================
echo.

REM Verifica se pipenv está instalado
echo Verificando dependencias...
pip show pipenv >nul 2>&1
if errorlevel 1 (
    echo Pipenv nao encontrado. Instalando...
    pip install pipenv
)

REM Instala dependancias do projeto
echo Instalando dependencias do projeto...
pipenv install

echo.
echo Iniciando aplicacao...
echo ===============================
echo.

REM Executa a aplicação
pipenv run python main.py

echo.
echo Aplicacao finalizada. Pressione qualquer tecla para sair...
pause >nul