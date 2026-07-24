# -*- coding: utf-8 -*-
import re
import random
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
from reportlab.graphics.barcode import code128

import config
import icons

def _numero_aleatorio_codigo_barras() -> str:
    """Gera um número de 12 dígitos aleatórios (decorativo, sem significado real)."""
    return f"{random.randint(100000000000, 999999999999)}"

def desenhar_qrcode(c, url: str, x: float, y: float, tamanho: float):
    """
    Desenha um QR code 100% vetorial (sem PNG intermediário) apontando
    para `url`, ocupando um quadrado de `tamanho` x `tamanho` com o
    canto inferior esquerdo em (x, y). Por ser vetor, nunca fica
    borrado nem pixelizado, em qualquer resolução de impressão.
    """
    qr = QrCodeWidget(url, barLevel="M")
    x0_bounds, y0_bounds, x1_bounds, y1_bounds = qr.getBounds()
    largura_nativa = x1_bounds - x0_bounds
    altura_nativa = y1_bounds - y0_bounds
    desenho = Drawing(
        tamanho, tamanho,
        transform=[tamanho / largura_nativa, 0, 0, tamanho / altura_nativa, 0, 0],
    )
    desenho.add(qr)
    renderPDF.draw(desenho, c, x, y)

def desenhar_codigo_barras(c, valor: str, x_centro: float, y: float, largura_alvo: float, altura_barras: float):
    """
    Desenha um código de barras Code128 100% vetorial, centralizado em
    `x_centro`, com o número `valor`, ajustado para ocupar exatamente
    `largura_alvo` de largura e `altura_barras` de altura.
    """
    referencia = code128.Code128(valor, barWidth=1.0, barHeight=altura_barras, quiet=0, humanReadable=False)
    fator = (largura_alvo / referencia.width) if referencia.width else 1.0
    barras = code128.Code128(valor, barWidth=fator, barHeight=altura_barras, quiet=0, humanReadable=False)
    barras.drawOn(c, x_centro - barras.width / 2, y)
    return barras.width

def formatar_metros(texto: str) -> str:
    texto = (texto or "").strip()
    if not texto: return "-"
    padrao = re.compile(r"\s*M[²2]?\s*$", re.IGNORECASE)
    numero = padrao.sub("", texto).strip()
    if not numero: return "-"
    return f"{numero} m²"

def formatar_unidades(texto: str) -> str:
    texto = (texto or "").strip()
    return texto if texto else "-"

def _fonte_ajustada(c, texto, fonte, tamanho_inicial, largura_maxima, tamanho_minimo=6):
    tam = tamanho_inicial
    while c.stringWidth(texto, fonte, tam) > largura_maxima and tam > tamanho_minimo:
        tam -= 0.4
    return tam

def _texto_e_fonte_ajustados(c, texto, fonte, tamanho_inicial, largura_maxima, tamanho_minimo=6):
    tam = _fonte_ajustada(c, texto, fonte, tamanho_inicial, largura_maxima, tamanho_minimo)
    if c.stringWidth(texto, fonte, tam) <= largura_maxima:
        return texto, tam
    truncado = texto
    while truncado and c.stringWidth(truncado + "…", fonte, tam) > largura_maxima:
        truncado = truncado[:-1]
    texto_final = f"{truncado.rstrip()}…" if truncado else "…"
    return texto_final, tam

def _texto_multilinha(observacao: str, max_linhas=2):
    observacao = (observacao or "").strip()
    if not observacao:
        return [""] * max_linhas
    linhas = observacao.split("\n")
    linhas = linhas[:max_linhas]
    while len(linhas) < max_linhas:
        linhas.append("")
    return linhas

