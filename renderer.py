import pygame as pg
import math
from typing import Literal # SOMENTE PARA ESPECIFICAR O TIPO DE ENTRADA

class Renderer:
	def __init__(self, surf):
		self.surf = surf;
	
	def render_circle(self, x, y, r, color):
		pg.draw.circle(self.surf, color, (x, y), r);

	def render_rectangle(self, x, y, w, h, color):
		pg.draw.rect(self.surf, color, (x, y, w,h));

	def render_taco(self, base, fim, forca, raio_da_bolinha=15):
		dist = math.sqrt((fim[0]-base[0])**2 + (base[1]-fim[1])**2)
		sin = (fim[1]-base[1])/(dist) # norma vertical
		cos = (fim[0]-base[0])/(dist) # norma horizontal
		
		widthTaco = 10 # largura (raio) do taco
		lenTaco = -400 # comprimento do taco
		fm = -10 # multiplicador da força para representá-la pela distância do taco
		offset = (fm*forca*cos, fm*forca*sin)
		ponta1 = (offset[0]+base[0]+(sin*widthTaco/2)+(cos*raio_da_bolinha), offset[1]+(sin*raio_da_bolinha)+base[1]-(cos*widthTaco/2))
		ponta2 = (ponta1[0]+(cos*lenTaco),ponta1[1]+(sin*lenTaco))
		ponta3 = (ponta2[0]-(sin*widthTaco), ponta2[1]+(cos*widthTaco))
		ponta4 = (ponta3[0]-(cos*lenTaco),ponta3[1]-(sin*lenTaco))
		pg.draw.polygon(self.surf, (111,78,55), (ponta1,ponta2,ponta3,ponta4))
	
	def render_text(self, surf, txt, fonte, cor, pos, justifyX:Literal['center','left','right']='center', justifyY:Literal['middle','top','bottom']='middle'): # inspirado pelo canal Coding With Russ (https://www.youtube.com/watch?v=ndtFoWWBAoE)
		img = fonte.render(txt, True, cor)
		width = img.get_width()
		height = img.get_height()

		x=pos[0]
		y=pos[1]
		if justifyX == 'center':
			x = pos[0] - (width/2)
		elif justifyX == 'right':
			x = pos[0] - width
		if justifyY == 'middle':
			y = pos[1] - (height/2)
		elif justifyY == 'bottom':
			y = pos[1] - height
		
		surf.blit(img,(x,y))