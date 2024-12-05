# Pool game
from pool.verlet import VerletObject
from math import exp, pi, isclose
import pygame as pg
from pygame.math import Vector2 as Vec2

balls_pos = [
	(825, 225), # White ball
	(150, 125),
	(750, 295),
	(750, 155),
	(750, 225),
	(475, 225),
	(150, 225),
	(20,  225)
];

balls_colors = [
	(220, 220, 220), # White ball
	(200, 0, 0),
	(200, 200, 0),
	(0, 200, 0),
	(200, 100, 0),
	(0, 0, 200),
	(200, 100, 100),
	(25, 25, 25)
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
		self.cue_force = 5;

		# Create game balls
		for i in range(0, 8):
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
		if (self.cue_force<10):
			self.cue_force += 0.25;

	def decrease_force(self):
		if (self.cue_force>1):
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
		color1 = (0, 0, 0);
		color2 = (0, 0, 0);

		self.ren.render_text("Score 1: " + str(self.score[0]),
							 self.score_font, color1,
							 (1200, 30), "right", "middle");
		self.ren.render_text("Score 2: " + str(self.score[1]),
							 self.score_font, color2,
							 (1200, 80), "right", "middle");

	def draw_force_bar(self):
		self.ren.render_rect(45, 495, 460, 60, (0, 0, 0));
		self.ren.render_rect(50, 500, 450, 50, (150, 150, 150));
		self.ren.render_rect(50, 500, 45*self.cue_force, 50,
							 (2.25*abs(self.cue_force-20)*
							 self.cue_force,
							 10.2*self.cue_force*
							 abs(self.cue_force-10),
							 255-255*exp(self.cue_force/10-1)));

	def draw_hud(self):
		self.draw_score();
		self.draw_force_bar();

	def tick(self):
		balls = self.vl.objs;

		self.vl.set_bounds(0, 950, 5, 440);
		self.draw_table();

		# Rendering balls
		for ball in balls:
			self.ren.render_circle(ball.curr[0], ball.curr[1],
								   ball.radius, ball.color);

		# Rendering holes
		for hole in holes:
			self.ren.render_circle(hole[0], hole[1], 30,
								   (0, 0, 0));
		
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

		self.draw_hud();
		self.vl.update();
