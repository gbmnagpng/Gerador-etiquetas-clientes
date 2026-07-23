# -*- mode: python ; coding: utf-8 -*-
#
# Gera um executável autônomo (Windows: main.exe / Linux: main):
# nenhuma instalação de Python, pip ou bibliotecas é necessária na
# máquina de destino - basta copiar o binário gerado em dist/ e clicar
# (requisito de "rodar em qualquer PC com o mínimo de configurações").
#
# Este mesmo main.spec é usado nos dois sistemas. O PyInstaller sempre
# empacota para a plataforma em que ele próprio está rodando, então:
#     Windows -> rode `pyinstaller main.spec` em uma máquina Windows
#     Linux   -> rode `pyinstaller main.spec` em uma máquina Linux
#
# Observação: o CustomTkinter guarda temas/fontes/ícones em uma pasta
# `assets/` própria do pacote que o PyInstaller NÃO inclui automaticamente
# -> sem `collect_data_files` abaixo o executável abre e fecha sem aviso
# (ou fica sem tema) em qualquer PC que não tenha o customtkinter
# instalado globalmente. O mesmo vale para os módulos opcionais do
# Windows (pywin32 / PyMuPDF) usados por printer_windows.py: como são
# importados dinamicamente (dentro de função, não no topo do arquivo), o
# PyInstaller não os detecta sozinho - por isso só entram em
# hiddenimports quando o build roda no Windows (no Linux esses módulos
# nem existem, e forçá-los quebraria o build).

import sys

from PyInstaller.utils.hooks import collect_data_files

datas = collect_data_files('customtkinter')
datas += [('assets', 'assets')]  # ícones/fontes/templates próprios do projeto

hiddenimports = [
    'PIL._tkinter_finder',
]

icone = None
if sys.platform.startswith('win'):
    hiddenimports += ['win32print', 'win32ui', 'win32con', 'PIL.ImageWin', 'fitz']
    icone = 'assets/icons/icon.ico'

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icone,
)
