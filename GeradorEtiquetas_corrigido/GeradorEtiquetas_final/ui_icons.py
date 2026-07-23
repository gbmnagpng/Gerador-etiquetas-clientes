# -*- coding: utf-8 -*-
"""
ui_icons.py
-----------
Ícones vetoriais (desenhados com PIL) usados na *interface* (CustomTkinter),
no mesmo estilo visual do emblema quadrado navy usado na etiqueta impressa
(ver `icons.py`, que desenha os mesmos ícones diretamente no PDF).

Cada função devolve um `customtkinter.CTkImage` pronto para ser usado em
`CTkLabel(image=...)`, já com anti-aliasing (desenhado em alta resolução e
reduzido com LANCZOS) para ficar nítido em qualquer densidade de tela.
"""

from PIL import Image, ImageDraw
import customtkinter as ctk

import config

_ESCALA = 4  # desenha em 4x e reduz -> bordas suaves sem depender de libs extras


def _base(size_px: int, cor_fundo: str, radius_frac: float = 0.28):
    """Cria a tela de desenho em alta resolução com o quadrado de fundo arredondado."""
    s = size_px * _ESCALA
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    if cor_fundo:
        raio = int(s * radius_frac)
        draw.rounded_rectangle([0, 0, s - 1, s - 1], radius=raio, fill=cor_fundo)
    return img, draw, s


def _finalizar(img: Image.Image, size_px: int) -> ctk.CTkImage:
    img = img.resize((size_px, size_px), Image.LANCZOS)
    return ctk.CTkImage(light_image=img, dark_image=img, size=(size_px, size_px))


def icone_pessoa(size_px=28, cor_fundo=config.COR_NAVY, cor_icone="#FFFFFF"):
    img, draw, s = _base(size_px, cor_fundo)
    cx, cy = s / 2, s / 2
    r_cabeca = s * 0.15
    draw.ellipse(
        [cx - r_cabeca, cy - s * 0.16 - r_cabeca, cx + r_cabeca, cy - s * 0.16 + r_cabeca],
        fill=cor_icone,
    )
    largura, altura = s * 0.42, s * 0.28
    base_y = cy + s * 0.20
    draw.pieslice(
        [cx - largura / 2, base_y - altura, cx + largura / 2, base_y + altura],
        180, 360, fill=cor_icone,
    )
    return _finalizar(img, size_px)


def icone_pin(size_px=28, cor_fundo=config.COR_NAVY, cor_icone="#FFFFFF"):
    img, draw, s = _base(size_px, cor_fundo)
    cx = s / 2
    topo = s * 0.28
    r = s * 0.17
    draw.ellipse([cx - r, topo - r, cx + r, topo + r], fill=cor_icone)
    draw.polygon(
        [(cx - r * 0.85, topo + r * 0.35), (cx + r * 0.85, topo + r * 0.35), (cx, topo + s * 0.34)],
        fill=cor_icone,
    )
    furo = r * 0.42
    draw.ellipse([cx - furo, topo - furo, cx + furo, topo + furo], fill=cor_fundo or (0, 0, 0, 0))
    return _finalizar(img, size_px)


def icone_produto(size_px=28, cor_fundo=config.COR_NAVY, cor_icone="#FFFFFF"):
    img, draw, s = _base(size_px, cor_fundo)
    cx, cy = s / 2, s / 2
    lado = s * 0.24

    def losango(dx, dy):
        draw.polygon(
            [
                (cx + dx, cy + dy - lado * 0.55),
                (cx + dx + lado * 0.55, cy + dy),
                (cx + dx, cy + dy + lado * 0.55),
                (cx + dx - lado * 0.55, cy + dy),
            ],
            fill=cor_icone,
        )

    losango(-lado * 0.55, -s * 0.05)
    losango(lado * 0.55, -s * 0.05)
    losango(0, s * 0.20)
    return _finalizar(img, size_px)


