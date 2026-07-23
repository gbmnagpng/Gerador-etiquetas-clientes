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


def icone_pessoa(c, x, y, size, cor_fundo=None, cor_icone="#FFFFFF"):
    """Ícone de pessoa (CLIENTE)."""
    _fundo(c, x, y, size, cor_fundo)
    c.saveState()
    c.setFillColor(HexColor(cor_icone))
    c.setStrokeColor(HexColor(cor_icone))
    cx, cy = x + size / 2, y + size / 2

    # Cabeça
    r_cabeca = size * 0.14
    c.circle(cx, cy + size * 0.14, r_cabeca, fill=1, stroke=0)

    # Corpo (meia elipse / arco)
    p = c.beginPath()
    largura = size * 0.40
    altura = size * 0.26
    base_y = cy - size * 0.20
    p.moveTo(cx - largura / 2, base_y)
    p.curveTo(cx - largura / 2, base_y + altura,
              cx + largura / 2, base_y + altura,
              cx + largura / 2, base_y)
    p.lineTo(cx - largura / 2, base_y)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    c.restoreState()


def icone_pin(c, x, y, size, cor_fundo=None, cor_icone="#FFFFFF"):
    """Ícone de pino de localização (CIDADE)."""
    _fundo(c, x, y, size, cor_fundo)
    c.saveState()
    c.setFillColor(HexColor(cor_icone))
    c.setStrokeColor(HexColor(cor_icone))
    cx = x + size / 2
    topo = y + size * 0.72
    r = size * 0.17

    # Corpo em forma de gota (círculo + ponta triangular)
    p = c.beginPath()
    p.moveTo(cx - r, topo)
    p.curveTo(cx - r, topo + r * 1.55, cx + r, topo + r * 1.55, cx + r, topo)
    p.curveTo(cx + r, topo - r * 0.9, cx, topo - size * 0.34, cx, topo - size * 0.34)
    p.curveTo(cx, topo - size * 0.34, cx - r, topo - r * 0.9, cx - r, topo)
    p.close()
    c.drawPath(p, fill=1, stroke=0)

    # Furo central (branco vira "buraco" -> desenhamos com a cor de fundo)
    c.setFillColor(HexColor(cor_fundo) if cor_fundo else white)
    c.circle(cx, topo, r * 0.42, fill=1, stroke=0)
    c.restoreState()


def icone_produto(c, x, y, size, cor_fundo=None, cor_icone="#FFFFFF"):
    """Ícone de ladrilhos/produto (PRODUTO)."""
    _fundo(c, x, y, size, cor_fundo)
    c.saveState()
    c.setFillColor(HexColor(cor_icone))
    c.setStrokeColor(HexColor(cor_icone))
    cx, cy = x + size / 2, y + size / 2 - size * 0.03
    lado = size * 0.26

    def losango(dx, dy, alpha=1.0):
        p = c.beginPath()
        p.moveTo(cx + dx, cy + dy + lado * 0.55)
        p.lineTo(cx + dx + lado * 0.55, cy + dy)
        p.lineTo(cx + dx, cy + dy - lado * 0.55)
        p.lineTo(cx + dx - lado * 0.55, cy + dy)
        p.close()
        c.setFillAlpha(alpha)
        c.drawPath(p, fill=1, stroke=0)
        c.setFillAlpha(1)

    losango(-lado * 0.55, size * 0.12, 1.0)
    losango(lado * 0.55, size * 0.12, 0.65)
    losango(0, -size * 0.16, 0.85)
    c.restoreState()


def icone_caixa_aberta(c, x, y, size, cor_fundo=None, cor_icone="#FFFFFF"):
    """Ícone de caixa de papelão aberta (UNIDADES)."""
    _fundo(c, x, y, size, cor_fundo)
    c.saveState()
    c.setStrokeColor(HexColor(cor_icone))
    c.setFillColor(HexColor(cor_icone))
    c.setLineWidth(max(1.3, size * 0.04))
    c.setLineJoin(1)
    cx, cy = x + size / 2, y + size / 2 - size * 0.04
    w = size * 0.34
    h = size * 0.22

    # Corpo da caixa (trapézio simples representando a base)
    p = c.beginPath()
    p.moveTo(cx - w, cy - h * 0.2)
    p.lineTo(cx - w, cy - h)
    p.lineTo(cx + w, cy - h)
    p.lineTo(cx + w, cy - h * 0.2)
    p.close()
    c.drawPath(p, fill=0, stroke=1)

    # Abas abertas (linhas em V no topo)
    c.line(cx - w, cy - h * 0.2, cx - w * 0.15, cy + h * 0.55)
    c.line(cx - w * 0.15, cy + h * 0.55, cx, cy - h * 0.2)
    c.line(cx + w, cy - h * 0.2, cx + w * 0.15, cy + h * 0.55)
    c.line(cx + w * 0.15, cy + h * 0.55, cx, cy - h * 0.2)
    c.restoreState()


def icone_clipboard(c, x, y, size, cor_fundo=None, cor_icone="#FFFFFF"):
    """Ícone de prancheta (OBSERVAÇÃO)."""
    _fundo(c, x, y, size, cor_fundo)
    c.saveState()
    c.setStrokeColor(HexColor(cor_icone))
    c.setFillColor(HexColor(cor_icone))
    c.setLineWidth(max(1.3, size * 0.038))
    cx, cy = x + size / 2, y + size / 2

    w, h = size * 0.30, size * 0.40
    # Prancheta (retângulo)
    c.roundRect(cx - w, cy - h, w * 2, h * 2, 3, fill=0, stroke=1)
    # Clipe superior
    c.roundRect(cx - w * 0.35, cy + h - size * 0.02, w * 0.7, size * 0.12, 2, fill=1, stroke=0)
    # Linhas de texto
    for i, frac in enumerate([0.35, 0.02, -0.31]):
        c.line(cx - w * 0.6, cy + h * frac, cx + w * 0.6, cy + h * frac)
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
