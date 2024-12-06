# Pool game
from pool.verlet import VerletObject # Método Verlet
from math import exp, pi, isclose
from pygame.math import Vector2 as Vec2
from matplotlib import pyplot as plt
import pygame as pg
import numpy

#Definição das coordenadas das bolas na mesa
balls_pos = [
	(825, 225), # Bola branca
	
	(280, 225),
	
	(250, 210),
	(250, 240),
	
	(220, 190),
	(220, 225),
	(220, 260),
	
	(190, 180),
	(190, 210),
	(190, 240),
	(190, 270),
	
	(160, 155),
	(160, 190),
	(160, 225),
	(160, 260),
	(160, 295)
	
];

#Definição das cores da bola na mesa
balls_colors = [
	(220, 220, 220), # Bola branca
	
	(200, 200, 0),
	
	(200, 0, 0),
	(200, 135, 0),
	
	(0, 0, 200),
	(0, 0, 0),
	(119, 160, 200),
	
	(200, 180, 0),
	(200, 0, 100),
	(45, 180, 50),
	(180, 25, 180),
	
	(25, 150, 30),
	(150, 50, 100),
	(160, 100, 50),
	(100, 70, 50),
	(25, 25, 125)
];

#Definição das coordenadas dos buracos na mesa
holes = [
	(11, 11),
	(939, 11),
	(11, 439),
	(939, 439),
	(475, 11),
	(475, 439)
];

#Definição das coordenadas e dimensões das paredes 
walls = [
	(40, 10, 410, 7),
	(497, 10, 410, 7),
	(3, 40, 7, 368),
	(934, 40, 7, 368),
	(40, 430, 410, 7),
	(497, 430, 410, 7)
]; 

