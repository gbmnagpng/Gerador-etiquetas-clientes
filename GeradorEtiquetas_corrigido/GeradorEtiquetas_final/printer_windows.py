# -*- coding: utf-8 -*-
"""
printer_windows.py
-------------------
Impressão nativa e silenciosa no Windows, via GDI (biblioteca pywin32).

Por que este módulo existe
---------------------------
A forma "simples" de imprimir um PDF no Windows é pedir para o Shell
abrir o arquivo com o verbo "print" (`os.startfile(caminho, "print")`).
Na prática isso é pouco confiável:

    - Só funciona se existir um programa associado a .pdf que reconheça
      o verbo "print" (nem sempre existe, dependendo da instalação).
    - Muitas vezes abre uma janela do leitor de PDF, mesmo que
      brevemente, antes de mandar para a impressora.
    - Se não houver impressora padrão configurada, falha silenciosamente
      sem avisar o usuário.

Este módulo evita tudo isso: ele renderiza a própria etiqueta (a mesma
função de desenho vetorial usada no PDF, então o resultado é 100%
idêntico ao exportado) em um bitmap de altíssima resolução e desenha
esse bitmap diretamente no contexto de dispositivo (DC) da impressora
usando a API do Windows (GDI), sem abrir nenhum programa ou janela.

Dependências (apenas no Windows):
    pip install pywin32 pymupdf pillow
"""

from __future__ import annotations

import os

import config
import pdf

from PIL import Image

try:
    import win32print
    import win32ui
    from PIL import ImageWin

    _PYWIN32_DISPONIVEL = True
except ImportError:
    _PYWIN32_DISPONIVEL = False

try:
    import fitz  # PyMuPDF

    _FITZ_DISPONIVEL = True
except ImportError:
    _FITZ_DISPONIVEL = False

# Índices usados por GetDeviceCaps para obter a resolução física da
# impressora (constantes padrão da API do Windows GDI).
_LOGPIXELSX = 88
_LOGPIXELSY = 90


class ErroImpressaoWindows(Exception):
    pass


def disponivel() -> bool:
    """Indica se a impressão nativa via GDI pode ser usada neste ambiente."""
    return os.name == "nt" and _PYWIN32_DISPONIVEL and _FITZ_DISPONIVEL


def _renderizar_pdf_em_bitmap(caminho_pdf: str, dpi: int = 600):
    """Rasteriza a primeira página do PDF (vetorial) em alta resolução."""
    documento = fitz.open(caminho_pdf)
    try:
        pagina = documento[0]
        zoom = dpi / 72.0
        matriz = fitz.Matrix(zoom, zoom)
        pix = pagina.get_pixmap(matrix=matriz, alpha=False)
        imagem = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        largura_pt = pagina.rect.width
        altura_pt = pagina.rect.height
    finally:
        documento.close()
    return imagem, largura_pt, altura_pt


def imprimir(dados: dict, nome_impressora: str | None = None, dpi: int = 600, copias: int = 1) -> None:
    """
    Gera a etiqueta e envia diretamente para a impressora do Windows via
    GDI, sem abrir nenhuma janela de visualização. `copias` controla
    quantas vezes a etiqueta é repetida no mesmo trabalho de impressão.
    """
    if not disponivel():
        raise ErroImpressaoWindows(
            "Impressão nativa indisponível: instale as dependências com "
            "'pip install pywin32 pymupdf pillow'."
        )

    copias = max(1, int(copias or 1))

    caminho_pdf = os.path.join(config.PASTA_TEMP, "_etiqueta_impressao_tmp.pdf")
    pdf.gerar_pdf_etiqueta(caminho_pdf, dados)

    imagem, largura_pt, altura_pt = _renderizar_pdf_em_bitmap(caminho_pdf, dpi=dpi)

    nome_impressora = nome_impressora or win32print.GetDefaultPrinter()
    if not nome_impressora:
        raise ErroImpressaoWindows(
            "Nenhuma impressora padrão configurada no Windows. Defina uma "
            "impressora padrão em Configurações > Dispositivos > Impressoras."
        )

    dc_impressora = win32ui.CreateDC()
    try:
        dc_impressora.CreatePrinterDC(nome_impressora)
    except Exception as exc:
        raise ErroImpressaoWindows(
            f"Não foi possível conectar à impressora '{nome_impressora}': {exc}"
        ) from exc

    try:
        ppp_x = dc_impressora.GetDeviceCaps(_LOGPIXELSX)
        ppp_y = dc_impressora.GetDeviceCaps(_LOGPIXELSY)

        # Converte o tamanho real da etiqueta (em pontos, 1/72 pol) para
        # pixels na resolução física da impressora, mantendo a proporção
        # exata - sem cortes e sem distorção.
        largura_px = int(round(largura_pt / 72.0 * ppp_x))
        altura_px = int(round(altura_pt / 72.0 * ppp_y))

        dc_impressora.StartDoc(f"Etiqueta - Pedido {dados.get('pedido', '')}")
        dib = ImageWin.Dib(imagem)
        for _ in range(copias):
            dc_impressora.StartPage()
            dib.draw(dc_impressora.GetHandleOutput(), (0, 0, largura_px, altura_px))
            dc_impressora.EndPage()
        dc_impressora.EndDoc()
    except Exception as exc:
        try:
            dc_impressora.AbortDoc()
        except Exception:
            pass
        raise ErroImpressaoWindows(f"Falha ao enviar a etiqueta para a impressora: {exc}") from exc
    finally:
        dc_impressora.DeleteDC()


def listar_impressoras() -> list[str]:
    """Lista os nomes das impressoras instaladas no Windows."""
    if not _PYWIN32_DISPONIVEL:
        return []
    flags = win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
    return [impressora[2] for impressora in win32print.EnumPrinters(flags)]
