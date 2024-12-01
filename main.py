#!/bin/env python3
from pool.window import Window
import sys

W = 1300;
H = 600;

if __name__ == "__main__":
	win = Window("Sinuca", W, H);

	win.bgcolor = (0x0, 0x28, 0x3c);
	tela = "menu"
	while True:
		if tela == "menu":
			tela = win.menu()
		elif tela == "jogo":
			tela = win.loop()
		elif tela == "q":
			break
		else:
			raise Exception(f"Erro: tela desconhecida/indisponível \"{tela}\".")
			break
