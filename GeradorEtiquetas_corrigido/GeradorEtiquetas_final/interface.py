# -*- coding: utf-8 -*-
"""
interface.py
------------
Interface gráfica do Gerador de Etiquetas, construída com CustomTkinter.

Reproduz o layout da imagem de referência (modelo.jpeg): título com
emblema navy, cartão com os campos de preenchimento (cada um com seu
ícone, no mesmo estilo da etiqueta impressa), os botões de ação
(Imprimir, Exportar PDF, Limpar Campos) e o rodapé com a assinatura do
autor. Ao clicar em "Imprimir" é aberta uma janela de opções (impressora
e número de cópias) antes do envio.
"""

import os
import webbrowser

import customtkinter as ctk
from tkinter import filedialog

import config
import pdf
import printer
import ui_icons


class CampoEtiqueta(ctk.CTkFrame):
    """Um par (ícone + rótulo + campo de entrada) igual ao usado na referência."""

    def __init__(self, master, rotulo: str, placeholder: str, icone=None, **kwargs):
        super().__init__(master, fg_color="transparent")

        cabecalho = ctk.CTkFrame(self, fg_color="transparent")
        cabecalho.pack(fill="x", pady=(0, 6))

        if icone is not None:
            ctk.CTkLabel(cabecalho, text="", image=icone, width=22, height=22).pack(side="left", padx=(0, 8))

        self.label = ctk.CTkLabel(
            cabecalho,
            text=rotulo,
            font=config.FONTE_LABEL_CAMPO,
            text_color=config.COR_TEXTO_LABEL,
            anchor="w",
        )
        self.label.pack(side="left", fill="x")

        self.entry = ctk.CTkEntry(
            self,
            placeholder_text=placeholder,
            font=config.FONTE_ENTRY,
            height=38,
            corner_radius=10,
            border_width=1,
            border_color=config.COR_ENTRY_BORDA,
            fg_color=config.COR_BRANCO,
            text_color=config.COR_TEXTO_LABEL,
            placeholder_text_color=config.COR_PLACEHOLDER,
            **kwargs,
        )
        self.entry.pack(fill="x")

    def get(self) -> str:
        return self.entry.get().strip()

    def set(self, texto: str):
        self.entry.delete(0, "end")
        self.entry.insert(0, texto)

    def limpar(self):
        self.entry.delete(0, "end")

    def focar(self):
        self.entry.focus_set()