def icone_unidades(size_px=28, cor_fundo=config.COR_NAVY, cor_icone="#FFFFFF"):
    """Caixa de papelão aberta (campo UNIDADES)."""
    img, draw, s = _base(size_px, cor_fundo)
    cx, cy = s / 2, s / 2 - s * 0.04
    w, h = s * 0.30, s * 0.18
    largura_linha = max(2, int(s * 0.05))
    draw.line([(cx - w, cy - h * 0.2), (cx - w, cy - h)], fill=cor_icone, width=largura_linha)
    draw.line([(cx - w, cy - h), (cx + w, cy - h)], fill=cor_icone, width=largura_linha)
    draw.line([(cx + w, cy - h), (cx + w, cy - h * 0.2)], fill=cor_icone, width=largura_linha)
    draw.line([(cx - w, cy - h * 0.2), (cx - w * 0.15, cy + h * 0.7)], fill=cor_icone, width=largura_linha)
    draw.line([(cx - w * 0.15, cy + h * 0.7), (cx, cy - h * 0.2)], fill=cor_icone, width=largura_linha)
    draw.line([(cx + w, cy - h * 0.2), (cx + w * 0.15, cy + h * 0.7)], fill=cor_icone, width=largura_linha)
    draw.line([(cx + w * 0.15, cy + h * 0.7), (cx, cy - h * 0.2)], fill=cor_icone, width=largura_linha)
    return _finalizar(img, size_px)


def icone_metros(size_px=28, cor_fundo=config.COR_NAVY, cor_icone="#FFFFFF"):
    """Régua / área (campo METROS)."""
    img, draw, s = _base(size_px, cor_fundo)
    largura_linha = max(2, int(s * 0.05))
    x0, x1 = s * 0.20, s * 0.80
    y0, y1 = s * 0.36, s * 0.64
    draw.rounded_rectangle([x0, y0, x1, y1], radius=s * 0.05, outline=cor_icone, width=largura_linha)
    for frac in (0.35, 0.5, 0.65):
        x = x0 + (x1 - x0) * frac
        draw.line([(x, y0), (x, y0 + (y1 - y0) * 0.45)], fill=cor_icone, width=largura_linha)
    return _finalizar(img, size_px)


def icone_clipboard(size_px=28, cor_fundo=config.COR_NAVY, cor_icone="#FFFFFF"):
    img, draw, s = _base(size_px, cor_fundo)
    cx, cy = s / 2, s / 2
    w, h = s * 0.22, s * 0.28
    largura_linha = max(2, int(s * 0.045))
    draw.rounded_rectangle([cx - w, cy - h, cx + w, cy + h], radius=s * 0.04, outline=cor_icone, width=largura_linha)
    draw.rounded_rectangle(
        [cx - w * 0.4, cy - h - s * 0.04, cx + w * 0.4, cy - h + s * 0.06], radius=s * 0.02, fill=cor_icone
    )
    for frac in (0.30, 0.02, -0.26):
        draw.line([(cx - w * 0.65, cy + h * frac), (cx + w * 0.65, cy + h * frac)], fill=cor_icone, width=max(1, largura_linha - 1))
    return _finalizar(img, size_px)


def icone_pacote(size_px=32, cor_fundo=config.COR_NAVY, cor_icone="#FFFFFF"):
    """Ícone de pacote/caixa 3D (cabeçalho do app)."""
    img, draw, s = _base(size_px, cor_fundo, radius_frac=0.30)
    cx, cy = s / 2, s / 2
    r = s * 0.30
    largura_linha = max(2, int(s * 0.05))
    draw.line([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy), (cx, cy - r)], fill=cor_icone, width=largura_linha, joint="curve")
    draw.line([(cx, cy - r), (cx, cy + r)], fill=cor_icone, width=largura_linha)
    draw.line([(cx - r * 0.5, cy - r * 0.5), (cx, cy)], fill=cor_icone, width=largura_linha)
    draw.line([(cx + r * 0.5, cy - r * 0.5), (cx, cy)], fill=cor_icone, width=largura_linha)
    return _finalizar(img, size_px)


def icone_impressora(size_px=20, cor_fundo=None, cor_icone=config.COR_NAVY):
    img, draw, s = _base(size_px, cor_fundo)
    largura_linha = max(2, int(s * 0.06))
    draw.rounded_rectangle([s * 0.18, s * 0.38, s * 0.82, s * 0.66], radius=s * 0.06, outline=cor_icone, width=largura_linha)
    draw.rectangle([s * 0.30, s * 0.14, s * 0.70, s * 0.40], outline=cor_icone, width=largura_linha)
    draw.rectangle([s * 0.30, s * 0.64, s * 0.70, s * 0.88], fill=cor_icone)
    return _finalizar(img, size_px)
