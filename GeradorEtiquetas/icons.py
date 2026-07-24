# -*- coding: utf-8 -*-
"""
icons.py
--------
Ícones 100% vetoriais desenhados diretamente no Canvas do ReportLab.

Nenhum arquivo de imagem é usado: cada ícone é composto por formas
geométricas (retângulos, círculos, linhas e curvas) desenhadas por código.
Isso garante que a etiqueta seja impressa em vetor puro, sem qualquer
perda de nitidez, e mantém o projeto 100% offline (sem downloads de ícones).

Cada função recebe:
    c       -> objeto Canvas do ReportLab
    x, y    -> posição do canto inferior esquerdo do "slot" do ícone
    size    -> tamanho do lado do slot quadrado (em pontos)
    cor_fundo -> cor de preenchimento do quadrado de fundo (ou None)
    cor_icone -> cor do desenho do ícone (traço/preenchimento)
"""

from reportlab.lib.colors import HexColor, white


def _fundo(c, x, y, size, cor_fundo, raio=None):
    """
    Desenha o quadrado de fundo arredondado atrás do ícone. O raio é
    proporcional ao tamanho do ícone por padrão (em vez de um valor fixo
    em pontos), para o arredondamento ficar visualmente consistente tanto
    nos ícones pequenos quanto nos grandes da etiqueta.
    """
    if cor_fundo:
        if raio is None:
            raio = size * 0.22
        c.saveState()
        c.setFillColor(HexColor(cor_fundo))
        c.roundRect(x, y, size, size, raio, fill=1, stroke=0)
        c.restoreState()


def icone_pacote(c, x, y, size, cor_fundo=None, cor_icone="#FFFFFF"):
    """Ícone de caixa/pacote 3D (cabeçalho - PEDIDO Nº)."""
    _fundo(c, x, y, size, cor_fundo)
    c.saveState()
    c.setStrokeColor(HexColor(cor_icone))
    c.setFillColor(HexColor(cor_icone))
    c.setLineWidth(max(1.4, size * 0.045))
    c.setLineJoin(1)

    cx, cy = x + size / 2, y + size / 2
    r = size * 0.34

    # Losango externo (vista superior da caixa)
    p = c.beginPath()
    p.moveTo(cx, cy + r)
    p.lineTo(cx + r, cy)
    p.lineTo(cx, cy - r)
    p.lineTo(cx - r, cy)
    p.close()
    c.setFillColor(white)
    c.drawPath(p, fill=0, stroke=1)

    # Linha vertical central (aresta frontal da caixa)
    c.line(cx, cy + r, cx, cy - r)
    # Linhas das abas superiores
    c.line(cx - r * 0.5, cy + r * 0.5, cx, cy)
    c.line(cx + r * 0.5, cy + r * 0.5, cx, cy)
    c.restoreState()


def _borda(c, x, y, size, cor_borda, raio=None, largura=None):
    """
    Desenha apenas o CONTORNO do quadrado de fundo (sem preenchimento).
    Estilo "clássico": muito menos tinta que um quadrado sólido, já que
    apenas a borda fina é impressa em vez da área inteira.
    """
    if cor_borda:
        if raio is None:
            raio = size * 0.22
        if largura is None:
            largura = max(1.0, size * 0.045)
        c.saveState()
        c.setStrokeColor(HexColor(cor_borda))
        c.setLineWidth(largura)
        c.roundRect(x, y, size, size, raio, fill=0, stroke=1)
        c.restoreState()


def icone_pessoa(c, x, y, size, cor_fundo=None, cor_icone="#12224E"):
    """Ícone de grupo de clientes (CLIENTE) - estilo clássico, contorno fino."""
    _borda(c, x, y, size, cor_fundo)
    c.saveState()
    c.setFillColor(HexColor(cor_icone))
    c.setStrokeColor(HexColor(cor_icone))
    cx, cy = x + size / 2, y + size / 2

    def pessoa(dx, escala, base_y):
        r_cabeca = size * 0.115 * escala
        cx_p = cx + dx
        c.circle(cx_p, base_y + size * 0.20 * escala, r_cabeca, fill=1, stroke=0)
        largura = size * 0.30 * escala
        altura = size * 0.20 * escala
        p = c.beginPath()
        p.moveTo(cx_p - largura / 2, base_y)
        p.curveTo(cx_p - largura / 2, base_y + altura,
                  cx_p + largura / 2, base_y + altura,
                  cx_p + largura / 2, base_y)
        p.lineTo(cx_p - largura / 2, base_y)
        p.close()
        c.drawPath(p, fill=1, stroke=0)

    base_y = cy - size * 0.22
    # Pessoas laterais (menores, mais ao fundo)
    pessoa(-size * 0.26, 0.80, base_y + size * 0.02)
    pessoa(size * 0.26, 0.80, base_y + size * 0.02)
    # Pessoa central (maior, por cima)
    pessoa(0, 1.0, base_y)
    c.restoreState()


