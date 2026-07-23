@echo off
REM executar.bat
REM ------------
REM Abre o Gerador de Etiquetas usando o ambiente virtual criado por
REM setup.bat. Se o .venv nao existir ainda, cai para o Python global.

if exist ".venv\Scripts\pythonw.exe" (
    start "" ".venv\Scripts\pythonw.exe" main.py
) else (
    echo [AVISO] .venv nao encontrado - rode "setup.bat" primeiro.
    echo Tentando abrir com o Python padrao do sistema...
    pythonw main.py 2>nul || python main.py
)
