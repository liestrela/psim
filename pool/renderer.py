# Renderizador (Funções auxiliares)
import pygame as pg
import pygame.gfxdraw as gfxdraw # Para desenhos mais sofisticados
from math import sqrt
from math import cos as mcos
from math import sin as msin

class Renderer:
	def __init__(self, surf):
	# Parâmetro: Superfície
		self.surf = surf;
	
	# Renderiza um circulo de raio e cor dados na tela
	def render_circle(self, x, y, r, color):
	# Parâmetros: 	x (float): coordenada X do centro
	# 	    	y (float): coordenada Y do centro
	# 	    	r (float): raio
	# 	    	color (tupla): cor (R, G, B)
		pg.draw.circle(self.surf, color, (x, y), r);
	
	# Renderiza um retângulo de posição e dimensões dadas na tela
	def render_rect(self, x, y, w, h, color):
	# Parâmetros: 	x (float): coordenada X do vétice superior esquerdo
	# 	   	y (float): coordenada Y do vétice superior esquerdo
	# 	    	w (float): largura
	# 	    	h (float): altura
	# 	    	color (tupla): cor (R, G, B)
		pg.draw.rect(self.surf, color, (x, y, w, h));

	# Renderiza um texto dado na tela
	def render_text(self, msg, font, color, pos, just_x, just_y):
	# Parâmetros: 	msg (string): mensagem a ser exibida
	# 	    	font (fonte): fonte do texto
	# 	    	color (tupla): cor do texto (R, G, B)
	# 	    	pos (tupla): posição do texto (x, y)
	# 	    	just_x (string): alinhamento horizontal do texto
	# 	    	just_y (string): alinhamento vertical do texto

		# Renderização do texto em uma superfície
		surf = font.render(msg, True, color);
		
		# Cálcula as dimensões do texto
		f_pos = list(pos);
		width = surf.get_width();
		height = surf.get_height();

		 # Ajuste com base no alinhamento horizontal
		if just_x == "center":
			f_pos[0] -= width/2;
		if just_x == "right":
			f_pos[0] -= width;

		 # Ajuste com base no alinhamento vertical
		if just_y == "middle":
			f_pos[1] -= height/2;
		if just_y == "bottom":
			f_pos[1] -= height;

		# Exibição do texto
		self.surf.blit(surf, (f_pos[0], f_pos[1]));

	# Renderiza um polígono que representa o taco na tela
	def render_cue(self, base, end, force, radius=15):
	# Parâmetros: 	base (tupla): coordenadas da base do taco (x, y)
	# 	    	end (tupla): coordenadas da ponta do taco (x, y)
	# 	    	force (float): força a ser aplicada com o taco
	# 	    	radius (float): raio da base do taco
		
		# Cálculo da distância entre base e ponta
		dist = sqrt((end[0]-base[0])**2+(base[1]-end[1])**2);
		
		# Cálculo do seno e cosseno do ângulo formado pelo taco
		sin = (end[1]-base[1])/dist;
		cos = (end[0]-base[0])/dist;

		# Definição da largura e comprimento do taco
		width = 10;
		cue_len = 400;

		# Deslocamento do taco conforme a força a ser aplicada
		offset = (-10*force*cos, -10*force*sin);

		# Cálculo dos vértices do polígono que representa o taco
		vtx_1 = (offset[0]+base[0]+(sin*width/2)+(cos*radius),
		         offset[1]+(sin*radius)+base[1]-(cos*width/2));
		vtx_2 = (vtx_1[0]+(cos*(-cue_len)), vtx_1[1]+(sin*(-cue_len)));
		vtx_3 = (vtx_2[0]-(sin*width), vtx_2[1]+(cos*width));
		vtx_4 = (vtx_3[0]-(cos*(-cue_len)), vtx_3[1]-(sin*(-cue_len)));
		
		 # Exibição do taco de bilhar
		pg.draw.polygon(self.surf, (111, 78, 55),
		                (vtx_1, vtx_2, vtx_3, vtx_4));
