# -*- coding: utf-8 -*-
"""
config.py
---------
Configurações centrais do Gerador de Etiquetas.

Reúne cores, tamanhos, fontes e textos padrão usados tanto pela interface
(CustomTkinter) quanto pelo módulo de desenho da etiqueta (ReportLab).
Mantendo tudo em um único lugar evita "números mágicos" espalhados pelo
código e facilita ajustes finos de layout.
"""

from reportlab.lib.units import mm

# ---------------------------------------------------------------------------
# Identidade / metadados
# ---------------------------------------------------------------------------
APP_NAME = "Gerador de Etiquetas"
APP_SUBTITLE = "Preencha os campos à direita e clique em Imprimir."
AUTOR_NOME = "Gabriel Menezes Aragão"
AUTOR_GITHUB = "github.com/gbmnagpng"
AUTOR_GITHUB_URL = "https://github.com/gbmnagpng"
ANO_COPYRIGHT = "2026"

# ---------------------------------------------------------------------------
# Paleta de cores (hexadecimal) - usada nos dois módulos
# ---------------------------------------------------------------------------
COR_NAVY = "#12224E"          # Azul-marinho principal (cabeçalho, ícones, bordas)
COR_NAVY_ESCURO = "#0D1938"   # Variação mais escura (sombras / hover)
COR_BRANCO = "#FFFFFF"
COR_FUNDO_APP = "#F2F3F5"     # Fundo cinza claro da janela
COR_CARD = "#FFFFFF"          # Fundo do cartão central
COR_BORDA_CARD = "#E1E3E8"
COR_TEXTO_TITULO = "#111827"
COR_TEXTO_SUBTITULO = "#6B7280"
COR_TEXTO_LABEL = "#1F2937"
COR_TEXTO_CINZA = "#8A8A8A"
COR_PLACEHOLDER = "#9CA3AF"
COR_ENTRY_BORDA = "#D9DCE1"
COR_BOTAO_PRIMARIO = "#12224E"
COR_BOTAO_PRIMARIO_HOVER = "#0D1938"
COR_BOTAO_SECUNDARIO = "#FFFFFF"
COR_BOTAO_SECUNDARIO_HOVER = "#F0F1F3"
COR_BOTAO_SECUNDARIO_BORDA = "#D9DCE1"

# ---------------------------------------------------------------------------
# Fontes da interface (CustomTkinter)
# ---------------------------------------------------------------------------
FONTE_FAMILIA = "Segoe UI"
FONTE_TITULO = (FONTE_FAMILIA, 22, "bold")
FONTE_SUBTITULO = (FONTE_FAMILIA, 13, "normal")
FONTE_SECAO = (FONTE_FAMILIA, 13, "bold")
FONTE_LABEL_CAMPO = (FONTE_FAMILIA, 12, "bold")
FONTE_ENTRY = (FONTE_FAMILIA, 13, "normal")
FONTE_BOTAO = (FONTE_FAMILIA, 13, "bold")
FONTE_RODAPE = (FONTE_FAMILIA, 10, "normal")

# ---------------------------------------------------------------------------
# Fontes da etiqueta (ReportLab - fontes internas padrão, sempre disponíveis
# sem precisar embutir arquivos .ttf, garantindo 100% de funcionamento offline)
# ---------------------------------------------------------------------------
FONTE_PDF_REGULAR = "Helvetica"
FONTE_PDF_BOLD = "Helvetica-Bold"

# ---------------------------------------------------------------------------
# Dimensões da janela
# ---------------------------------------------------------------------------
JANELA_LARGURA = 460
JANELA_ALTURA = 860

# ---------------------------------------------------------------------------
# Dimensões físicas da etiqueta (em mm) - tamanho real de impressão
# ---------------------------------------------------------------------------
ETIQUETA_LARGURA_MM = 210
ETIQUETA_ALTURA_MM = 110
ETIQUETA_LARGURA_PT = ETIQUETA_LARGURA_MM * mm
ETIQUETA_ALTURA_PT = ETIQUETA_ALTURA_MM * mm

# ---------------------------------------------------------------------------
# Textos de placeholder dos campos (idênticos à referência)
# ---------------------------------------------------------------------------
PLACEHOLDER_CLIENTE = "Nome do cliente"
PLACEHOLDER_CIDADE = "Cidade"
PLACEHOLDER_PEDIDO = "Número do pedido"
PLACEHOLDER_PRODUTO = "Produto"
PLACEHOLDER_UNIDADES = "Ex: 15"
PLACEHOLDER_METROS = "Ex: 40,65"
PLACEHOLDER_OBSERVACAO = "Observação (opcional)"

# ---------------------------------------------------------------------------
# Pasta temporária para PDFs gerados na hora de imprimir
# ---------------------------------------------------------------------------
import os
import tempfile

PASTA_TEMP = os.path.join(tempfile.gettempdir(), "GeradorEtiquetas")
os.makedirs(PASTA_TEMP, exist_ok=True)
