#!/bin/env python3
from pool.window import Window
import sys

# Resolução padrão da janela
W = 1300; # Definição da largura da janela
H = 600; # Definição da altura da janela
bg_color = (35, 125, 15); # Definição da cor de fundo

if __name__ == "__main__":
	win = Window("Sinuca", W, H); # Cria janela do jogo

	win.bgcolor = bg_color; # Cor de fundo da janela
	win.loop(); # Loop da janela
