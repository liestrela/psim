import pygame as pg
import pygame.gfxdraw as gfxdraw
from math import sqrt
from math import cos as mcos
from math import sin as msin

class Renderer:
	def __init__(self, surf):
		self.surf = surf;
	
	def render_circle(self, x, y, r, color):
		pg.draw.circle(self.surf, color, (x, y), r);
	
	def render_rect(self, x, y, w, h, color):
		pg.draw.rect(self.surf, color, (x, y, w, h));

	def render_text(self, msg, font, color, pos, just_x, just_y):
		surf = font.render(msg, True, color);
		f_pos = list(pos);
		width = surf.get_width();
		height = surf.get_height();

		if just_x == "center":
			f_pos[0] -= width/2;
		if just_x == "right":
			f_pos[0] -= width;
		if just_y == "middle":
			f_pos[1] -= height/2;
		if just_y == "bottom":
			f_pos[1] -= height;

		self.surf.blit(surf, (f_pos[0], f_pos[1]));

	def render_cue(self, base, end, force, radius=15):
		dist = sqrt((end[0]-base[0])**2+(base[1]-end[1])**2);
		sin = (end[1]-base[1])/dist;
		cos = (end[0]-base[0])/dist;
		width = 10;
		cue_len = 400;

		offset = (-10*force*cos, -10*force*sin);

		vtx_1 = (offset[0]+base[0]+(sin*width/2)+(cos*radius),
		         offset[1]+(sin*radius)+base[1]-(cos*width/2));
		vtx_2 = (vtx_1[0]+(cos*(-cue_len)), vtx_1[1]+(sin*(-cue_len)));
		vtx_3 = (vtx_2[0]-(sin*width), vtx_2[1]+(cos*width));
		vtx_4 = (vtx_3[0]-(cos*(-cue_len)), vtx_3[1]-(sin*(-cue_len)));

		pg.draw.polygon(self.surf, (111, 78, 55),
		                (vtx_1, vtx_2, vtx_3, vtx_4));
	
	def render_arc(self, x, y, r, th, start, stop, color):
		p_outer  = [];
		p_inner = [];
		n = round(r*abs(stop-start)/20);

		if n<2: n=2;

		for i in range(n):
			delta = i/(n-1);
			phi_0 = start+(stop-start)*delta;
			x_0 = round(x+r*mcos(phi_0));
			y_0 = round(y+r*msin(phi_0));
			p_outer.append([x_0, y_0]);

			phi_1 = stop+(start-stop)*delta;
			x_1 = round(x+(r-th)*mcos(phi_1));
			y_1 = round(y+(r-th)*msin(phi_1));
			p_inner.append([x_1, y_1]);

		points = p_outer+p_inner;
		gfxdraw.aapolygon(self.surf, points, color);
		gfxdraw.filled_polygon(self.surf, points, color);