# Mecânica do jogo
class Game:
	def __init__(self, w, h, ren, vl):
		self.w = w; # Largura da janela
		self.h = h; # Altura da janela
		self.ren = ren; # Renderizador
		self.vl = vl; # Método Verlet
		self.brk = False; # Break do jogo
		self.player = 0; # Turno (0 ou 1)
		self.score = [0, 0]; # Placares dos jogadores
		self.score_font = pg.font.SysFont(None, 50);
		self.aiming = False; # Se o jogador está mirando
		self.moving = False; # Se as bolas ainda estão em movimento
		self.cue_force = 15; # Força inicial para tacada
		self.cue_force_max = 25; # Força máxima da tacada
		self.cue_force_min = 5; # Força miníma da tacada
		self.ended = False # Se o jogo acabou
		self.kin = 0; # Energia cinética da bola branca
		self.vel = 0; # Velocidade da bola branca
		self.kins = list[numpy.floating](); # Valores assumidos pela energia
		self.vels = list[numpy.floating](); # Valores assumidos pela velocidade
		self.disc_line = list[int](); # Iterações (tempo)
		self.n_iter = 0; # Nº de iterações

		# Criação das bolas 
		for i in range(len(balls_pos)):
			vo = VerletObject();
			vo.id = i+1;
			vo.prev.update(balls_pos[i]);
			vo.curr.update(balls_pos[i]);
			vo.acc.update(0, 0);
			vo.radius = 15;
			vo.color = balls_colors[i];

			self.vl.objs.append(vo);

	def shoot_ball(self, power : float , direction):
		# Dispara a bola branca
		if self.moving: return; # Na condição de ela estar parada
		self.vl.objs[0].prv = self.vl.objs[0].curr;
		self.vl.objs[0].curr += direction*power;
		self.moving = True; # Há movimento

	def increase_force(self):
		# Aumenta a força da tacada até o valor máximo
		if (self.cue_force<self.cue_force_max):
			self.cue_force += 0.25;

	def decrease_force(self):
		# Reduz a força da tacada até o valor mínimo
		if (self.cue_force>self.cue_force_min):
			self.cue_force -= 0.25;

	def draw_table(self):
		# Exibe a mesa e seus limites
		surf = self.ren.surf;

		pg.draw.line(surf, (255, 255, 255), (750, 0), (750, 450), 5);
		pg.draw.arc(surf, (255, 255, 255), (675, 160, 150, 140),
				   -pi/2, pi/2, 5);
		pg.draw.line(surf, (100, 100, 100), (0, 0), (0, 450), 10);
		pg.draw.line(surf, (100, 100, 100), (0, 0), (950, 0), 18);
		pg.draw.line(surf, (100, 100, 100), (0, 450), (950, 445), 28);
		pg.draw.line(surf, (100, 100, 100), (950, 0), (950, 450), 30);

	def draw_score(self):
		# Exibe o placar dos jogadores
		self.ren.render_text("Score 1: " + str(self.player_score[0]),
							 self.score_font, (0, 0, 0),
							 (1250, 30), "right", "middle");
		self.ren.render_text("Score 2: " + str(self.player_score[1]),
							 self.score_font, (0, 0, 0),
							 (1250, 80), "right", "middle");

	def draw_force_bar(self):
		# Exibe uma barra que representa a força da tacada
		self.ren.render_rect(45, 495, 460, 60, (0, 0, 0));
		self.ren.render_rect(50, 500, 450, 50, (150, 150, 150));
		self.ren.render_rect(50, 500, 450*((self.cue_force - self.cue_force_min)/(self.cue_force_max - self.cue_force_min)), 50,
							 (1.0,1.0,200.0));

	def draw_values(self):
		# Exibe os valores da Energia Cinética e da Velocidade
		self.ren.render_text("E.C.: " +
		                     str(round(self.kin, 1)),
							 self.score_font, (0, 0, 0),
							 (1250, 130), "right", "middle");
		
		self.ren.render_text("Velocidade: " +
		                     str(round(self.vel, 1)),
							 self.score_font, (0, 0, 0),
							 (1250, 180), "right", "middle");

	def draw_hud(self):
		# Atualiza e exibe todos os valores da interface
		self.draw_score();
		self.draw_force_bar();
		self.draw_values();

	def plot(self):
		# Plota os gráficos de energia cinética e velocidade
		fig, ax = plt.subplots(1, 2, figsize=(14, 6));

		ax[0].plot(self.disc_line, self.kins, color="blue",
		           label="Energia Cinética");
		ax[0].set_title('Energia Cinética da bola branca');
		ax[0].set(xlabel="Iteração", ylabel="Energia Cinética");
		ax[0].legend();

		ax[1].plot(self.disc_line, self.vels, color="red",
		           label="Velocidade");
		ax[1].set_title('Velocidade da bola branca');
		ax[1].set(xlabel="Iteração", ylabel="Energia Cinética");
		ax[1].legend();

		plt.waitforbuttonpress(0);
		plt.draw();
		plt.close();

	def tick(self):
		# Conforme as iterações, atualiza o jogo
		if (len(self.vl.objs) == 1): # Casos só reste a bola branca, ganha quem tiver mais pontos
			print("acabou: jogador " + str(int(not (self.player_score[0]  > self.player_score[1] ))+1) + " ganhou" )
			self.ended = True;
			
		balls = self.vl.objs;
		self.vl.set_bounds(0, 950, 5, 440);
		self.draw_table();

		# Renderiza os buracos
		for hole in holes:
			self.ren.render_circle(hole[0], hole[1], 30,
								   (0, 0, 0));
		# Renderiza as bolas 
		for ball in balls:
			self.ren.render_circle(ball.curr[0], ball.curr[1],
								   ball.radius, ball.color);

		# Renderiza o taco
		if self.aiming and not self.moving:
			self.ren.render_cue(self.vl.objs[0].curr,
								pg.mouse.get_pos(), 10,
								self.vl.objs[0].radius);
		for ball in balls:
			# Verifica se a bola caiu no buraco
			for hole in holes:
				dist = ball.curr.distance_to(Vec2(hole));
				if dist < 30:
					if (ball != balls[0]): # Desde que ela seja branca
						self.vl.objs.remove(ball); # É removida do jogo
						self.score[not self.player] += 1; # E é atribuído um ponto ao jogador do turno
					else:
						ball.prev = Vec2(balls_pos[0]); # Caso seja a bola branca, ela é retornada para sua posição original
						ball.curr = Vec2(balls_pos[0]);
						self.player = not self.player; # E o turno é passado

		all_stopped = True; 
		# Verifica se ainda há movimento na mesa
		for ball in balls:
			if ball.vel.length()>0.05:
				all_stopped = False;
				break;

		# Se não houver, registra isso e passsa o turno
		if all_stopped and self.moving:
			self.moving = False;
			self.player = not self.player;

		self.kin = (balls[0].vel.length()**2)/2; # Cálculo da energia cinética
		self.vel = balls[0].vel.length(); # Registro da velocidade

		self.kins.append(self.kin);  # Guarda a energia cinética atual
		self.vels.append(self.vel); # Guarda a velocidade

		self.disc_line.append(self.n_iter); # Guarda a iteração atual (tempo)
		self.n_iter += 1; # Incrementa o número de iterações

		self.draw_hud(); # Atualiza a interface
		self.vl.update(); # Atualiza os elementos do Método Verlet