class JanelaOpcoesImpressao(ctk.CTkToplevel):
    """Janela modal com as opções de impressão (impressora e nº de cópias)."""

    def __init__(self, master, dados: dict):
        super().__init__(master)
        self.dados = dados
        self.title("Opções de impressão")
        self.geometry("360x300")
        self.resizable(False, False)
        self.configure(fg_color=config.COR_FUNDO_APP)
        self.transient(master)
        self.grab_set()

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=22, pady=20)

        cabecalho = ctk.CTkFrame(container, fg_color="transparent")
        cabecalho.pack(fill="x", pady=(0, 16))
        ctk.CTkLabel(
            cabecalho, text="", image=ui_icons.icone_impressora(24, cor_fundo=config.COR_NAVY), width=28, height=28
        ).pack(side="left", padx=(0, 10))
        ctk.CTkLabel(
            cabecalho,
            text="Opções de impressão",
            font=config.FONTE_SECAO,
            text_color=config.COR_TEXTO_LABEL,
        ).pack(side="left")

        ctk.CTkLabel(
            container, text="IMPRESSORA", font=config.FONTE_LABEL_CAMPO,
            text_color=config.COR_TEXTO_LABEL, anchor="w",
        ).pack(fill="x", pady=(0, 6))

        impressoras = printer.listar_impressoras()
        padrao = printer.impressora_padrao()
        opcoes = impressoras if impressoras else ["(impressora padrão do sistema)"]
        valor_inicial = padrao if padrao in opcoes else opcoes[0]

        self.combo_impressora = ctk.CTkComboBox(
            container,
            values=opcoes,
            font=config.FONTE_ENTRY,
            height=36,
            corner_radius=10,
            border_color=config.COR_ENTRY_BORDA,
            button_color=config.COR_BOTAO_PRIMARIO,
            button_hover_color=config.COR_BOTAO_PRIMARIO_HOVER,
        )
        self.combo_impressora.set(valor_inicial)
        self.combo_impressora.pack(fill="x", pady=(0, 14))

        ctk.CTkLabel(
            container, text="NÚMERO DE CÓPIAS", font=config.FONTE_LABEL_CAMPO,
            text_color=config.COR_TEXTO_LABEL, anchor="w",
        ).pack(fill="x", pady=(0, 6))

        linha_copias = ctk.CTkFrame(container, fg_color="transparent")
        linha_copias.pack(fill="x", pady=(0, 20))

        self.entry_copias = ctk.CTkEntry(
            linha_copias,
            font=config.FONTE_ENTRY,
            height=36,
            corner_radius=10,
            border_width=1,
            border_color=config.COR_ENTRY_BORDA,
            justify="center",
        )
        self.entry_copias.insert(0, "1")

        ctk.CTkButton(
            linha_copias, text="−", width=36, height=36, corner_radius=10,
            fg_color=config.COR_BOTAO_SECUNDARIO, hover_color=config.COR_BOTAO_SECUNDARIO_HOVER,
            text_color=config.COR_TEXTO_LABEL, border_width=1, border_color=config.COR_BOTAO_SECUNDARIO_BORDA,
            command=lambda: self._ajustar_copias(-1),
        ).pack(side="left")
        self.entry_copias.pack(side="left", fill="x", expand=True, padx=8)
        ctk.CTkButton(
            linha_copias, text="+", width=36, height=36, corner_radius=10,
            fg_color=config.COR_BOTAO_SECUNDARIO, hover_color=config.COR_BOTAO_SECUNDARIO_HOVER,
            text_color=config.COR_TEXTO_LABEL, border_width=1, border_color=config.COR_BOTAO_SECUNDARIO_BORDA,
            command=lambda: self._ajustar_copias(1),
        ).pack(side="left")

        linha_botoes = ctk.CTkFrame(container, fg_color="transparent")
        linha_botoes.pack(fill="x")
        linha_botoes.grid_columnconfigure((0, 1), weight=1, uniform="opcoes")

        ctk.CTkButton(
            linha_botoes, text="Cancelar", height=40, corner_radius=10,
            fg_color=config.COR_BOTAO_SECUNDARIO, hover_color=config.COR_BOTAO_SECUNDARIO_HOVER,
            text_color=config.COR_TEXTO_LABEL, border_width=1, border_color=config.COR_BOTAO_SECUNDARIO_BORDA,
            command=self.destroy,
        ).grid(row=0, column=0, sticky="ew", padx=(0, 6))

        ctk.CTkButton(
            linha_botoes, text="🖨  Imprimir", height=40, corner_radius=10,
            fg_color=config.COR_BOTAO_PRIMARIO, hover_color=config.COR_BOTAO_PRIMARIO_HOVER,
            command=self._confirmar,
        ).grid(row=0, column=1, sticky="ew", padx=(6, 0))

        self.resultado = None
        self.after(50, self._centralizar)

    def _centralizar(self):
        self.update_idletasks()
        master = self.master
        x = master.winfo_rootx() + (master.winfo_width() - self.winfo_width()) // 2
        y = master.winfo_rooty() + (master.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{max(x, 0)}+{max(y, 0)}")

    def _ajustar_copias(self, delta: int):
        try:
            valor = int(self.entry_copias.get() or "1")
        except ValueError:
            valor = 1
        valor = max(1, min(99, valor + delta))
        self.entry_copias.delete(0, "end")
        self.entry_copias.insert(0, str(valor))

    def _confirmar(self):
        impressora = self.combo_impressora.get().strip()
        if impressora.startswith("("):
            impressora = None
        try:
            copias = max(1, int(self.entry_copias.get() or "1"))
        except ValueError:
            copias = 1
        self.resultado = {"impressora": impressora, "copias": copias}
        self.destroy()


class App(ctk.CTk):
    """Janela principal do Gerador de Etiquetas."""

    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.title(config.APP_NAME)
        self.configure(fg_color=config.COR_FUNDO_APP)
        self.resizable(True, True)
        self.minsize(400, 480)

        self._montar_cabecalho()
        self._montar_cartao()
        self._montar_rodape()
        self._configurar_atalhos()

        # Ordem de navegação com Enter (mesma ordem visual dos campos)
        self._ordem_campos = [
            self.campo_cliente,
            self.campo_cidade,
            self.campo_pedido,
            self.campo_produto,
            self.campo_unidades,
            self.campo_metros,
            self.campo_observacao,
        ]
        for i, campo in enumerate(self._ordem_campos):
            proximo = self._ordem_campos[(i + 1) % len(self._ordem_campos)]
            campo.entry.bind("<Return>", lambda e, prox=proximo: prox.focar())

        self.campo_cliente.focar()
        self._ajustar_tamanho_janela()

    # ------------------------------------------------------------------
    # Construção da interface
    # ------------------------------------------------------------------
    def _ajustar_tamanho_janela(self):
        """
        Calcula o tamanho ideal da janela a partir do conteúdo já montado
        (em vez de um valor fixo em pixels), e limita esse tamanho ao
        espaço disponível na tela do usuário. Isso evita que a janela
        fique maior que a tela em computadores com fontes/DPI diferentes
        - o que fazia os botões ficarem inacessíveis. A área de campos é
        rolável (CTkScrollableFrame), então mesmo que o conteúdo não
        caiba inteiro, o usuário sempre consegue rolar até os botões.
        """
        self.update_idletasks()

        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()

        largura_desejada = max(config.JANELA_LARGURA, self.winfo_reqwidth())
        altura_desejada = max(config.JANELA_ALTURA, self.winfo_reqheight())

        # Nunca maior que a tela (com folga para barra de tarefas/dock)
        largura_final = min(largura_desejada, int(largura_tela * 0.95))
        altura_final = min(altura_desejada, int(altura_tela * 0.90))

        x = max((largura_tela // 2) - (largura_final // 2), 0)
        y = max((altura_tela // 2) - (altura_final // 2), 0)
        self.geometry(f"{largura_final}x{altura_final}+{x}+{y}")

    def _montar_cabecalho(self):
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="x", padx=24, pady=(24, 12))

        linha_titulo = ctk.CTkFrame(container, fg_color="transparent")
        linha_titulo.pack(fill="x")

        ctk.CTkLabel(
            linha_titulo, text="", image=ui_icons.icone_pacote(36, cor_fundo=config.COR_NAVY),
            width=40, height=40,
        ).pack(side="left", padx=(0, 12))

        textos = ctk.CTkFrame(linha_titulo, fg_color="transparent")
        textos.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(
            textos,
            text=config.APP_NAME,
            font=config.FONTE_TITULO,
            text_color=config.COR_TEXTO_TITULO,
            anchor="w",
        ).pack(fill="x")

        ctk.CTkLabel(
            textos,
            text=config.APP_SUBTITLE,
            font=config.FONTE_SUBTITULO,
            text_color=config.COR_TEXTO_SUBTITULO,
            anchor="w",
        ).pack(fill="x", pady=(2, 0))

    def _montar_cartao(self):
        cartao = ctk.CTkFrame(
            self,
            fg_color=config.COR_CARD,
            corner_radius=14,
            border_width=1,
            border_color=config.COR_BORDA_CARD,
        )
        cartao.pack(fill="both", expand=True, padx=24, pady=(0, 12))

        interno = ctk.CTkScrollableFrame(
            cartao,
            fg_color="transparent",
            corner_radius=0,
            scrollbar_button_color=config.COR_BORDA_CARD,
            scrollbar_button_hover_color=config.COR_ENTRY_BORDA,
        )
        interno.pack(fill="both", expand=True, padx=16, pady=16)

        cabecalho_secao = ctk.CTkFrame(interno, fg_color="transparent")
        cabecalho_secao.pack(fill="x", pady=(0, 14))

        ctk.CTkFrame(cabecalho_secao, fg_color=config.COR_NAVY, corner_radius=2, width=4, height=16).pack(
            side="left", padx=(0, 8)
        )
        ctk.CTkLabel(
            cabecalho_secao,
            text="PREENCHER ETIQUETA",
            font=config.FONTE_SECAO,
            text_color=config.COR_TEXTO_LABEL,
            anchor="w",
        ).pack(side="left", fill="x")

        self.campo_cliente = CampoEtiqueta(
            interno, "CLIENTE", config.PLACEHOLDER_CLIENTE, icone=ui_icons.icone_pessoa()
        )
        self.campo_cliente.pack(fill="x", pady=(0, 12))

        self.campo_cidade = CampoEtiqueta(
            interno, "CIDADE", config.PLACEHOLDER_CIDADE, icone=ui_icons.icone_pin()
        )
        self.campo_cidade.pack(fill="x", pady=(0, 12))

        self.campo_pedido = CampoEtiqueta(
            interno, "PEDIDO", config.PLACEHOLDER_PEDIDO, icone=ui_icons.icone_pacote(28)
        )
        self.campo_pedido.pack(fill="x", pady=(0, 12))

        self.campo_produto = CampoEtiqueta(
            interno, "PRODUTO", config.PLACEHOLDER_PRODUTO, icone=ui_icons.icone_produto()
        )
        self.campo_produto.pack(fill="x", pady=(0, 12))

        # --- Unidades / Metros lado a lado (mesma divisão da etiqueta impressa) ---
        linha_qtd = ctk.CTkFrame(interno, fg_color="transparent")
        linha_qtd.pack(fill="x", pady=(0, 12))
        linha_qtd.grid_columnconfigure((0, 1), weight=1, uniform="qtd")

        self.campo_unidades = CampoEtiqueta(
            linha_qtd, "UNIDADES", config.PLACEHOLDER_UNIDADES, icone=ui_icons.icone_unidades()
        )
        self.campo_unidades.grid(row=0, column=0, sticky="ew", padx=(0, 6))

        self.campo_metros = CampoEtiqueta(
            linha_qtd, "METROS (M²)", config.PLACEHOLDER_METROS, icone=ui_icons.icone_metros()
        )
        self.campo_metros.grid(row=0, column=1, sticky="ew", padx=(6, 0))

        self.campo_observacao = CampoEtiqueta(
            interno, "OBSERVAÇÃO", config.PLACEHOLDER_OBSERVACAO, icone=ui_icons.icone_clipboard()
        )
        self.campo_observacao.pack(fill="x", pady=(0, 16))

        # --- Botões de ação ---
        linha_botoes = ctk.CTkFrame(interno, fg_color="transparent")
        linha_botoes.pack(fill="x", pady=(0, 6))
        linha_botoes.grid_columnconfigure((0, 1), weight=1, uniform="botoes")

        self.btn_imprimir = ctk.CTkButton(
            linha_botoes,
            text="🖨  Imprimir",
            font=config.FONTE_BOTAO,
            height=42,
            corner_radius=10,
            fg_color=config.COR_BOTAO_PRIMARIO,
            hover_color=config.COR_BOTAO_PRIMARIO_HOVER,
            command=self.acao_imprimir,
        )
        self.btn_imprimir.grid(row=0, column=0, sticky="ew", padx=(0, 6), pady=(0, 8))

        self.btn_pdf = ctk.CTkButton(
            linha_botoes,
            text="📄  Exportar PDF",
            font=config.FONTE_BOTAO,
            height=42,
            corner_radius=10,
            fg_color=config.COR_BOTAO_PRIMARIO,
            hover_color=config.COR_BOTAO_PRIMARIO_HOVER,
            command=self.acao_exportar_pdf,
        )
        self.btn_pdf.grid(row=0, column=1, sticky="ew", padx=(6, 0), pady=(0, 8))

        self.btn_limpar = ctk.CTkButton(
            interno,
            text="🗑  Limpar campos",
            font=config.FONTE_BOTAO,
            height=42,
            corner_radius=10,
            fg_color=config.COR_BOTAO_SECUNDARIO,
            hover_color=config.COR_BOTAO_SECUNDARIO_HOVER,
            text_color=config.COR_TEXTO_LABEL,
            border_width=1,
            border_color=config.COR_BOTAO_SECUNDARIO_BORDA,
            command=self.acao_limpar_campos,
        )
        self.btn_limpar.pack(fill="x")

        # Rótulo de status (mensagens temporárias: sucesso/erro)
        self.label_status = ctk.CTkLabel(
            interno, text="", font=config.FONTE_SUBTITULO, text_color=config.COR_TEXTO_SUBTITULO
        )
        self.label_status.pack(fill="x", pady=(10, 0))

    def _montar_rodape(self):
        rodape = ctk.CTkFrame(self, fg_color="transparent")
        rodape.pack(fill="x", padx=24, pady=(0, 18))

        texto = f"© {config.ANO_COPYRIGHT} {config.AUTOR_NOME}. Todos os direitos reservados."
        ctk.CTkLabel(
            rodape,
            text=texto,
            font=config.FONTE_RODAPE,
            text_color=config.COR_TEXTO_SUBTITULO,
        ).pack(side="left")

        link = ctk.CTkLabel(
            rodape,
            text=f"GitHub: {config.AUTOR_GITHUB}",
            font=(config.FONTE_FAMILIA, 10, "underline"),
            text_color=config.COR_BOTAO_PRIMARIO,
            cursor="hand2",
        )
        link.pack(side="right")
        link.bind("<Button-1>", lambda e: webbrowser.open(config.AUTOR_GITHUB_URL))

    # ------------------------------------------------------------------
    # Atalhos de teclado
    # ------------------------------------------------------------------
    def _configurar_atalhos(self):
        self.bind("<Escape>", lambda e: self.acao_limpar_campos())
        self.bind("<Control-p>", lambda e: self.acao_imprimir())
        self.bind("<Control-P>", lambda e: self.acao_imprimir())
        self.bind("<Control-s>", lambda e: self.acao_exportar_pdf())
        self.bind("<Control-S>", lambda e: self.acao_exportar_pdf())

    # ------------------------------------------------------------------
    # Coleta e validação dos dados digitados
    # ------------------------------------------------------------------
    def _coletar_dados(self) -> dict:
        return {
            "cliente": self.campo_cliente.get(),
            "cidade": self.campo_cidade.get(),
            "pedido": self.campo_pedido.get(),
            "produto": self.campo_produto.get(),
            "unidades": self.campo_unidades.get(),
            "metros": self.campo_metros.get(),
            "observacao": self.campo_observacao.get(),
        }

    def _campos_obrigatorios_preenchidos(self, dados: dict) -> bool:
        obrigatorios = ["cliente", "cidade", "pedido", "produto"]
        return all(dados.get(campo) for campo in obrigatorios)

    def _mostrar_status(self, mensagem: str, sucesso: bool = True):
        cor = "#1F7A3D" if sucesso else "#B3261E"
        self.label_status.configure(text=mensagem, text_color=cor)
        # A mensagem some sozinha após alguns segundos
        self.after(4000, lambda: self.label_status.configure(text=""))

    # ------------------------------------------------------------------
    # Ações dos botões
    # ------------------------------------------------------------------
    def acao_imprimir(self):
        dados = self._coletar_dados()
        if not self._campos_obrigatorios_preenchidos(dados):
            self._mostrar_status("Preencha ao menos Cliente, Cidade, Pedido e Produto.", sucesso=False)
            return

        janela = JanelaOpcoesImpressao(self, dados)
        self.wait_window(janela)
        if not janela.resultado:
            return  # usuário cancelou

        try:
            printer.imprimir_etiqueta(
                dados,
                nome_impressora=janela.resultado["impressora"],
                copias=janela.resultado["copias"],
            )
            self._mostrar_status("Etiqueta enviada para impressão.")
        except printer.ErroImpressao as exc:
            self._mostrar_status(str(exc), sucesso=False)

    def acao_exportar_pdf(self):
        dados = self._coletar_dados()
        if not self._campos_obrigatorios_preenchidos(dados):
            self._mostrar_status("Preencha ao menos Cliente, Cidade, Pedido e Produto.", sucesso=False)
            return

        sugestao = f"etiqueta_{dados['pedido']}.pdf" if dados["pedido"] else "etiqueta.pdf"
        caminho = filedialog.asksaveasfilename(
            title="Exportar etiqueta em PDF",
            defaultextension=".pdf",
            initialfile=sugestao,
            filetypes=[("Arquivo PDF", "*.pdf")],
        )
        if not caminho:
            return

        try:
            pdf.gerar_pdf_etiqueta(caminho, dados)
            self._mostrar_status("PDF salvo com sucesso.")
        except Exception as exc:
            self._mostrar_status(f"Erro ao salvar PDF: {exc}", sucesso=False)

    def acao_limpar_campos(self):
        for campo in (
            self.campo_cliente,
            self.campo_cidade,
            self.campo_pedido,
            self.campo_produto,
            self.campo_unidades,
            self.campo_metros,
            self.campo_observacao,
        ):
            campo.limpar()
        self.campo_cliente.focar()
        self.label_status.configure(text="")
