# Pool game
from pool.verlet import VerletObject
import pygame as pg

balls_pos = [
	(825, 225),
	(150, 125),
	(750, 295),
	(750, 155),
	(750, 225),
	(475, 225),
	(150, 225),
	(20,  225)
];

balls_colors = [
	(220, 220, 220),
	(200, 0, 0),
	(200, 200, 0),
	(0, 200, 0),
	(200, 100, 0),
	(0, 0, 200),
	(200, 100, 100),
	(25, 25, 25)
];

holes = [
	(11, 11 , 30),
	(939, 11, 30),
	(11, 439, 30),
	(939, 439, 30),
	(475, 11, 30),
	(475, 439, 30)
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
		self.score1 = 0;
		self.score2 = 0;
		self.score_font = pg.font.SysFont(None, 50);
		self.aiming = False;

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

	def draw_score(self):
		self.ren.render_text("Score 1: " + str(self.score1),
		                     self.score_font, (0, 0, 0),
							 (1200, 30), "right", "middle");
		self.ren.render_text("Score 2: " + str(self.score1),
		                     self.score_font, (0, 0, 0),
							 (1200, 80), "right", "middle");

	def tick(self):
		balls = self.vl.objs;

		# Rendering balls
		for ball in balls:
			self.ren.render_circle(ball.curr[0], ball.curr[1],
			                       ball.radius, ball.color);

		# Rendering walls
		for wall in walls:
			self.ren.render_rect(wall[0], wall[1], wall[2],
			                     wall[3], (255, 255, 0));

		# Rendering holes
		for hole in holes:
			self.ren.render_circle(hole[0], hole[1], hole[2],
			                       (0, 0, 0));
		
		# Rendering cue
		if self.aiming:
			self.ren.render_cue(self.vl.objs[0].curr,
			                    pg.mouse.get_pos(), 10,
								self.vl.objs[0].radius);
		self.draw_score();
		self.vl.update();
