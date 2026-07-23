# -*- coding: utf-8 -*-
"""
pdf.py
------
Desenho vetorial da etiqueta e geração do PDF final.

A etiqueta é desenhada inteiramente por coordenadas (retângulos, linhas e
textos) usando ReportLab - nenhuma imagem/captura de tela é usada em
nenhum momento, garantindo impressão nítida em qualquer resolução.

A mesma função `desenhar_etiqueta()` é reaproveitada tanto para exportar
o PDF quanto para gerar o arquivo que será enviado à impressora
(módulo printer.py), garantindo que os dois resultados sejam idênticos.
"""

import re
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

import config
import icons


def formatar_metros(texto: str) -> str:
    """
    Recebe o texto digitado no campo Metros (ex: "40,65" ou "40,65 m²") e
    garante que o sufixo "m²" apareça exatamente uma vez na etiqueta.
    """
    texto = (texto or "").strip()
    if not texto:
        return "-"

    padrao = re.compile(r"\s*M[²2]?\s*$", re.IGNORECASE)
    numero = padrao.sub("", texto).strip()
    if not numero:
        return "-"
    return f"{numero} m²"


def formatar_unidades(texto: str) -> str:
    """Recebe o texto digitado no campo Unidades e devolve pronto para a etiqueta."""
    texto = (texto or "").strip()
    return texto if texto else "-"


def _fonte_ajustada(c, texto, fonte, tamanho_inicial, largura_maxima, tamanho_minimo=6):
    """Reduz o tamanho da fonte até o texto caber em `largura_maxima`."""
    tam = tamanho_inicial
    while c.stringWidth(texto, fonte, tam) > largura_maxima and tam > tamanho_minimo:
        tam -= 0.4
    return tam


def _texto_e_fonte_ajustados(c, texto, fonte, tamanho_inicial, largura_maxima, tamanho_minimo=6):
    """
    Reduz a fonte até `tamanho_minimo` e, se mesmo assim o texto não
    couber (nomes muito longos), trunca com reticências. Sem isso um
    texto extremo (ex: nome de cliente muito comprido) ultrapassaria a
    coluna e sobreporia o ícone/bloco vizinho.
    """
    tam = _fonte_ajustada(c, texto, fonte, tamanho_inicial, largura_maxima, tamanho_minimo)
    if c.stringWidth(texto, fonte, tam) <= largura_maxima:
        return texto, tam

    truncado = texto
    while truncado and c.stringWidth(truncado + "…", fonte, tam) > largura_maxima:
        truncado = truncado[:-1]
    texto_final = f"{truncado.rstrip()}…" if truncado else "…"
    return texto_final, tam


def _texto_multilinha(observacao: str, max_linhas=2):
    """Garante no máximo `max_linhas` para o campo de observação."""
    observacao = (observacao or "").strip()
    if not observacao:
        return [""] * max_linhas
    linhas = observacao.split("\n")
    linhas = linhas[:max_linhas]
    while len(linhas) < max_linhas:
        linhas.append("")
    return linhas


