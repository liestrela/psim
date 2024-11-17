import pygame as pg

class Renderer:
	def __init__(self, surf):
		self.surf = surf;
	
	def render_circle(self, x, y, r, color):
		pg.draw.circle(self.surf, color, (x, y), r);

	def render_rectangle(self, x, y, w, h, color):
		pg.draw.rect(self.surf, color, (x, y, w,h));