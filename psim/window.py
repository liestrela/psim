from psim.renderer import Renderer
from psim.verlet   import Verlet
import pygame as pg

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
		self.vl.set_max_radius(max_radius);
		self.vl.create_objs(n);
		self.vl.apply_forces();

	def loop(self):
		brk = False;
		pause = False;
		surf = self.ren.surf;

		while not brk:
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
					self.vl.create_obj_at(e.pos);

			surf.fill(self.bgcolor);

			self.clk.tick(60);

			for vo in self.vl.objs:
				self.ren.render_circle(vo.curr.x, vo.curr.y, vo.radius, vo.color);

			if not pause:
				self.vl.update();

			# update display
			pg.display.flip();