def desenhar_etiqueta(c: canvas.Canvas, dados: dict, largura, altura, origem_x=0, origem_y=0):
    """
    Desenha a etiqueta completa dentro do retângulo
    [origem_x, origem_y, origem_x + largura, origem_y + altura] do canvas `c`.

    dados: {
        "pedido": str, "cliente": str, "cidade": str, "produto": str,
        "unidades": str (ex "15"), "metros": str (ex "40,65" ou "40,65 m²"),
        "observacao": str
    }
    """
    NAVY = HexColor(config.COR_NAVY)
    BRANCO = HexColor(config.COR_BRANCO)
    PRETO = HexColor("#111111")
    CINZA = HexColor(config.COR_TEXTO_CINZA)

    c.saveState()
    c.translate(origem_x, origem_y)

    margem = largura * 0.018
    raio_ext = largura * 0.028

    # ------------------------------------------------------------------
    # Escala tipográfica (todos os tamanhos como fração de `altura`, não
    # da altura de cada linha) - garante uma hierarquia consistente entre
    # os blocos, em vez de cada seção crescer/encolher com sua própria
    # altura de linha:
    #   PEDIDO Nº (hero)  >  PRODUTO  >  UNIDADES/ÁREA TOTAL  >
    #   CLIENTE/CIDADE  >  OBSERVAÇÃO
    # ------------------------------------------------------------------
    TAM_LABEL_HEADER = altura * 0.032       # "PEDIDO Nº" (label branco no cabeçalho)
    TAM_HERO = altura * 0.085                # número do pedido
    TAM_LABEL = altura * 0.027                # CLIENTE/CIDADE/PRODUTO/UNIDADES/ÁREA/OBSERVAÇÃO
    TAM_VALOR_PRODUTO = altura * 0.062         # nome do produto
    TAM_VALOR_STAT = altura * 0.058             # números de unidades / área total
    TAM_VALOR_CLIENTE = altura * 0.048           # cliente / cidade
    TAM_TEXTO_OBS = altura * 0.025                 # texto livre da observação

    # ------------------------------------------------------------------
    # Moldura externa arredondada (recorte visual da etiqueta inteira)
    # ------------------------------------------------------------------
    c.setStrokeColor(NAVY)
    c.setLineWidth(1.1)
    c.roundRect(margem, margem, largura - margem * 2, altura - margem * 2, raio_ext, fill=0, stroke=1)

    x0 = margem
    x1 = largura - margem
    largura_util = x1 - x0

    # ------------------------------------------------------------------
    # 1) CABEÇALHO - PEDIDO Nº
    # ------------------------------------------------------------------
    h_header = altura * 0.165
    y_header_top = altura - margem
    y_header_bottom = y_header_top - h_header

    p = c.beginPath()
    r = raio_ext
    p.moveTo(x0, y_header_bottom)
    p.lineTo(x0, y_header_top - r)
    p.curveTo(x0, y_header_top, x0, y_header_top, x0 + r, y_header_top)
    p.lineTo(x1 - r, y_header_top)
    p.curveTo(x1, y_header_top, x1, y_header_top, x1, y_header_top - r)
    p.lineTo(x1, y_header_bottom)
    p.close()
    c.setFillColor(NAVY)
    c.drawPath(p, fill=1, stroke=0)

    # Ícone de pacote
    icone_tam = h_header * 0.62
    icone_x = x0 + largura_util * 0.025
    icone_y = y_header_bottom + (h_header - icone_tam) / 2
    icons.icone_pacote(c, icone_x, icone_y, icone_tam, cor_fundo=None, cor_icone=config.COR_BRANCO)

    # Texto "PEDIDO Nº"
    label_x = icone_x + icone_tam + largura_util * 0.025
    c.setFillColor(BRANCO)
    c.setFont(config.FONTE_PDF_BOLD, TAM_LABEL_HEADER)
    meio_header_y = y_header_bottom + h_header / 2
    c.drawString(label_x, meio_header_y - h_header * 0.07, "PEDIDO Nº")

    # Linha divisória vertical
    divisor_x = label_x + largura_util * 0.235
    c.setStrokeColor(BRANCO)
    c.setLineWidth(1)
    c.line(divisor_x, y_header_bottom + h_header * 0.18, divisor_x, y_header_top - h_header * 0.18)

    # Número do pedido (grande, com ajuste automático se for muito longo)
    pedido_txt = dados.get("pedido") or "-"
    largura_pedido_disp = (x1 - (divisor_x + largura_util * 0.02)) * 0.97
    tam_pedido = _fonte_ajustada(c, pedido_txt, config.FONTE_PDF_BOLD, TAM_HERO, largura_pedido_disp, tamanho_minimo=10)
    c.setFont(config.FONTE_PDF_BOLD, tam_pedido)
    c.drawString(divisor_x + largura_util * 0.02, meio_header_y - h_header * 0.16, pedido_txt)

    # ------------------------------------------------------------------
    # 2) LINHA CLIENTE / CIDADE
    # ------------------------------------------------------------------
    h_row2 = altura * 0.180
    y2_top = y_header_bottom
    y2_bottom = y2_top - h_row2

    c.setStrokeColor(NAVY)
    c.setLineWidth(0.8)
    c.line(x0, y2_bottom, x1, y2_bottom)  # linha inferior da seção

    meio_x = x0 + largura_util * 0.5

    # --- Bloco CLIENTE (esquerda) ---
    ic_tam = h_row2 * 0.60
    ic_x = x0 + largura_util * 0.025
    ic_y = y2_bottom + (h_row2 - ic_tam) / 2
    icons.icone_pessoa(c, ic_x, ic_y, ic_tam, cor_fundo=config.COR_NAVY, cor_icone=config.COR_BRANCO)

    texto_x = ic_x + ic_tam + largura_util * 0.02
    c.setFillColor(NAVY)
    c.setFont(config.FONTE_PDF_BOLD, TAM_LABEL)
    c.drawString(texto_x, y2_bottom + h_row2 * 0.60, "CLIENTE")
    cliente_txt = (dados.get("cliente") or "-").upper()
    largura_cliente_disp = (meio_x - texto_x) * 0.97
    cliente_txt, tam_cliente = _texto_e_fonte_ajustados(
        c, cliente_txt, config.FONTE_PDF_BOLD, TAM_VALOR_CLIENTE, largura_cliente_disp, tamanho_minimo=7
    )
    c.setFillColor(PRETO)
    c.setFont(config.FONTE_PDF_BOLD, tam_cliente)
    c.drawString(texto_x, y2_bottom + h_row2 * 0.20, cliente_txt)

    # Divisor vertical central
    c.setStrokeColor(NAVY)
    c.setLineWidth(0.8)
    c.line(meio_x, y2_bottom + h_row2 * 0.12, meio_x, y2_top - h_row2 * 0.12)

    # --- Bloco CIDADE (direita) ---
    ic2_x = meio_x + largura_util * 0.035
    icons.icone_pin(c, ic2_x, ic_y, ic_tam, cor_fundo=config.COR_NAVY, cor_icone=config.COR_BRANCO)

    texto2_x = ic2_x + ic_tam + largura_util * 0.02
    c.setFillColor(NAVY)
    c.setFont(config.FONTE_PDF_BOLD, TAM_LABEL)
    c.drawString(texto2_x, y2_bottom + h_row2 * 0.60, "CIDADE")
    cidade_txt = (dados.get("cidade") or "-").upper()
    largura_cidade_disp = (x1 - texto2_x) * 0.97
    cidade_txt, tam_cidade = _texto_e_fonte_ajustados(
        c, cidade_txt, config.FONTE_PDF_BOLD, TAM_VALOR_CLIENTE, largura_cidade_disp, tamanho_minimo=7
    )
    c.setFillColor(PRETO)
    c.setFont(config.FONTE_PDF_BOLD, tam_cidade)
    c.drawString(texto2_x, y2_bottom + h_row2 * 0.20, cidade_txt)

    # ------------------------------------------------------------------
    # 3) LINHA PRODUTO
    # ------------------------------------------------------------------
    h_row3 = altura * 0.195
    y3_top = y2_bottom
    y3_bottom = y3_top - h_row3
    caixa_margem = largura_util * 0.025

    ic3_tam = h_row3 * 0.86
    c.setFillColor(NAVY)
    c.roundRect(x0 + caixa_margem, y3_bottom + (h_row3 - ic3_tam) / 2, ic3_tam, ic3_tam, ic3_tam * 0.22, fill=1, stroke=0)
    icons.icone_produto(c, x0 + caixa_margem, y3_bottom + (h_row3 - ic3_tam) / 2, ic3_tam,
                         cor_fundo=None, cor_icone=config.COR_BRANCO)

    caixa_x = x0 + caixa_margem + ic3_tam
    caixa_w = x1 - caixa_margem - caixa_x
    c.setStrokeColor(NAVY)
    c.setLineWidth(0.9)
    c.roundRect(caixa_x, y3_bottom + largura_util * 0.006, caixa_w, h_row3 - largura_util * 0.012, raio_ext * 0.5, fill=0, stroke=1)

    centro_caixa_x = caixa_x + caixa_w / 2
    c.setFillColor(NAVY)
    c.setFont(config.FONTE_PDF_BOLD, TAM_LABEL)
    c.drawCentredString(centro_caixa_x, y3_bottom + h_row3 * 0.68, "PRODUTO")

    c.setFillColor(PRETO)
    produto_txt = (dados.get("produto") or "-").upper()
    largura_disponivel = caixa_w * 0.94
    produto_txt, tam_fonte = _texto_e_fonte_ajustados(
        c, produto_txt, config.FONTE_PDF_BOLD, TAM_VALOR_PRODUTO, largura_disponivel
    )
    c.setFont(config.FONTE_PDF_BOLD, tam_fonte)
    c.drawCentredString(centro_caixa_x, y3_bottom + h_row3 * 0.26, produto_txt)

    # ------------------------------------------------------------------
    # 4) LINHA UNIDADES / ÁREA TOTAL (METROS)
    # ------------------------------------------------------------------
    h_row4 = altura * 0.175
    y4_top = y3_bottom
    y4_bottom = y4_top - h_row4

    ic4_tam = h_row4 * 0.86
    c.setFillColor(NAVY)
    c.roundRect(x0 + caixa_margem, y4_bottom + (h_row4 - ic4_tam) / 2, ic4_tam, ic4_tam, ic4_tam * 0.22, fill=1, stroke=0)
    icons.icone_caixa_aberta(c, x0 + caixa_margem, y4_bottom + (h_row4 - ic4_tam) / 2, ic4_tam,
                              cor_fundo=None, cor_icone=config.COR_BRANCO)

    caixa4_x = caixa_x
    caixa4_w = caixa_w
    c.setStrokeColor(NAVY)
    c.setLineWidth(0.9)
    c.roundRect(caixa4_x, y4_bottom + largura_util * 0.006, caixa4_w, h_row4 - largura_util * 0.012, raio_ext * 0.5, fill=0, stroke=1)

    unidades_str = formatar_unidades(dados.get("unidades"))
    area_str = formatar_metros(dados.get("metros"))
    meio4_x = caixa4_x + caixa4_w / 2
    c.setStrokeColor(NAVY)
    c.setLineWidth(0.8)
    c.line(meio4_x, y4_bottom + h_row4 * 0.14, meio4_x, y4_top - h_row4 * 0.14)

    quarto1_x = caixa4_x + caixa4_w * 0.27
    quarto2_x = caixa4_x + caixa4_w * 0.73

    c.setFillColor(PRETO)
    c.setFont(config.FONTE_PDF_BOLD, TAM_VALOR_STAT)
    c.drawCentredString(quarto1_x, y4_bottom + h_row4 * 0.44, unidades_str)
    c.setFillColor(CINZA)
    c.setFont(config.FONTE_PDF_BOLD, TAM_LABEL)
    c.drawCentredString(quarto1_x, y4_bottom + h_row4 * 0.20, "UNIDADES")

    c.setFillColor(PRETO)
    c.setFont(config.FONTE_PDF_BOLD, TAM_VALOR_STAT)
    c.drawCentredString(quarto2_x, y4_bottom + h_row4 * 0.44, area_str)
    c.setFillColor(CINZA)
    c.setFont(config.FONTE_PDF_BOLD, TAM_LABEL)
    c.drawCentredString(quarto2_x, y4_bottom + h_row4 * 0.20, "ÁREA TOTAL")

    # ------------------------------------------------------------------
    # 5) LINHA OBSERVAÇÃO
    # ------------------------------------------------------------------
    h_row5 = altura * 0.140
    y5_top = y4_bottom
    y5_bottom = y5_top - h_row5

    ic5_tam = h_row5 * 0.86
    c.setFillColor(NAVY)
    c.roundRect(x0 + caixa_margem, y5_bottom + (h_row5 - ic5_tam) / 2, ic5_tam, ic5_tam, ic5_tam * 0.22, fill=1, stroke=0)
    icons.icone_clipboard(c, x0 + caixa_margem, y5_bottom + (h_row5 - ic5_tam) / 2, ic5_tam,
                           cor_fundo=None, cor_icone=config.COR_BRANCO)

    obs_x = caixa_x
    c.setFillColor(NAVY)
    c.setFont(config.FONTE_PDF_BOLD, TAM_LABEL)
    c.drawString(obs_x, y5_bottom + h_row5 * 0.68, "OBSERVAÇÃO")

    linhas = _texto_multilinha(dados.get("observacao"), max_linhas=2)
    c.setStrokeColor(HexColor("#9AA0AC"))
    c.setLineWidth(0.6)
    c.setFillColor(PRETO)
    c.setFont(config.FONTE_PDF_REGULAR, TAM_TEXTO_OBS)
    linha_y_1 = y5_bottom + h_row5 * 0.32
    linha_y_2 = y5_bottom + h_row5 * 0.06
    c.drawString(obs_x + 2, linha_y_1 + 1.5, linhas[0])
    c.line(obs_x, linha_y_1, x1 - caixa_margem, linha_y_1)
    c.drawString(obs_x + 2, linha_y_2 + 1.5, linhas[1])
    c.line(obs_x, linha_y_2, x1 - caixa_margem, linha_y_2)

    # ------------------------------------------------------------------
    # 6) RODAPÉ (duas linhas de texto centralizadas)
    # ------------------------------------------------------------------
    h_rodape = y5_bottom - margem  # área realmente reservada para o rodapé
    y_rodape_topo = y5_bottom

    c.setStrokeColor(HexColor("#D9DCE1"))
    c.setLineWidth(0.6)
    c.line(x0 + largura_util * 0.06, y_rodape_topo, x1 - largura_util * 0.06, y_rodape_topo)

    centro_x = x0 + largura_util / 2
    largura_disp_rodape = largura_util * 0.9

    texto_direitos = f"© {config.ANO_COPYRIGHT} {config.AUTOR_NOME}. Todos os direitos reservados."
    texto_github = config.AUTOR_GITHUB

    tam_direitos = _fonte_ajustada(
        c, texto_direitos, config.FONTE_PDF_REGULAR, h_rodape * 0.34, largura_disp_rodape, tamanho_minimo=6
    )
    tam_github = _fonte_ajustada(
        c, texto_github, config.FONTE_PDF_REGULAR, h_rodape * 0.34, largura_disp_rodape, tamanho_minimo=6
    )

    c.setFillColor(HexColor("#4B5563"))
    c.setFont(config.FONTE_PDF_REGULAR, tam_direitos)
    c.drawCentredString(centro_x, margem + h_rodape * 0.56, texto_direitos)

    c.setFont(config.FONTE_PDF_REGULAR, tam_github)
    c.drawCentredString(centro_x, margem + h_rodape * 0.18, texto_github)

    c.restoreState()


def gerar_pdf_etiqueta(caminho_arquivo: str, dados: dict):
    """
    Gera um PDF em alta resolução com o tamanho REAL da etiqueta
    (sem margens de página, sem redimensionamento).
    """
    largura = config.ETIQUETA_LARGURA_PT
    altura = config.ETIQUETA_ALTURA_PT

    c = canvas.Canvas(caminho_arquivo, pagesize=(largura, altura))
    c.setTitle(f"Etiqueta - Pedido {dados.get('pedido', '')}")
    desenhar_etiqueta(c, dados, largura, altura)
    c.showPage()
    c.save()
    return caminho_arquivo
