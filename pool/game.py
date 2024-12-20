# Jogo Principal - Sinuca
from pool.verlet import VerletObject # Objeto (bola) da simulação
from math import exp, pi, isclose
from pygame.math import Vector2 as Vec2 # Vetores bidimensionais
from matplotlib import pyplot as plt
import pygame as pg
import numpy

# Posições das bolas do jogo
balls_pos = [
	(825, 225), # Bola branca
	(280, 225), (250, 210), (250, 240),
	(220, 190), (220, 225),	(220, 260),
	(190, 180),	(190, 210), (190, 240),
	(190, 270), (160, 155),	(160, 190),
	(160, 225),	(160, 260),	(160, 295)
];

# Cores das bolas do jogo RGB
balls_colors = [
	(220, 220, 220), # Bola branca
	(200, 200, 0), (200, 0, 0), (200, 135, 0),
	(0, 0, 200), (0, 0, 0), (119, 160, 200),
	(200, 180, 0), (200, 0, 100), (45, 180, 50),
	(180, 25, 180), (25, 150, 30), (150, 50, 100),
	(160, 100, 50), (100, 70, 50), (25, 25, 125)
];

# Posições das caçapas na mesa
holes = [
	(11, 11),
	(939, 11),
	(11, 439),
	(939, 439),
	(475, 11),
	(475, 439)
];

# Posições das bordas da mesa
walls = [
	(40, 10, 410, 7),
	(497, 10, 410, 7),
	(3, 40, 7, 368),
	(934, 40, 7, 368),
	(40, 430, 410, 7),
	(497, 430, 410, 7)
]; 

