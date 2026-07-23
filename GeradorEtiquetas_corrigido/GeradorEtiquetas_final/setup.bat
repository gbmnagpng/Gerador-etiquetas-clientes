@echo off
REM setup.bat
REM ---------
REM Prepara o Gerador de Etiquetas para rodar neste PC com o minimo de
REM configuracao manual: cria um ambiente virtual isolado (.venv) e
REM instala automaticamente todas as dependencias de requirements.txt
REM (incluindo pywin32 + pymupdf para impressao nativa no Windows).
REM
REM Uso: de um duplo clique neste arquivo (ou rode "setup.bat" no
REM terminal). Ao final, use "executar.bat" para abrir o programa.
REM Requer apenas o Python 3.10+ instalado (https://python.org/downloads).

setlocal

where python >nul 2>nul
if errorlevel 1 (
    echo [ERRO] Python nao foi encontrado no PATH.
    echo Instale o Python em https://python.org/downloads e marque a opcao
    echo "Add Python to PATH" durante a instalacao. Depois rode este arquivo de novo.
    pause
    exit /b 1
)

echo Criando ambiente virtual em .venv ...
python -m venv .venv

echo Instalando dependencias ...
".venv\Scripts\python.exe" -m pip install --upgrade pip
".venv\Scripts\pip.exe" install -r requirements.txt

echo.
echo Tudo pronto! Use o arquivo "executar.bat" para abrir o Gerador de Etiquetas.
pause