def icone_pin(c, x, y, size, cor_fundo=None, cor_icone="#12224E"):
    """Ícone de localização/entrega (CIDADE) - pino sobre envelope, estilo clássico."""
    _borda(c, x, y, size, cor_fundo)
    c.saveState()
    cx = x + size / 2

    # Envelope na base (apenas contorno, pouca tinta)
    lw = max(1.0, size * 0.045)
    c.setStrokeColor(HexColor(cor_icone))
    c.setLineWidth(lw)
    c.setLineJoin(1)
    env_w = size * 0.30
    env_y0 = y + size * 0.16
    env_y1 = y + size * 0.36
    c.rect(cx - env_w, env_y0, env_w * 2, env_y1 - env_y0, fill=0, stroke=1)
    c.line(cx - env_w, env_y1, cx, env_y0 + (env_y1 - env_y0) * 0.30)
    c.line(cx + env_w, env_y1, cx, env_y0 + (env_y1 - env_y0) * 0.30)

    # Pino de localização (preenchido, sólido)
    c.setFillColor(HexColor(cor_icone))
    topo = y + size * 0.78
    r = size * 0.18
    p = c.beginPath()
    p.moveTo(cx - r, topo)
    p.curveTo(cx - r, topo + r * 1.55, cx + r, topo + r * 1.55, cx + r, topo)
    p.curveTo(cx + r, topo - r * 0.9, cx, topo - size * 0.36, cx, topo - size * 0.36)
    p.curveTo(cx, topo - size * 0.36, cx - r, topo - r * 0.9, cx - r, topo)
    p.close()
    c.drawPath(p, fill=1, stroke=0)

    # Furo central (vira "buraco" branco)
    c.setFillColor(white)
    c.circle(cx, topo, r * 0.42, fill=1, stroke=0)
    c.restoreState()


def icone_produto(c, x, y, size, cor_fundo=None, cor_icone="#12224E"):
    """Ícone de caixa/produto em 3D com etiqueta (PRODUTO) - estilo clássico."""
    _borda(c, x, y, size, cor_fundo)
    c.saveState()
    c.setFillColor(HexColor(cor_icone))
    c.setStrokeColor(white)
    c.setLineWidth(max(1.0, size * 0.035))
    c.setLineJoin(1)
    cx, cy = x + size / 2, y + size / 2 - size * 0.02
    r = size * 0.30

    # Silhueta do cubo (hexágono) preenchida
    p = c.beginPath()
    p.moveTo(cx, cy + r)
    p.lineTo(cx + r * 0.87, cy + r * 0.5)
    p.lineTo(cx + r * 0.87, cy - r * 0.5)
    p.lineTo(cx, cy - r)
    p.lineTo(cx - r * 0.87, cy - r * 0.5)
    p.lineTo(cx - r * 0.87, cy + r * 0.5)
    p.close()
    c.drawPath(p, fill=1, stroke=0)

    # Linhas internas (separam as 3 faces) na cor de fundo, pouca tinta
    c.line(cx, cy, cx, cy + r)
    c.line(cx, cy, cx + r * 0.87, cy + r * 0.5)
    c.line(cx, cy, cx - r * 0.87, cy + r * 0.5)

    # Etiqueta/tag no canto superior esquerdo
    c.setFillColor(HexColor(cor_icone))
    tag = c.beginPath()
    tx, ty = cx - r * 0.75, cy + r * 0.62
    tag.moveTo(tx, ty)
    tag.lineTo(tx + size * 0.12, ty + size * 0.10)
    tag.lineTo(tx + size * 0.02, ty + size * 0.16)
    tag.close()
    c.drawPath(tag, fill=1, stroke=0)
    c.restoreState()


