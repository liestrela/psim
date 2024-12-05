from pool.renderer import Renderer
from pool.verlet   import Verlet
from pool.game	   import Game
import pygame as pg

class Button:
	def __init__(self, idx, msg, color, color_hover, pos, dim):
		self.idx = idx;
		self.msg = msg;
		self.color = color;
		self.color_hover = color_hover;
		self.hover = False;
		self.pos = pos;
		self.dim = dim;

	def check_hover(self, w, h):
		mouse_x = pg.mouse.get_pos()[0];
		mouse_y = pg.mouse.get_pos()[1];

		self.hover = mouse_x > self.pos[0] and \
					 mouse_x < self.pos[0]+self.dim[0] and \
					 mouse_y > self.pos[1] and \
					 mouse_y < self.pos[1]+self.dim[1];

class Window:
	def __init__(self, title, w, h):
		self.title = title;
		self.w = w;
		self.h = h;
		self.clk = pg.time.Clock();

		pg.display.init();
		surface = pg.display.set_mode(size=(w, h), vsync=1);
		pg.display.set_caption(self.title);
		pg.font.init();

		self.fonts = [
			pg.font.SysFont(None, 30, bold=True)
		];

		# Default button positions
		def_btn_x = (self.w/2)-200;
		def_btn_y = (self.h)/7;

		self.buttons = [
			Button(0, "Jogar", (127, 200, 127), (200, 255, 200),
				(def_btn_x, def_btn_y), (400, self.h/7)),
			Button(1, "Ajuda", (200, 127, 127), (255, 200, 200),
				(def_btn_x, 3*def_btn_y), (400, self.h/7)),
			Button(2, "Sair",  (127, 127, 200), (200, 200, 255),
				(def_btn_x, 5*def_btn_y), (400, self.h/7))
		];
		
		self.btn_pos = [(self.w)/2-200, self.h/7];
		self.btn_dim = [400, self.h/7];

		self.ren = Renderer(surface);
		self.vl = Verlet(w, h);
		self.game = Game(w, h, self.ren, self.vl);

	def draw_buttons(self):
		for btn in self.buttons:
			color = btn.color_hover if btn.hover else btn.color;

			self.ren.render_rect(self.btn_pos[0],
								 (1+2*btn.idx)*self.btn_pos[1],
								 self.btn_dim[0], self.btn_dim[1],
								 color);
			self.ren.render_text(btn.msg, self.fonts[0],
								 (0, 0, 0), (self.w/2,
								 (3+4*btn.idx)*(self.h/14)), "center",
								 "middle");
	def loop(self):
		brk = False;
		pause = True;
		surf = self.ren.surf;
		menu_click = False;

		while not brk:
			# Force setup
			if pg.key.get_pressed()[pg.K_w]:
				self.game.increase_force();
			if pg.key.get_pressed()[pg.K_s]:
				self.game.decrease_force();

			for e in pg.event.get():
				if e.type == pg.MOUSEBUTTONDOWN:
					if pause:
						menu_click = True;

						if self.buttons[1].hover:
							print("help");
							continue;
						if self.buttons[2].hover:
							brk = True;
							continue;
					else:
						menu_click = False;
						self.game.aiming = True;

				if e.type == pg.MOUSEBUTTONUP:
					if not pause and not menu_click:
						menu_click = not menu_click;
						self.game.shoot_ball(10.0, pg.math.Vector2.normalize(e.pos - self.vl.objs[0].curr))
						self.game.aiming = False;

					if pause and menu_click:
						menu_click = not menu_click;
						if self.buttons[0].hover:
							if pause:
								pg.display.set_caption(self.title);

							pause = not pause;
							continue;

				if e.type == pg.QUIT:
					brk = True;
				if e.type == pg.KEYDOWN:
					key = pg.key.name(e.key);
					if key=='q':
						brk = True;
					if key=='p':
						if pause:
							pg.display.set_caption(self.title);

						pause = not pause;

			surf.fill(self.bgcolor);

			if pause:
				pg.display.set_caption("Menu");

				for btn in self.buttons:
					btn.check_hover(self.w, self.h);

				self.draw_buttons();
			else:
				self.clk.tick(60);
				self.game.tick();

			# Update display
			pg.display.flip();
