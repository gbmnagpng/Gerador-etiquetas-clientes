#!/usr/bin/env bash
# setup.sh
# --------
# Prepara o Gerador de Etiquetas para rodar neste PC (Linux/macOS) com o
# minimo de configuracao manual: cria um ambiente virtual isolado (.venv)
# e instala automaticamente as dependencias de requirements.txt.
#
# Uso:
#     ./setup.sh
# Depois, para abrir o programa:
#     ./.venv/bin/python main.py
#
# Requisitos do sistema (uma unica vez, via gerenciador de pacotes):
#   Debian/Ubuntu: sudo apt install python3-venv python3-tk python3-pil.imagetk
#   Fedora:        sudo dnf install python3-tkinter
#   macOS:         Python.org ja inclui Tk; nao precisa de nada extra.

set -e

if ! command -v python3 >/dev/null 2>&1; then
    echo "[ERRO] python3 nao encontrado. Instale o Python 3.10+ antes de continuar."
    exit 1
fi

if ! python3 -c "import tkinter" >/dev/null 2>&1; then
    echo "[ERRO] O modulo tkinter nao esta disponivel neste Python."
    echo "Instale com: sudo apt install python3-tk python3-pil.imagetk (Debian/Ubuntu)"
    exit 1
fi

echo "Criando ambiente virtual em .venv ..."
python3 -m venv --system-site-packages .venv

echo "Instalando dependencias ..."
./.venv/bin/pip install --upgrade pip
./.venv/bin/pip install -r requirements.txt

echo
echo "Tudo pronto! Para abrir o programa:"
echo "    ./.venv/bin/python main.py"
