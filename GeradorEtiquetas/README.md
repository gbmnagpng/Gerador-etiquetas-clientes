# Gerador de Etiquetas

Programa desktop, 100% offline, para gerar e imprimir etiquetas de pedido
(cliente, cidade, produto, unidades, metros e observação) com layout
idêntico ao modelo de referência.

## Instalação

### Opção 1 - Instalador de um clique (recomendado)

Dá duplo clique em **`instalar.bat`** (Windows) ou rode **`./instalar.sh`**
(Linux). O instalador faz tudo sozinho:

1. Cria um ambiente virtual (`.venv`) e instala as dependências, se ainda
   não existir.
2. Gera o executável autônomo em `dist/` (via PyInstaller), se ainda não
   existir.
3. Cria os atalhos de "clicar e abrir":
   - **Windows**: ícone na Área de Trabalho e no Menu Iniciar.
   - **Linux**: ícone na Área de Trabalho e uma entrada "Gerador de
     Etiquetas" no menu de aplicativos.

Depois de rodar o instalador uma vez, o programa pode ser aberto sempre
pelo ícone criado - sem terminal, sem Python visível para quem for usar.
Requer apenas que o **Python 3.10+** já esteja instalado no PC (com
Tkinter). Em distribuições Linux baseadas em Debian/Ubuntu, se faltar,
instale antes: `sudo apt install python3-venv python3-tk python3-pil.imagetk`.

### Opção 2 - Executável já pronto

Se você já recebeu a pasta `dist/` com o binário (`main.exe` no Windows
ou `main` no Linux), pode pular o instalador: no Windows é só dar duplo
clique; no Linux, rode `./instalar.sh` mesmo assim (ele detecta que o
binário já existe e só cria os atalhos), ou execute `./dist/main`
direto pelo terminal.

### Opção 3 - Rodando a partir do código-fonte, sem gerar executável

```bash
# Windows
setup.bat        # instala tudo
executar.bat     # abre o programa

# Linux / macOS
./setup.sh
./.venv/bin/python main.py
```

Instalação totalmente manual (sem nenhum script), se preferir:

```bash
pip install -r requirements.txt
python main.py
```

## Estrutura do projeto

```
GeradorEtiquetas/
├── main.py             # ponto de entrada
├── interface.py         # interface gráfica (CustomTkinter)
├── pdf.py                # desenho vetorial da etiqueta + geração do PDF
├── printer.py             # decide a estratégia de impressão por SO
├── printer_windows.py      # impressão nativa via GDI (Windows)
├── icons.py                 # ícones vetoriais da etiqueta impressa (ReportLab)
├── ui_icons.py               # ícones vetoriais da interface (PIL/CTkImage)
├── config.py                  # cores, fontes, medidas e textos centrais
├── requirements.txt
├── setup.bat / setup.sh          # instalação automática (venv + dependências)
├── instalar.bat / instalar.sh     # instalador de um clique (build + atalhos)
├── executar.bat                    # abre o programa usando o venv (Windows)
├── main.spec                        # empacotamento em executável autônomo (PyInstaller)
├── GeradorEtiquetas.desktop           # modelo do atalho Linux (usado por instalar.sh)
└── assets/
    └── icons/icon.png, icon.ico          # ícone do programa (janela, atalhos e .exe)
```

## Funcionalidades

- Preenchimento dos campos **Cliente, Cidade, Pedido, Produto, Unidades,
  Metros (m²) e Observação**, cada um com seu ícone, no mesmo estilo da
  etiqueta impressa.
- **Imprimir**: abre uma janela de **opções de impressão** (escolha da
  impressora e número de cópias) e só então gera a etiqueta em vetor e
  envia para a impressora selecionada, sem abrir janela de visualização
  do PDF.
- **Exportar PDF**: salva a etiqueta em PDF, em alta resolução, no
  tamanho real (150 mm x 100 mm), sem perda de qualidade.
- **Limpar campos**: apaga todos os campos preenchidos.

## Atalhos de teclado

| Atalho     | Ação                          |
|------------|-------------------------------|
| `Enter`    | Vai para o próximo campo      |
| `Esc`      | Limpa todos os campos         |
| `Ctrl + P` | Abre as opções de impressão   |
| `Ctrl + S` | Exporta a etiqueta em PDF     |