class Game:
	def __init__(self, w, h, ren, vl):
	# Parâmetros:	w (float): largura da janela
	#		h (float): altura da janela
	#		ren: Renderizador
	#		vl: Física implementada
		self.w = w;
		self.h = h;
		self.ren = ren;
		self.vl = vl;
		self.brk = False;
		self.player = 0; # Indica qual jogador está jogando
		self.score = [0, 0]; # Pontuação dos jogadores
		self.score_font = pg.font.SysFont(None, 50); # Fonte para as pontuações
		self.aiming = False; # Indica que o jogador está mirando
		self.moving = False; # Indica que existem bolas se movendo
		self.cue_force = 15; # Força do taco
		self.cue_force_max = 25; # Força máxima do taco
		self.cue_force_min = 5; # Força mínima do taco
		self.ended = False; # Indica que o jogo terminou
		self.end = False # Flag para terminar do jogo

		self.kin = 0; # Energia cinética da bola branca
		self.kin2 = 0; # Energia cinética da última bola acertada
		self.vel = 0; # Velocidade da bola branca
		self.last_hit = None; # Última bola com que a branca colidiu

		# Conjuntos de dados para plotagem dos gráficos
		self.kins  = list[numpy.floating]();
		self.kins2 = list[numpy.floating]();
		self.vels = list[numpy.floating]();
		self.disc_line = list[int]();
		self.n_iter = 0; # Iteração atual

		# Cria as bolas do jogo
		for i in range(len(balls_pos)):
			vo = VerletObject();
			vo.id = i+1;
			vo.prev.update(balls_pos[i]);
			vo.curr.update(balls_pos[i]);
			vo.acc.update(0, 0);
			vo.radius = 15;
			vo.color = balls_colors[i];

			self.vl.objs.append(vo);

	# Acerta a bola branca com uma intensidade dada
	def shoot_ball(self, power : float , direction):
	# Parâmetros:	power (float): intensidade da força
	#		direction (vec2): vetor normalizado da direção
		
		# Desde que não haja bolas em movimento
		if self.moving: return; 
		self.vl.objs[0].prv = self.vl.objs[0].curr;
		self.vl.objs[0].curr += direction*power;
		self.moving = True;

	# Aumenta a força do taco
	def increase_force(self):
		if (self.cue_force<self.cue_force_max):
			self.cue_force += 0.25;

	# Diminui a força do taco
	def decrease_force(self):
		if (self.cue_force>self.cue_force_min):
			self.cue_force -= 0.25;

	# Renderiza a mesa na tela
	def draw_table(self):
		surf = self.ren.surf;

		pg.draw.line(surf, (255, 255, 255), (750, 0), (750, 450), 5);
		pg.draw.arc(surf, (255, 255, 255), (675, 160, 150, 140),
				   -pi/2, pi/2, 5);
		pg.draw.line(surf, (100, 100, 100), (0, 0), (0, 450), 10);
		pg.draw.line(surf, (100, 100, 100), (0, 0), (950, 0), 18);
		pg.draw.line(surf, (100, 100, 100), (0, 450), (950, 445), 28);
		pg.draw.line(surf, (100, 100, 100), (950, 0), (950, 450), 30);

	# Renderiza as pontuações na tela
	def draw_score(self):
		self.ren.render_text("Score 1: " + str(self.score[0]),
							 self.score_font, (0, 0, 0),
							 (1250, 30), "right", "middle");
		self.ren.render_text("Score 2: " + str(self.score[1]),
							 self.score_font, (0, 0, 0),
							 (1250, 80), "right", "middle");

	# Renderiza a barra de força do taco na tela
	def draw_force_bar(self):
		self.ren.render_rect(45, 495, 460, 60, (0, 0, 0));
		self.ren.render_rect(50, 500, 450, 50, (150, 150, 150));
		self.ren.render_rect(50, 500, 450*((self.cue_force - self.cue_force_min)/(self.cue_force_max - self.cue_force_min)), 50,
							 (1.0,1.0,200.0));
	
	# Desenha valores de energia e velocidade na tela
	def draw_values(self):
		self.ren.render_text("E.C.: " +
		                     str(round(self.kin, 1)),
							 self.score_font, (0, 0, 0),
							 (1250, 130), "right", "middle");

		self.ren.render_text("E.C. acertada: " +
		                     str(round(self.kin2, 1)),
							 self.score_font, (0, 0, 0),
							 (1250, 180), "right", "middle");

		self.ren.render_text("Velocidade: " +
		                     str(round(self.vel, 1)),
							 self.score_font, (0, 0, 0),
							 (1250, 230), "right", "middle");

	# Desenha o HUD na tela
	def draw_hud(self):
		self.draw_score();
		self.draw_force_bar();
		self.draw_values();

	# Renderiza a tela de "venceu"
	def draw_win(self):
		msg = "Jogador " + str(int(not(self.score[0]>self.score[1]))+1) + " venceu!";
		self.ren.render_text(msg, self.score_font, (0, 0, 0),
		                     (self.w/2, self.h/2), "center", "middle");
		pg.display.flip();
		pg.time.delay(1500);

	# Plota os gráficos da simulação usando MatPlotLib
	def plot(self):
		fig, ax = plt.subplots(1, 3, figsize=(14, 6));

		# Energia cinética da bola branca
		ax[0].plot(self.disc_line, self.kins, color="blue",
		           label="Energia Cinética");
		ax[0].set_title('Energia Cinética da bola branca');
		ax[0].set(xlabel="Iteração", ylabel="Energia Cinética");
		ax[0].legend();

		# Velocidade da bola branca
		ax[1].plot(self.disc_line, self.vels, color="red",
		           label="Velocidade");
		ax[1].set_title('Velocidade da bola branca');
		ax[1].set(xlabel="Iteração", ylabel="Energia Cinética");
		ax[1].legend();

		# Energia cinética da última bola atingida
		ax[2].plot(self.disc_line, self.kins2, color="green",
		           label="Energia Cinética");
		ax[2].set_title('Energia Cinética da bola acertada');
		ax[2].set(xlabel="Iteração", ylabel="Energia Cinética");
		ax[2].legend();

		plt.waitforbuttonpress(0);
		plt.draw();
		plt.close();

	# Iteração da simulação
	def tick(self):
		# Se apenas restar a bola branca, o jogo acaba
		if (len(self.vl.objs) == 1):
			self.ended = True;

		# Se o jogo não acabou, atualiza a simulação.
		if not self.ended:
			balls = self.vl.objs; # Bolas do jogo
			self.vl.set_bounds(0, 950, 5, 440); # Limites da mesa
			self.draw_table(); # Exibição da mesa

			# Renderizando caçapas
			for hole in holes:
				self.ren.render_circle(hole[0], hole[1], 30,
									   (0, 0, 0));

			# Renderizando bolas
			for ball in balls:
				self.ren.render_circle(ball.curr[0], ball.curr[1],
									   ball.radius, ball.color);

			# Renderizando taco
			if self.aiming and not self.moving:
				self.ren.render_cue(self.vl.objs[0].curr,
									pg.mouse.get_pos(), 10,
									self.vl.objs[0].radius);

			# Verifica se alguma bola foi encaçapada
			for ball in balls:
				for hole in holes:
					dist = ball.curr.distance_to(Vec2(hole));
					if dist < 30:
						if (ball != balls[0]):  # Desde que ela não seja branca
							self.vl.objs.remove(ball); # É removida do jogo
							self.score[not self.player] += 1; # E é somado um ponto ao score do jogador do turno
						else:
							ball.prev = Vec2(balls_pos[0]); # Caso seja a bola branca, ela é retornada para sua posição original
							ball.curr = Vec2(balls_pos[0]);
							self.player = not self.player; # E o turno é passado

			# Verifica se existem bolas se movendo
			all_stopped = True;
			for ball in balls:
				if ball.vel.length()>0.05:
					all_stopped = False;
					break;
					
			# Se não houver, registra isso e passsa o turno
			if all_stopped and self.moving:
				self.moving = False;
				self.player = not self.player;

			# Procura bola colidindo
			for ball in balls:
				if (ball == balls[0]): continue;
				dist = (balls[0].curr-ball.curr).length();
				if dist <= 2*ball.radius+1:
					self.last_hit = ball;
					break;

			# Atualiza valores para plotagem
			self.kin  = (balls[0].vel.length()**2)/2;

			if self.last_hit:
				self.kin2 = (self.last_hit.vel.length()**2)/2; # Cálculo da energia cinética
			self.vel = balls[0].vel.length(); # Registro da velocidade

			self.kins.append(self.kin); # Guarda a energia cinética atual da bola branca (em cada iteração)
			self.kins2.append(self.kin2); # Guarda a energia cinética atual da última bola com que a branca entrou em contato (em cada iteração)
			self.vels.append(self.vel); # Guarda a velocidade atual da bola branca (em cada iteração)

			self.disc_line.append(self.n_iter);  # Guarda a iteração atual (tempo)
			self.n_iter += 1; # Incrementa o número de iterações

			# Desenha o HUD
			self.draw_hud();

			# Calcula as novas posições pelo método de Verlet
			self.vl.update();
		else:
			self.draw_win(); # Exibe mensagem de vitória
			self.end = True; # Indica que o jogo acabou
