from pool.renderer import Renderer
from pool.verlet   import Verlet
from pygame.locals import *
import pygame as pg
import math

class Window:
	def __init__(self, title, w, h):
		pg.init()
		self.title = title;
		self.w = w;
		self.h = h;
		self.clk = pg.time.Clock();

		pg.display.init();
		surface = pg.display.set_mode(size=(w, h), vsync=1);
		pg.display.set_caption(self.title);

		pg.font.init()
		
		self.ren = Renderer(surface);

		self.vl = Verlet(w, h);
		self.vl.create_holes();
		self.vl.create_walls();
		self.vl.create_objs();
		self.score_font = pg.font.SysFont('arial', 50)

	def loop(self):
		force=5;
		brk = False;
		pause = False;
		surf = self.ren.surf;

		fonte1 = pg.font.SysFont("ubuntumono", 30, bold=True)
		mirando = False
		
		while not brk:
			if(self.vl.game_over): 
			    dead=True

			    if(self.vl.score1>self.vl.score2):
			    	vencedor=1
			    	score = self.vl.score1
			    elif(self.vl.score2>self.vl.score1):
			    	vencedor=2
			    	score = self.vl.score2
			    else:
			    	vencedor=0
			    	score = self.vl.score1

			    # Cria a superfície de texto com a pontuação final do jogador
			    if(vencedor==0):
			    	self.ren.render_text('Empatou no score ' + str(score), fonte1  , (255,0,0), (self.w / 2, self.h / 4))
			    else:
			    	self.ren.render_text('O jogador ' + str(vencedor) + ' ganhou com score ' + str(score),  fonte1,(255,0,0), (self.w / 2, self.h / 4))
			    self.ren.render_text('Pressione R para jogar novamente', fonte1, (255,0,0), (self.w / 2, self.h / 4 + 75))

			    pg.display.flip()
			    
			    while dead:
			        for event in pg.event.get():
			                    if (event.type == QUIT): # Verifica se foi clicado em fechar janela
			                        brk = True
			                        dead=False
			                        self.vl.reset()
			                    if (event.type == KEYDOWN):
			                        if event.key == K_r: # Verifica se a tecla R foi pressionada
			                            dead=False
			                            self.vl.reset()

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
			self.ren.render_rectangle(445, 495, 460, 60, (0, 0, 0))
			self.ren.render_rectangle(450, 500, 450, 50, (150, 150, 150)) 
			self.ren.render_rectangle(450, 500, 45*force, 50, (2.25*abs(force-20)*force, 10.2*force*abs(force-10), 255-255*math.exp(force/10-1)))  
			
			# Draws momentum indicator
			self.ren.render_rectangle(45, 495, 360, 60, (0, 0, 0))
			self.ren.render_rectangle(50, 500, 350, 50, (150, 150, 150))
			self.ren.render_rectangle(50, 500, 350*momentum/25, 50, (60, 46, 150))

			self.ren.render_text(str(round(momentum,3)),fonte1,(0,0,0),(60,525), 'left')


			# Parte visual da mesa
			pg.draw.line(surf, (255, 255, 255), (750, 0), (750, 450), 5)
			pg.draw.arc(surf, (255, 255, 255), (675, 160, 150, 140), -math.pi/2, math.pi/2, 5)
			pg.draw.line(surf, (100, 100, 100), (0, 0), (0, 450), 10)
			pg.draw.line(surf, (100, 100, 100), (0, 0), (950, 0), 18)
			pg.draw.line(surf, (100, 100, 100), (0, 450), (950, 445), 28)
			pg.draw.line(surf, (100, 100, 100), (950, 0), (950, 450), 30)
		
			for wall in self.vl.walls:
				self.ren.render_rectangle(wall[0], wall[1], wall[2], wall[3],(255,255,0));

			for hole in self.vl.holes:
				self.ren.render_circle(hole[0], hole[1], hole[2], (0,0,0));		

			self.clk.tick(60);

			self.ren.render_rectangle(1000, 200, 50, 50, self.vl.ballcolor);


			self.ren.render_rectangle(self.vl.psquare[0],self.vl.psquare[1], self.vl.psquare[2], self.vl.psquare[3], (255,255,0));


			s1 = self.vl.score1
			s2 = self.vl.score2

			# Cria a superfície do texto que exibe a pontuação do jogador 1
			score1_surface = self.score_font.render('Score 1: ' + str(s1), True, (0,0,0))
		    # Obtém o retângulo para posicionar o texto na tela
			score1_rect = score1_surface.get_rect()
			score1_rect.midtop = (1100 ,10)
			
		    # Exibe o texto na janela do jogo
			pg.draw.rect(surf, (255, 127, 0), score1_rect)
			self.ren.render_text('Score 1: ' + str(s1), self.score_font, (0,0,0), (1100 ,30))


			# Cria a superfície do texto que exibe a pontuação do jogador 2
			score2_surface = self.score_font.render('Score 2: ' + str(s2), True, (0,0,0))
		    # Obtém o retângulo para posicionar o texto na tela
			score2_rect = score2_surface.get_rect()
			score2_rect.midtop = (1100 ,75)
			
			# Exibe o texto na janela do jogo
			pg.draw.rect(surf, (0, 0, 255), score2_rect)
			self.ren.render_text('Score 2: ' + str(s2), self.score_font, (0,0,0), (1100 ,100))



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
		
		btn_pos = [(self.w/2)-200, self.h/7];
		btn_dim = [400, self.h/7];
		
		pg.font.init()
		fonte1 = pg.font.SysFont("ubuntumono", 30, bold=True)
		
		while not brk:
			hoverBtn1 = (pg.mouse.get_pos()[0] > btn_pos[0] and pg.mouse.get_pos()[0] < btn_pos[0]+btn_dim[0] and pg.mouse.get_pos()[1] > btn_pos[1] and pg.mouse.get_pos()[1] <  btn_pos[1]+btn_dim[1])
			hoverBtn2 = (pg.mouse.get_pos()[0] > btn_pos[0] and pg.mouse.get_pos()[0] < btn_pos[0]+btn_dim[0] and pg.mouse.get_pos()[1] > btn_pos[1]*3 and pg.mouse.get_pos()[1] < btn_pos[1]*3+btn_dim[1])
			hoverBtn3 = (pg.mouse.get_pos()[0] > btn_pos[0] and pg.mouse.get_pos()[0] <  btn_pos[0]+btn_dim[0] and pg.mouse.get_pos()[1] > btn_pos[1]*5 and pg.mouse.get_pos()[1] < btn_pos[1]*5+btn_dim[1])
			for e in pg.event.get():
				if e.type == pg.QUIT:
					prox_tela = "q"
					brk = True
					break
				if e.type == pg.KEYDOWN:
					key = pg.key.name(e.key);
					if key=='q':
						prox_tela = "q"
						brk = True
						break
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
				self.ren.render_rectangle(btn_pos[0], btn_pos[1],
				                          btn_dim[0], btn_dim[1],
										  (127, 200, 127));
			else:
				self.ren.render_rectangle(btn_pos[0], btn_pos[1],
				                          btn_dim[0], btn_dim[1],
										  (200, 255, 200));
			
			self.ren.render_text("Jogar Sinuca", fonte1, (0,0,0),(self.w/2,3*(self.h/14)))

			if not hoverBtn2:
				self.ren.render_rectangle(btn_pos[0], btn_pos[1]*3,
				                          btn_dim[0], btn_dim[1],
										  (200, 127, 127));
			else:
				self.ren.render_rectangle(btn_pos[0], btn_pos[1]*3,
				                          btn_dim[0], btn_dim[1],
										  (255, 200, 200));
			self.ren.render_text("Ajuda", fonte1, (0,0,0),(self.w/2,7*(self.h/14)))

			if not hoverBtn3:
				self.ren.render_rectangle(btn_pos[0], btn_pos[1]*5,
				                          btn_dim[0], btn_dim[1],
										  (127, 127, 200));
			else:
				self.ren.render_rectangle(btn_pos[0], btn_pos[1]*5,
				                          btn_dim[0], btn_dim[1],
										  (200, 200, 255));
			self.ren.render_text("Sair", fonte1, (0,0,0),(self.w/2,11*(self.h/14)))

			pg.display.flip()
		return prox_tela
