@echo off
REM instalar.bat
REM ------------
REM Instalador de um clique para Windows: gera o executavel autonomo (se
REM ainda nao existir) e cria os atalhos de "clicar e abrir" - um na
REM Area de Trabalho e outro no Menu Iniciar - sem exigir nenhum passo
REM manual do usuario.
REM
REM Uso: de um duplo clique neste arquivo.

setlocal
cd /d "%~dp0"

REM 1) Garante o ambiente virtual com as dependencias.
if not exist ".venv\Scripts\python.exe" (
    echo Ambiente virtual nao encontrado - rodando setup.bat primeiro...
    call setup.bat
)

REM 2) Garante o PyInstaller e gera dist\main.exe (o executavel autonomo).
if not exist "dist\main.exe" (
    echo Gerando o executavel autonomo ^(dist\main.exe^) ...
    ".venv\Scripts\pip.exe" install --upgrade pyinstaller pywin32 pymupdf -q
    ".venv\Scripts\pyinstaller.exe" --noconfirm main.spec
)

REM 3) Cria os atalhos na Area de Trabalho e no Menu Iniciar apontando
REM    para o executavel, com o icone do programa.
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "$dir = (Get-Location).Path;" ^
    "$target = Join-Path $dir 'dist\main.exe';" ^
    "$icon = Join-Path $dir 'assets\icons\icon.ico';" ^
    "$ws = New-Object -ComObject WScript.Shell;" ^
    "foreach ($destino in @([Environment]::GetFolderPath('Desktop'), [Environment]::GetFolderPath('StartMenu') + '\Programs')) {" ^
    "  $lnk = $ws.CreateShortcut((Join-Path $destino 'Gerador de Etiquetas.lnk'));" ^
    "  $lnk.TargetPath = $target;" ^
    "  $lnk.WorkingDirectory = $dir;" ^
    "  $lnk.IconLocation = $icon;" ^
    "  $lnk.Save();" ^
    "}"

echo.
echo Instalacao concluida!
echo - Procure por "Gerador de Etiquetas" no Menu Iniciar, ou
echo - de duplo clique no icone que apareceu na Area de Trabalho.
pause