def desenhar_etiqueta(c: canvas.Canvas, dados: dict, largura, altura, origem_x=0, origem_y=0):
    NAVY = HexColor(config.COR_NAVY)
    BRANCO = HexColor(config.COR_BRANCO)
    PRETO = HexColor("#111111")
    CINZA = HexColor(config.COR_TEXTO_CINZA)

    c.saveState()
    c.translate(origem_x, origem_y)

    margem = largura * 0.018
    raio_ext = largura * 0.028

    TAM_LABEL_HEADER = altura * 0.038
    TAM_HERO = altura * 0.100
    TAM_LABEL = altura * 0.030
    TAM_VALOR_PRODUTO = altura * 0.075
    TAM_VALOR_STAT = altura * 0.070
    TAM_VALOR_CLIENTE = altura * 0.055
    TAM_TEXTO_OBS = altura * 0.030

    # Moldura
    c.setStrokeColor(NAVY)
    c.setLineWidth(1.1)
    c.roundRect(margem, margem, largura - margem * 2, altura - margem * 2, raio_ext, fill=0, stroke=1)

    x0 = margem
    x1 = largura - margem
    largura_util_total = x1 - x0

    # Painel direito e esquerdo
    painel_dir_w = largura_util_total * 0.25
    largura_util = largura_util_total - painel_dir_w
    linha_div_x = x0 + largura_util
    
    # 1) CABEÇALHO
    h_header = altura * 0.18
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

    icone_tam = h_header * 0.62
    icone_x = x0 + largura_util_total * 0.025
    icone_y = y_header_bottom + (h_header - icone_tam) / 2
    icons.icone_pacote(c, icone_x, icone_y, icone_tam, cor_fundo=None, cor_icone=config.COR_BRANCO)

    label_x = icone_x + icone_tam + largura_util_total * 0.025
    c.setFillColor(BRANCO)
    c.setFont(config.FONTE_PDF_BOLD, TAM_LABEL_HEADER)
    meio_header_y = y_header_bottom + h_header / 2
    c.drawString(label_x, meio_header_y - h_header * 0.07, "PEDIDO Nº")

    divisor_x = label_x + largura_util_total * 0.18
    c.setStrokeColor(BRANCO)
    c.setLineWidth(1)
    c.line(divisor_x, y_header_bottom + h_header * 0.18, divisor_x, y_header_top - h_header * 0.18)

    pedido_txt = dados.get("pedido") or "-"
    largura_pedido_disp = (x1 - (divisor_x + largura_util_total * 0.02)) * 0.97
    tam_pedido = _fonte_ajustada(c, pedido_txt, config.FONTE_PDF_BOLD, TAM_HERO, largura_pedido_disp, tamanho_minimo=10)
    c.setFont(config.FONTE_PDF_BOLD, tam_pedido)
    c.drawString(divisor_x + largura_util_total * 0.02, meio_header_y - h_header * 0.16, pedido_txt)

    # 6) RODAPÉ (Calculado antes para saber o espaço do corpo)
    h_rodape = altura * 0.10
    y_rodape_topo = margem + h_rodape

    # Linha vertical divisória do painel direito
    c.setStrokeColor(NAVY)
    c.setLineWidth(0.8)
    c.line(linha_div_x, y_rodape_topo, linha_div_x, y_header_bottom)

    # Divisão do Corpo (4 linhas iguais)
    h_body = y_header_bottom - y_rodape_topo
    h_row = h_body / 4.0
    
    # MEDIDAS FIXAS PARA TODAS AS CAIXAS (Garante alinhamento perfeito!)
    tamanho_box_icone = h_row * 0.70
    caixa_margem = largura_util * 0.025
    caixa_x = x0 + caixa_margem + tamanho_box_icone
    caixa_w = linha_div_x - caixa_margem - caixa_x
    box_padding_y = h_row * 0.08
    box_h = h_row - (box_padding_y * 2)

    # --- LINHA 1: CLIENTE / CIDADE ---
    y_linha1 = y_header_bottom - h_row
    c.setStrokeColor(NAVY)
    c.setLineWidth(0.8)
    c.line(x0, y_linha1, linha_div_x, y_linha1) 

    meio_x = x0 + largura_util * 0.5
    ic_y = y_linha1 + (h_row - tamanho_box_icone) / 2
    
    # Cliente
    icons.icone_pessoa(c, x0 + caixa_margem, ic_y, tamanho_box_icone, cor_fundo=config.COR_NAVY, cor_icone=config.COR_BRANCO)
    texto_x = x0 + caixa_margem + tamanho_box_icone + (largura_util * 0.02)
    c.setFillColor(NAVY)
    c.setFont(config.FONTE_PDF_BOLD, TAM_LABEL)
    c.drawString(texto_x, y_linha1 + h_row * 0.60, "CLIENTE")
    cliente_txt = (dados.get("cliente") or "-").upper()
    largura_cliente_disp = (meio_x - texto_x) * 0.95
    cliente_txt, tam_cliente = _texto_e_fonte_ajustados(c, cliente_txt, config.FONTE_PDF_BOLD, TAM_VALOR_CLIENTE, largura_cliente_disp, 7)
    c.setFillColor(PRETO)
    c.setFont(config.FONTE_PDF_BOLD, tam_cliente)
    c.drawString(texto_x, y_linha1 + h_row * 0.20, cliente_txt)

    # Divisor Cliente/Cidade
    c.setStrokeColor(NAVY)
    c.setLineWidth(0.8)
    c.line(meio_x, y_linha1 + h_row * 0.12, meio_x, y_header_bottom - h_row * 0.12)

    # Cidade
    ic2_x = meio_x + (largura_util * 0.025)
    icons.icone_pin(c, ic2_x, ic_y, tamanho_box_icone, cor_fundo=config.COR_NAVY, cor_icone=config.COR_BRANCO)
    texto2_x = ic2_x + tamanho_box_icone + (largura_util * 0.02)
    c.setFillColor(NAVY)
    c.setFont(config.FONTE_PDF_BOLD, TAM_LABEL)
    c.drawString(texto2_x, y_linha1 + h_row * 0.60, "CIDADE")
    cidade_txt = (dados.get("cidade") or "-").upper()
    largura_cidade_disp = (linha_div_x - texto2_x) * 0.95
    cidade_txt, tam_cidade = _texto_e_fonte_ajustados(c, cidade_txt, config.FONTE_PDF_BOLD, TAM_VALOR_CLIENTE, largura_cidade_disp, 7)
    c.setFillColor(PRETO)
    c.setFont(config.FONTE_PDF_BOLD, tam_cidade)
    c.drawString(texto2_x, y_linha1 + h_row * 0.20, cidade_txt)

    # --- LINHA 2: PRODUTO ---
    y_linha2 = y_linha1 - h_row
    ic_y = y_linha2 + (h_row - tamanho_box_icone) / 2
    c.setFillColor(NAVY)
    c.roundRect(x0 + caixa_margem, ic_y, tamanho_box_icone, tamanho_box_icone, tamanho_box_icone * 0.22, fill=1, stroke=0)
    icons.icone_produto(c, x0 + caixa_margem, ic_y, tamanho_box_icone, cor_fundo=None, cor_icone=config.COR_BRANCO)
    
    c.setStrokeColor(NAVY)
    c.setLineWidth(0.9)
    c.roundRect(caixa_x, y_linha2 + box_padding_y, caixa_w, box_h, raio_ext * 0.5, fill=0, stroke=1)
    
    centro_caixa_x = caixa_x + caixa_w / 2
    c.setFillColor(NAVY)
    c.setFont(config.FONTE_PDF_BOLD, TAM_LABEL)
    c.drawString(caixa_x + (caixa_w*0.02), y_linha2 + h_row * 0.65, "PRODUTO")
    
    c.setFillColor(PRETO)
    produto_txt = (dados.get("produto") or "-").upper()
    largura_disponivel = caixa_w * 0.96
    produto_txt, tam_fonte = _texto_e_fonte_ajustados(c, produto_txt, config.FONTE_PDF_BOLD, TAM_VALOR_PRODUTO, largura_disponivel)
    c.setFont(config.FONTE_PDF_BOLD, tam_fonte)
    c.drawCentredString(centro_caixa_x, y_linha2 + h_row * 0.22, produto_txt)

    # --- LINHA 3: UNIDADES / ÁREA ---
    y_linha3 = y_linha2 - h_row
    ic_y = y_linha3 + (h_row - tamanho_box_icone) / 2
    c.setFillColor(NAVY)
    c.roundRect(x0 + caixa_margem, ic_y, tamanho_box_icone, tamanho_box_icone, tamanho_box_icone * 0.22, fill=1, stroke=0)
    icons.icone_caixa_aberta(c, x0 + caixa_margem, ic_y, tamanho_box_icone, cor_fundo=None, cor_icone=config.COR_BRANCO)
    
    c.setStrokeColor(NAVY)
    c.setLineWidth(0.9)
    c.roundRect(caixa_x, y_linha3 + box_padding_y, caixa_w, box_h, raio_ext * 0.5, fill=0, stroke=1)

    unidades_str = formatar_unidades(dados.get("unidades"))
    area_str = formatar_metros(dados.get("metros"))
    meio4_x = caixa_x + caixa_w / 2
    c.setStrokeColor(NAVY)
    c.setLineWidth(0.8)
    c.line(meio4_x, y_linha3 + h_row * 0.14, meio4_x, y_linha2 - h_row * 0.14)

    quarto1_x = caixa_x + caixa_w * 0.25
    quarto2_x = caixa_x + caixa_w * 0.75

    c.setFillColor(PRETO)
    c.setFont(config.FONTE_PDF_BOLD, TAM_VALOR_STAT)
    c.drawCentredString(quarto1_x, y_linha3 + h_row * 0.40, unidades_str)
    c.setFillColor(CINZA)
    c.setFont(config.FONTE_PDF_BOLD, TAM_LABEL)
    c.drawCentredString(quarto1_x, y_linha3 + h_row * 0.12, "CAIXAS")

    c.setFillColor(PRETO)
    c.setFont(config.FONTE_PDF_BOLD, TAM_VALOR_STAT)
    c.drawCentredString(quarto2_x, y_linha3 + h_row * 0.40, area_str)
    c.setFillColor(CINZA)
    c.setFont(config.FONTE_PDF_BOLD, TAM_LABEL)
    c.drawCentredString(quarto2_x, y_linha3 + h_row * 0.12, "METROS QUADRADOS")

    # --- LINHA 4: OBSERVAÇÃO ---
    y_linha4 = y_linha3 - h_row
    ic_y = y_linha4 + (h_row - tamanho_box_icone) / 2
    c.setFillColor(NAVY)
    c.roundRect(x0 + caixa_margem, ic_y, tamanho_box_icone, tamanho_box_icone, tamanho_box_icone * 0.22, fill=1, stroke=0)
    icons.icone_clipboard(c, x0 + caixa_margem, ic_y, tamanho_box_icone, cor_fundo=None, cor_icone=config.COR_BRANCO)
    
    c.setStrokeColor(NAVY)
    c.setLineWidth(0.9)
    c.roundRect(caixa_x, y_linha4 + box_padding_y, caixa_w, box_h, raio_ext * 0.5, fill=0, stroke=1)

    c.setFillColor(NAVY)
    c.setFont(config.FONTE_PDF_BOLD, TAM_LABEL)
    c.drawString(caixa_x + (caixa_w*0.02), y_linha4 + h_row * 0.65, "OBSERVAÇÃO")

    linhas = _texto_multilinha(dados.get("observacao"), max_linhas=2)
    c.setStrokeColor(HexColor("#9AA0AC"))
    c.setLineWidth(0.6)
    c.setFillColor(PRETO)
    c.setFont(config.FONTE_PDF_REGULAR, TAM_TEXTO_OBS)
    linha_y_1 = y_linha4 + h_row * 0.35
    linha_y_2 = y_linha4 + h_row * 0.15
    
    text_start_x = caixa_x + (caixa_w*0.02)
    line_start_x = caixa_x + (caixa_w*0.02)
    line_end_x = caixa_x + caixa_w - (caixa_w*0.02)
    
    c.drawString(text_start_x, linha_y_1 + 2, linhas[0])
    c.line(line_start_x, linha_y_1, line_end_x, linha_y_1)
    c.drawString(text_start_x, linha_y_2 + 2, linhas[1])
    c.line(line_start_x, linha_y_2, line_end_x, linha_y_2)

    # --- PAINEL DIREITO: QR code (vetorial, aponta para o GitHub) + ---
    # --- código de barras (vetorial, número aleatório decorativo)   ---
    # Posicionamento sequencial de cima para baixo: cada elemento é
    # posicionado a partir do fim do anterior, então a linha divisória
    # nunca pode cair em cima do QR code (correção do bug reportado).
    centro_painel_x = linha_div_x + (painel_dir_w / 2)
    painel_top = y_header_bottom
    painel_bottom = y_rodape_topo
    painel_h = painel_top - painel_bottom
    largura_conteudo_painel = painel_dir_w * 0.82

    cursor_y = painel_top - painel_h * 0.095

    tam_qr = min(painel_h * 0.35, painel_dir_w * 0.82)
    cursor_y -= tam_qr
    qr_y = cursor_y
    desenhar_qrcode(c, config.AUTOR_GITHUB_URL, centro_painel_x - tam_qr / 2, qr_y, tam_qr)

    cursor_y -= painel_h * 0.03
    tam_label_git = TAM_LABEL * 0.85
    cursor_y -= tam_label_git * 0.9
    c.setFillColor(PRETO)
    c.setFont(config.FONTE_PDF_BOLD, tam_label_git)
    c.drawCentredString(centro_painel_x, cursor_y, "GitHub:")

    cursor_y -= tam_label_git * 1.15
    texto_url, tam_url = _texto_e_fonte_ajustados(
        c, config.AUTOR_GITHUB, config.FONTE_PDF_REGULAR, tam_label_git, largura_conteudo_painel, tamanho_minimo=5
    )
    c.setFont(config.FONTE_PDF_REGULAR, tam_url)
    c.drawCentredString(centro_painel_x, cursor_y, texto_url)

    # Linha divisória - sempre calculada DEPOIS do bloco do QR, então
    # nunca mais vai se sobrepor a ele.
    cursor_y -= painel_h * 0.05
    c.setStrokeColor(HexColor("#D9DCE1"))
    c.setLineWidth(1)
    c.line(linha_div_x + painel_dir_w * 0.12, cursor_y, x1 - painel_dir_w * 0.12, cursor_y)
    cursor_y -= painel_h * 0.05

    tam_bc_h = painel_h * 0.155
    cursor_y -= tam_bc_h
    bc_y = cursor_y
    numero_barras = _numero_aleatorio_codigo_barras()
    desenhar_codigo_barras(c, numero_barras, centro_painel_x, bc_y, largura_conteudo_painel, tam_bc_h)

    cursor_y -= painel_h * 0.035
    tam_label_bc = TAM_LABEL * 0.82
    cursor_y -= tam_label_bc * 0.9
    c.setFillColor(HexColor(config.COR_TEXTO_CINZA))
    c.setFont(config.FONTE_PDF_BOLD, tam_label_bc)
    c.drawCentredString(centro_painel_x, cursor_y, "CÓDIGO ALEATÓRIO")

    cursor_y -= tam_label_bc * 1.2
    tam_valor_bc = TAM_LABEL * 0.95
    c.setFillColor(PRETO)
    c.setFont(config.FONTE_PDF_BOLD, tam_valor_bc)
    c.drawCentredString(centro_painel_x, cursor_y, numero_barras)

    # 6) RODAPÉ
    c.setStrokeColor(HexColor("#D9DCE1"))
    c.setLineWidth(0.6)
    c.line(x0 + largura_util_total * 0.06, y_rodape_topo, x1 - largura_util_total * 0.06, y_rodape_topo)

    texto_direitos = f"© {config.ANO_COPYRIGHT} {config.AUTOR_NOME}. Todos os direitos reservados."
    tam_direitos = _fonte_ajustada(c, texto_direitos, config.FONTE_PDF_REGULAR, h_rodape * 0.30, largura_util_total * 0.8, tamanho_minimo=6)
    c.setFillColor(HexColor("#4B5563"))
    c.setFont(config.FONTE_PDF_REGULAR, tam_direitos)
    c.drawString(x0 + largura_util_total * 0.18, margem + h_rodape * 0.35, texto_direitos)
    
    c.restoreState()

def gerar_pdf_etiqueta(caminho_arquivo: str, dados: dict):
    largura = config.ETIQUETA_LARGURA_PT
    altura = config.ETIQUETA_ALTURA_PT
    c = canvas.Canvas(caminho_arquivo, pagesize=(largura, altura))
    c.setTitle(f"Etiqueta - Pedido {dados.get('pedido', '')}")
    desenhar_etiqueta(c, dados, largura, altura)
    c.showPage()
    c.save()
    return caminho_arquivo
