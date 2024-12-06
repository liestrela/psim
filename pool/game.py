# Pool game
from pool.verlet import VerletObject
from math import exp, pi, isclose
from pygame.math import Vector2 as Vec2
from matplotlib import pyplot as plt
import pygame as pg
import numpy

balls_pos = [
	(825, 225), # White ball
	
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

balls_colors = [
	(220, 220, 220), # White ball
	
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

holes = [
	(11, 11),
	(939, 11),
	(11, 439),
	(939, 439),
	(475, 11),
	(475, 439)
];

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
		self.w = w;
		self.h = h;
		self.ren = ren;
		self.vl = vl;
		self.brk = False;
		self.player = 0;
		self.score = [0, 0];
		self.score_font = pg.font.SysFont(None, 50);
		self.aiming = False;
		self.moving = False;
		self.cue_force = 15;
		self.cue_force_max = 25;
		self.cue_force_min = 5;
		self.ended = False
		self.kin = 0;
		self.vel = 0;
		self.kins = list[numpy.floating]();
		self.vels = list[numpy.floating]();
		self.disc_line = list[int]();
		self.n_iter = 0;

		# Create game balls
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
		if self.moving: return;
		self.vl.objs[0].prv = self.vl.objs[0].curr;
		self.vl.objs[0].curr += direction*power;
		self.moving = True;

	def increase_force(self):
		if (self.cue_force<self.cue_force_max):
			self.cue_force += 0.25;

	def decrease_force(self):
		if (self.cue_force>self.cue_force_min):
			self.cue_force -= 0.25;

	def draw_table(self):
		surf = self.ren.surf;

		pg.draw.line(surf, (255, 255, 255), (750, 0), (750, 450), 5);
		pg.draw.arc(surf, (255, 255, 255), (675, 160, 150, 140),
				   -pi/2, pi/2, 5);
		pg.draw.line(surf, (100, 100, 100), (0, 0), (0, 450), 10);
		pg.draw.line(surf, (100, 100, 100), (0, 0), (950, 0), 18);
		pg.draw.line(surf, (100, 100, 100), (0, 450), (950, 445), 28);
		pg.draw.line(surf, (100, 100, 100), (950, 0), (950, 450), 30);

	def draw_score(self):
		self.ren.render_text("Score 1: " + str(self.score[0]),
							 self.score_font, (0, 0, 0),
							 (1250, 30), "right", "middle");
		self.ren.render_text("Score 2: " + str(self.score[1]),
							 self.score_font, (0, 0, 0),
							 (1250, 80), "right", "middle");

	def draw_force_bar(self):
		self.ren.render_rect(45, 495, 460, 60, (0, 0, 0));
		self.ren.render_rect(50, 500, 450, 50, (150, 150, 150));
		self.ren.render_rect(50, 500, 450*((self.cue_force - self.cue_force_min)/(self.cue_force_max - self.cue_force_min)), 50,
							 (1.0,1.0,200.0));

	def draw_values(self):
		self.ren.render_text("E.C.: " +
		                     str(round(self.kin, 1)),
							 self.score_font, (0, 0, 0),
							 (1250, 130), "right", "middle");
		
		self.ren.render_text("Velocidade: " +
		                     str(round(self.vel, 1)),
							 self.score_font, (0, 0, 0),
							 (1250, 180), "right", "middle");

	def draw_hud(self):
		self.draw_score();
		self.draw_force_bar();
		self.draw_values();

	def plot(self):
		fig, ax = plt.subplots(1, 2, figsize=(14, 6));

		ax[0].plot(self.disc_line, self.kins, color="blue",
		           label="Energia Cinética");
		ax[0].set_title('Energia Cinética da bola branca');
		ax[0].set(xlabel="Iteração", ylabel="Energia Cinética");
		ax[0].legend();

		ax[1].plot(self.disc_line, self.vels, color="green",
		           label="Velocidade");
		ax[1].set_title('Velocidade da bola branca');
		ax[1].set(xlabel="Iteração", ylabel="Energia Cinética");
		ax[1].legend();

		plt.draw();
		plt.show();
		plt.ioff();
		plt.show();

	def tick(self):
		if (len(self.vl.objs) == 1):
			print("acabou: jogador " + str(int(not (self.player_score[0]  > self.player_score[1] ))+1) + " ganhou" )
			self.ended = True;
			
		balls = self.vl.objs;
		self.vl.set_bounds(0, 950, 5, 440);
		self.draw_table();

		# Rendering holes
		for hole in holes:
			self.ren.render_circle(hole[0], hole[1], 30,
								   (0, 0, 0));

		# Rendering balls
		for ball in balls:
			self.ren.render_circle(ball.curr[0], ball.curr[1],
								   ball.radius, ball.color);

		# Rendering cue
		if self.aiming and not self.moving:
			self.ren.render_cue(self.vl.objs[0].curr,
								pg.mouse.get_pos(), 10,
								self.vl.objs[0].radius);
		for ball in balls:
			# Check ball pocket
			for hole in holes:
				dist = ball.curr.distance_to(Vec2(hole));
				if dist < 30:
					if (ball != balls[0]):
						self.vl.objs.remove(ball);
						self.score[not self.player] += 1;
					else:
						ball.prev = Vec2(balls_pos[0]);
						ball.curr = Vec2(balls_pos[0]);
						self.player = not self.player;

		all_stopped = True;
		for ball in balls:
			if ball.vel.length()>0.05:
				all_stopped = False;
				break;

		if all_stopped and self.moving:
			self.moving = False;
			self.player = not self.player;

		self.kin = (balls[0].vel.length()**2)/2;
		self.vel = balls[0].vel.length();

		self.kins.append(self.kin);
		self.vels.append(self.vel);

		self.disc_line.append(self.n_iter);
		self.n_iter += 1;

		self.draw_hud();
		self.vl.update();
