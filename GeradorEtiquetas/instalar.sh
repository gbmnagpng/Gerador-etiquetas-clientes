#!/usr/bin/env bash
# instalar.sh
# -----------
# Instalador de um clique para Linux: gera o executável autônomo (se
# ainda não existir) e cria os atalhos de "clicar e abrir" - um no menu
# de aplicativos e outro na área de trabalho - sem exigir nenhum passo
# manual do usuário.
#
# Uso:
#     ./instalar.sh

set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

# 1) Garante o ambiente virtual com as dependências (reaproveita o
#    setup.sh se o .venv ainda não existir).
if [ ! -x ".venv/bin/python" ]; then
    echo "Ambiente virtual não encontrado - rodando setup.sh primeiro..."
    ./setup.sh
fi

# 2) Garante o PyInstaller e gera dist/main (o executável autônomo).
if [ ! -x "dist/main" ]; then
    echo "Gerando o executável autônomo (dist/main) ..."
    ./.venv/bin/pip install --upgrade pyinstaller -q
    ./.venv/bin/pyinstaller --workpath build/linux --noconfirm main.spec
fi

# 3) Instala o atalho (.desktop) no menu de aplicativos e na área de
#    trabalho, já apontando para o caminho real deste PC.
mkdir -p "$HOME/.local/share/applications"
sed "s#__APP_DIR__#$DIR#g" GeradorEtiquetas.desktop > "$HOME/.local/share/applications/GeradorEtiquetas.desktop"
chmod +x "$HOME/.local/share/applications/GeradorEtiquetas.desktop"

if [ -d "$HOME/Desktop" ]; then
    sed "s#__APP_DIR__#$DIR#g" GeradorEtiquetas.desktop > "$HOME/Desktop/GeradorEtiquetas.desktop"
    chmod +x "$HOME/Desktop/GeradorEtiquetas.desktop"
    command -v gio >/dev/null 2>&1 && gio set "$HOME/Desktop/GeradorEtiquetas.desktop" metadata::trusted true 2>/dev/null || true
fi

command -v update-desktop-database >/dev/null 2>&1 && update-desktop-database "$HOME/.local/share/applications" 2>/dev/null || true

echo
echo "Instalação concluída!"
echo "- Procure por \"Gerador de Etiquetas\" no menu de aplicativos, ou"
echo "- dê duplo clique no ícone que apareceu na sua área de trabalho."
