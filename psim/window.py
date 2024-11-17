from psim.renderer import Renderer
from psim.verlet   import Verlet
import pygame as pg
import math

class Window:
	def __init__(self, title, w, h, n, max_radius):
		self.title = title;
		self.w = w;
		self.h = h;
		self.clk = pg.time.Clock();

		pg.display.init();
		surface = pg.display.set_mode(size=(w, h), vsync=1);
		pg.display.set_caption(self.title);


		self.ren = Renderer(surface);

		self.vl = Verlet(w, h);
		self.vl.create_holes();
		self.vl.create_walls();
		self.vl.set_max_radius(max_radius);
		self.vl.create_objs();
		self.vl.create_obj_at((825 ,225));

	def loop(self):
		force=5;
		brk = False;
		pause = False;
		surf = self.ren.surf;

		while not brk:

			if pg.key.get_pressed()[pg.K_s]:
				if(force>1):
					force-=0.25
			if pg.key.get_pressed()[pg.K_w]:
				if(force<10):
					force+=0.25

			for e in pg.event.get():
				if e.type == pg.QUIT:
					brk = True;
				if e.type == pg.KEYDOWN:
					key = pg.key.name(e.key);
					if key=='q':
						brk = True;
					if key=='p':
						if not pause:
							self.title += " (paused)";
						else:
							self.title = self.title[0:-9];

						pg.display.set_caption(self.title);

						pause = not pause;
				if e.type == pg.MOUSEBUTTONDOWN:
					self.vl.hit_obj(e.pos, force);




			surf.fill(self.bgcolor);
			pg.draw.rect(surf, (0, 0, 0), (445, 495, 460, 60))
			pg.draw.rect(surf, (150, 150, 150), (450, 500, 450, 50))
			pg.draw.rect(surf, (2.25*abs(force-20)*force, 10.2*force*abs(force-10), 255-255*math.exp(force/10-1)), (450, 500, 45*force, 50))

			pg.draw.line(surf, (255, 255, 255), (0, 450), (950, 450), 5)
			pg.draw.line(surf, (255, 255, 255), (950, 0), (950, 457), 5)

			pg.draw.line(surf, (255, 255, 255), (750, 0), (750, 450), 5)
			pg.draw.arc(surf, (255, 255, 255), (675, 160, 150, 140), -math.pi/2, math.pi/2, 5)

			for hole in self.vl.holes:
				self.ren.render_circle(hole[0], hole[1], hole[2], (0,0,0));			
			for wall in self.vl.walls:
				self.ren.render_rectangle(wall[0], wall[1], wall[2], wall[3],(255,255,0));
				
			self.clk.tick(60);


			for vo in self.vl.objs:
				self.ren.render_circle(vo.curr.x, vo.curr.y, vo.radius, vo.color);


			if not pause:
				self.vl.update();

			# update display
			pg.display.flip();
