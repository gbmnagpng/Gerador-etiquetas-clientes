# -*- coding: utf-8 -*-
"""
printer.py
----------
Envio da etiqueta diretamente para a impressora padrão do sistema,
sem abrir qualquer janela de visualização/preview.

Estratégia por sistema operacional:

    Windows: impressão NATIVA via GDI (módulo printer_windows.py), que
             desenha a etiqueta direto no driver da impressora, sem
             depender de nenhum leitor de PDF externo. Caso as
             dependências opcionais (pywin32 + pymupdf) não estejam
             instaladas, cai para o método via Shell como alternativa.

    Linux/macOS: usa o utilitário `lp` (CUPS), padrão em praticamente
             todas as distribuições e no macOS.

Em todos os casos a etiqueta é gerada pela mesma função de desenho
vetorial usada na exportação de PDF (pdf.py), garantindo que impressão
e PDF exportado sejam sempre idênticos.
"""

from __future__ import annotations

import os
import platform
import shutil
import subprocess
import uuid

import config
import pdf


class ErroImpressao(Exception):
    """Erro genérico ao tentar imprimir a etiqueta."""
    pass


def _gerar_pdf_temporario(dados: dict) -> str:
    nome_arquivo = f"etiqueta_{uuid.uuid4().hex[:8]}.pdf"
    caminho = os.path.join(config.PASTA_TEMP, nome_arquivo)
    pdf.gerar_pdf_etiqueta(caminho, dados)
    return caminho


def _imprimir_windows(dados: dict, nome_impressora: str | None, copias: int):
    import printer_windows

    if printer_windows.disponivel():
        try:
            printer_windows.imprimir(dados, nome_impressora=nome_impressora, copias=copias)
            return
        except printer_windows.ErroImpressaoWindows as exc:
            raise ErroImpressao(str(exc)) from exc

    # Alternativa: pede para o Windows abrir o PDF com o verbo "print"
    # do programa padrão associado a .pdf. Só é usada se as dependências
    # da impressão nativa (pywin32 + pymupdf) não estiverem instaladas.
    caminho_pdf = _gerar_pdf_temporario(dados)
    try:
        os.startfile(caminho_pdf, "print")  # type: ignore[attr-defined]
    except OSError as exc:
        raise ErroImpressao(
            "Não foi possível imprimir. Instale as dependências recomendadas com "
            "'pip install pywin32 pymupdf' para impressão direta e silenciosa, "
            f"ou verifique se há um leitor de PDF e uma impressora padrão configurados. Detalhe: {exc}"
        ) from exc


def _imprimir_unix(dados: dict, nome_impressora: str | None, copias: int):
    if not shutil.which("lp"):
        raise ErroImpressao(
            "Comando 'lp' não encontrado. Instale o CUPS (ex: 'sudo apt install cups') "
            "para habilitar a impressão."
        )

    caminho_pdf = _gerar_pdf_temporario(dados)
    comando = ["lp"]
    if nome_impressora:
        comando += ["-d", nome_impressora]
    if copias and copias > 1:
        comando += ["-n", str(copias)]
    comando.append(caminho_pdf)

    try:
        resultado = subprocess.run(comando, capture_output=True, text=True, timeout=20)
    except subprocess.TimeoutExpired as exc:
        raise ErroImpressao("Tempo esgotado ao tentar imprimir.") from exc

    if resultado.returncode != 0:
        raise ErroImpressao(f"Falha ao enviar para a impressora: {resultado.stderr.strip()}")


def imprimir_etiqueta(dados: dict, nome_impressora: str | None = None, copias: int = 1) -> None:
    """
    Envia a etiqueta para a impressora padrão do sistema (ou para
    `nome_impressora`, se informado), sem exibir janela de preview.
    Lança ErroImpressao em caso de falha, com uma mensagem explicando
    o motivo e como corrigir.
    """
    sistema = platform.system()
    copias = max(1, int(copias or 1))

    if sistema == "Windows":
        _imprimir_windows(dados, nome_impressora, copias)
    elif sistema in ("Linux", "Darwin"):
        _imprimir_unix(dados, nome_impressora, copias)
    else:
        raise ErroImpressao(f"Sistema operacional não suportado: {sistema}")


def listar_impressoras() -> list[str]:
    """Lista os nomes das impressoras instaladas, independente do sistema operacional."""
    sistema = platform.system()

    if sistema == "Windows":
        import printer_windows

        return printer_windows.listar_impressoras()

    if shutil.which("lpstat"):
        try:
            resultado = subprocess.run(["lpstat", "-p"], capture_output=True, text=True, timeout=10)
        except subprocess.TimeoutExpired:
            return []
        nomes = []
        for linha in resultado.stdout.splitlines():
            if linha.startswith("printer "):
                nomes.append(linha.split()[1])
        return nomes

    return []


def impressora_padrao() -> str | None:
    """Retorna o nome da impressora padrão do sistema, se houver uma configurada."""
    sistema = platform.system()

    if sistema == "Windows":
        import win32print

        try:
            return win32print.GetDefaultPrinter()
        except Exception:
            return None

    if shutil.which("lpstat"):
        try:
            resultado = subprocess.run(["lpstat", "-d"], capture_output=True, text=True, timeout=10)
        except subprocess.TimeoutExpired:
            return None
        linha = resultado.stdout.strip()
        if ":" in linha:
            nome = linha.split(":", 1)[1].strip()
            return nome or None
    return None