def icone_caixa_aberta(c, x, y, size, cor_fundo=None, cor_icone="#12224E"):
    """Ícone de caixa aberta com contador (UNIDADES/QUANTIDADE) - estilo clássico."""
    _borda(c, x, y, size, cor_fundo)
    c.saveState()
    c.setStrokeColor(HexColor(cor_icone))
    c.setFillColor(HexColor(cor_icone))
    lw = max(1.2, size * 0.045)
    c.setLineWidth(lw)
    c.setLineJoin(1)
    cx = x + size / 2
    cy = y + size * 0.30
    w = size * 0.30
    h = size * 0.20

    # Corpo da caixa (contorno)
    c.rect(cx - w, cy - h, w * 2, h, fill=0, stroke=1)
    # Abas abertas (linhas em V no topo)
    c.line(cx - w, cy, cx - w * 0.12, cy + h * 0.65)
    c.line(cx - w * 0.12, cy + h * 0.65, cx, cy)
    c.line(cx + w, cy, cx + w * 0.12, cy + h * 0.65)
    c.line(cx + w * 0.12, cy + h * 0.65, cx, cy)

    # Círculo com o número "1" acima da caixa (contador de quantidade)
    r = size * 0.155
    ccx, ccy = cx, y + size * 0.76
    c.circle(ccx, ccy, r, fill=0, stroke=1)
    c.setFillColor(HexColor(cor_icone))
    c.setFont("Helvetica-Bold", r * 1.35)
    c.drawCentredString(ccx, ccy - r * 0.42, "1")
    c.restoreState()


def icone_clipboard(c, x, y, size, cor_fundo=None, cor_icone="#12224E"):
    """Ícone de documento com lápis (OBSERVAÇÃO) - estilo clássico."""
    _borda(c, x, y, size, cor_fundo)
    c.saveState()
    c.setStrokeColor(HexColor(cor_icone))
    c.setFillColor(HexColor(cor_icone))
    lw = max(1.2, size * 0.045)
    c.setLineWidth(lw)
    c.setLineJoin(1)
    cx, cy = x + size / 2, y + size / 2

    w, h = size * 0.24, size * 0.30
    dobra = size * 0.10

    # Folha do documento com canto dobrado
    p = c.beginPath()
    p.moveTo(cx - w, cy + h)
    p.lineTo(cx + w - dobra, cy + h)
    p.lineTo(cx + w, cy + h - dobra)
    p.lineTo(cx + w, cy - h)
    p.lineTo(cx - w, cy - h)
    p.close()
    c.drawPath(p, fill=0, stroke=1)
    c.line(cx + w - dobra, cy + h, cx + w - dobra, cy + h - dobra)
    c.line(cx + w - dobra, cy + h - dobra, cx + w, cy + h - dobra)

    # Linhas de texto
    lw_texto = max(1.0, size * 0.032)
    c.setLineWidth(lw_texto)
    for frac in (0.35, 0.05, -0.25):
        c.line(cx - w * 0.65, cy + h * frac, cx + w * 0.45, cy + h * frac)

    # Lápis sobreposto no canto inferior direito
    c.setLineWidth(max(1.2, size * 0.045))
    px0, py0 = cx + w * 0.10, cy - h * 0.75
    px1, py1 = cx + w * 1.15, cy + h * 0.30
    c.line(px0, py0, px1, py1)
    ponta = c.beginPath()
    ponta.moveTo(px0 - size * 0.02, py0 - size * 0.02)
    ponta.lineTo(px0 + size * 0.03, py0 + size * 0.01)
    ponta.lineTo(px0 + size * 0.01, py0 + size * 0.05)
    ponta.close()
    c.drawPath(ponta, fill=1, stroke=0)
    c.restoreState()


def icone_copyright(c, cx, cy, r, cor_icone):
    """Símbolo © desenhado como círculo com a letra C (usado no rodapé)."""
    c.saveState()
    c.setStrokeColor(HexColor(cor_icone))
    c.setLineWidth(0.9)
    c.circle(cx, cy, r, fill=0, stroke=1)
    c.setFont("Helvetica-Bold", r * 1.15)
    c.setFillColor(HexColor(cor_icone))
    c.drawCentredString(cx, cy - r * 0.42, "C")
    c.restoreState()


def icone_github(c, cx, cy, r, cor_icone):
    """Ícone estilizado do GitHub (círculo com 'gato' simplificado) - rodapé."""
    c.saveState()
    c.setFillColor(HexColor(cor_icone))
    c.circle(cx, cy, r, fill=1, stroke=0)
    c.setFillColor(white)
    # Corpo simplificado (cabeça + orelhas) em silhueta branca sobre o círculo
    p = c.beginPath()
    p.moveTo(cx - r * 0.42, cy - r * 0.35)
    p.curveTo(cx - r * 0.55, cy + r * 0.15, cx - r * 0.15, cy + r * 0.55, cx, cy + r * 0.55)
    p.curveTo(cx + r * 0.15, cy + r * 0.55, cx + r * 0.55, cy + r * 0.15, cx + r * 0.42, cy - r * 0.35)
    p.curveTo(cx + r * 0.30, cy - r * 0.15, cx - r * 0.30, cy - r * 0.15, cx - r * 0.42, cy - r * 0.35)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.restoreState()