## Campos Unidades e Metros

Dois campos numéricos simples, lado a lado (sem precisar decorar nenhum
formato especial): **Unidades** (ex: `15`) e **Metros** (ex: `40,65`, o
sufixo "m²" é adicionado automaticamente na etiqueta).

## Impressão

Ao clicar em **Imprimir** (ou `Ctrl+P`), uma janela de opções é aberta
antes do envio, permitindo escolher a impressora (lista todas as
instaladas no sistema, com a padrão pré-selecionada) e o número de
cópias.

- **Windows (recomendado)**: instale as dependências extras para impressão
  nativa e silenciosa via GDI, sem depender de nenhum leitor de PDF:
  ```bash
  pip install pywin32 pymupdf
  ```
  Com elas instaladas, o programa desenha a etiqueta direto no driver da
  impressora escolhida (ou na padrão do Windows), sem abrir nenhuma
  janela. **Sem essas duas dependências**, o programa cai para o método
  alternativo (abrir o PDF com o leitor padrão e mandar imprimir), que é
  menos confiável e pode falhar se não houver leitor de PDF associado ou
  impressora padrão configurada — nesse caso o programa mostra uma
  mensagem explicando o motivo.
- **Linux/macOS**: usa o utilitário `lp` (CUPS). Se aparecer o erro
  "comando 'lp' não encontrado", instale o CUPS (`sudo apt install cups`
  no Ubuntu/Debian) e garanta que exista uma impressora configurada
  (`lpstat -p` lista as impressoras disponíveis).

Em qualquer sistema, se a impressão falhar o programa explica o motivo na
tela (impressora padrão não configurada, comando ausente, etc.) em vez de
falhar silenciosamente.

## Gerando o executável autônomo manualmente

`instalar.bat` / `instalar.sh` já fazem todo o processo abaixo sozinhos
(veja "Instalação" no topo). Esta seção é só para quem quiser rodar os
passos manualmente ou entender o que o instalador faz por baixo dos panos.

O projeto já inclui `main.spec`, configurado para empacotar tudo (temas
do CustomTkinter, ícones, dependências opcionais do Windows) em um único
binário. O **mesmo comando** funciona nos dois sistemas - o PyInstaller
sempre empacota para a plataforma em que ele próprio é executado:

```bash
pip install -r requirements.txt pyinstaller
# no Windows, para impressão nativa, instale também: pip install pywin32 pymupdf
pyinstaller main.spec
```

- **Windows**: gera `dist/main.exe`. Basta dar duplo clique nele -
  não precisa de atalho nem instalação, já sai com o ícone do programa.
- **Linux**: gera `dist/main` (binário ELF autônomo). Para poder abrir
  com duplo clique / pelo menu de aplicativos (em vez de só pelo
  terminal), instale o atalho incluído no projeto:
  ```bash
  cp GeradorEtiquetas.desktop ~/.local/share/applications/   # aparece no menu de apps
  cp GeradorEtiquetas.desktop ~/Desktop/                     # ícone na área de trabalho
  chmod +x ~/Desktop/GeradorEtiquetas.desktop ~/.local/share/applications/GeradorEtiquetas.desktop
  gio set ~/Desktop/GeradorEtiquetas.desktop metadata::trusted true   # evita o aviso de "lançador não confiável"
  ```
  Se o `GeradorEtiquetas.desktop` for movido para outra pasta/PC, edite
  as linhas `Exec=` e `Icon=` dentro dele para apontar para o caminho
  real de `dist/main` e `assets/icons/icon.png` nesse PC.

> **Atenção**: sempre que o código for alterado (novos campos, ajustes de
> layout etc.), é preciso rodar `pyinstaller main.spec` de novo para que
> o executável em `dist/` reflita as mudanças - ele não se atualiza
> sozinho.


## Tamanho da etiqueta

O tamanho padrão é 150 mm x 100 mm e pode ser alterado em `config.py`
(`ETIQUETA_LARGURA_MM` / `ETIQUETA_ALTURA_MM`).

---
© 2026 Gabriel Menezes Aragão — github.com/gbmnagpng
