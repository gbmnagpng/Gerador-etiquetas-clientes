# -*- coding: utf-8 -*-
"""
main.py
-------
Ponto de entrada do Gerador de Etiquetas.

Execute com:
    python main.py

Requisitos (ver requirements.txt):
    pip install customtkinter reportlab pillow
"""

from interface import App


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
