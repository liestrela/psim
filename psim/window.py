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

		pg.font.init()
		fonte1 = pg.font.SysFont("ubuntumono", 30, bold=True)
		mirando = False
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
					if key=='m':
						self.vl.set_mass(7, self.vl.get_mass(7)*1.1)
						#self.vl.set_mass(7, self.vl.get_mass(7)+1)
					if key=='n':
						self.vl.set_mass(7, self.vl.get_mass(7)*0.9)
						#self.vl.set_mass(7, self.vl.get_mass(7)-1)

				if e.type == pg.MOUSEBUTTONDOWN:
					mirando = True
				if e.type == pg.MOUSEBUTTONUP:
					if mirando == True: # se estava mirando quando soltou o botão do mouse...
						self.vl.hit_obj(e.pos, force)
						mirando = False


			cur_vel = self.vl.get_velocity(7)
			cur_vel_mod = math.sqrt(cur_vel[0]**2 + cur_vel[1]**2)
			momentum = cur_vel_mod * self.vl.get_mass(7)

			surf.fill(self.bgcolor);

			# Draws force indicator
			pg.draw.rect(surf, (0, 0, 0), (445, 495, 460, 60))
			pg.draw.rect(surf, (150, 150, 150), (450, 500, 450, 50))
			pg.draw.rect(surf, (2.25*abs(force-20)*force, 10.2*force*abs(force-10), 255-255*math.exp(force/10-1)), (450, 500, 45*force, 50))

			# Draws momentum indicator
			pg.draw.rect(surf, (0, 0, 0), (45, 495, 360, 60))
			pg.draw.rect(surf, (150, 150, 150), (50, 500, 350, 50))
			pg.draw.rect(surf, (60, 46, 150), (50, 500, 350*momentum/25, 50))

			self.ren.render_text(surf,str(round(momentum,3)),fonte1,(0,0,0),(60,525), 'left')


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

			# desenha o taco
			if mirando:
				self.ren.render_taco(self.vl.objs[7].curr,pg.mouse.get_pos(), force, self.vl.objs[7].radius)

			if not pause:
				self.vl.update();

			# update display
			pg.display.flip();
		return "menu"
	
	def menu(self):
		pg.display.set_caption("Menu")
		brk = False
		surf = self.ren.surf;
		
		hoverBtn1 = False
		hoverBtn2 = False
		hoverBtn3 = False # botão de sair

		prox_tela = "menu" # Próxima tela depois desta

		pg.font.init()
		fonte1 = pg.font.SysFont("ubuntumono", 30, bold=True)
		while not brk:
			hoverBtn1 = (pg.mouse.get_pos()[0] > 200 and pg.mouse.get_pos()[0] < 600 and pg.mouse.get_pos()[1] > 80 and pg.mouse.get_pos()[1] < 160)
			hoverBtn2 = (pg.mouse.get_pos()[0] > 200 and pg.mouse.get_pos()[0] < 600 and pg.mouse.get_pos()[1] > 240 and pg.mouse.get_pos()[1] < 320)
			hoverBtn3 = (pg.mouse.get_pos()[0] > 200 and pg.mouse.get_pos()[0] < 600 and pg.mouse.get_pos()[1] > 400 and pg.mouse.get_pos()[1] < 480)
			for e in pg.event.get():
				if e.type == pg.QUIT:
					brk = True;
				if e.type == pg.KEYDOWN:
					key = pg.key.name(e.key);
					if key=='q':
						brk = True
				if e.type == pg.MOUSEBUTTONDOWN:
					if hoverBtn1:
						prox_tela = "jogo"
						brk = True
						break
					if hoverBtn2:
						prox_tela = "ajuda"
						brk = True
						break
					if hoverBtn3:
						prox_tela = "q"
						brk = True
						break
			surf.fill(self.bgcolor)

			if not hoverBtn1:
				pg.draw.rect(surf, (127, 200, 127), ((self.w/2)-200, (self.h/7), 400, self.h/7))
			else:
				pg.draw.rect(surf, (200, 255, 200), ((self.w/2)-200, (self.h/7), 400, self.h/7))
			self.ren.render_text(surf, "Jogar Sinuca", fonte1, (0,0,0),(self.w/2,3*(self.h/14)))

			if not hoverBtn2:
				pg.draw.rect(surf, (200, 127, 127), ((self.w/2)-200, (self.h/7)*3, 400, self.h/7))
			else:
				pg.draw.rect(surf, (255, 200, 200), ((self.w/2)-200, (self.h/7)*3, 400, self.h/7))
			self.ren.render_text(surf, "Ajuda", fonte1, (0,0,0),(self.w/2,7*(self.h/14)))

			if not hoverBtn3:
				pg.draw.rect(surf, (127, 127, 200), ((self.w/2)-200, (self.h/7)*5, 400, self.h/7))
			else:
				pg.draw.rect(surf, (200, 200, 255), ((self.w/2)-200, (self.h/7)*5, 400, self.h/7))
			self.ren.render_text(surf, "Sair", fonte1, (0,0,0),(self.w/2,11*(self.h/14)))

			pg.display.flip()
		return prox_tela
