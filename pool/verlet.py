from pygame.math import Vector2 as Vec2
from random import randint as randi
import math
import pygame as pg

ATRITO = 0.02;

balls_pos = [
	(150, 125),
	(750, 295),
	(750, 155),
	(750, 225),
	(475, 225),
	(150, 225),
	(20,  225),
	(825, 225)
];

balls_colors = [
	(200, 0, 0),
	(200, 200, 0),
	(0, 200, 0),
	(200, 100, 0),
	(0, 0, 200),
	(200, 100, 100),
	(25, 25, 25),
	(220, 220, 220)
];

class VerletObject:
	def __init__(self):
		self.curr = Vec2(0,0);
		self.prev = Vec2(0,0);
		self.vel  = Vec2(0,0);
		self.acc  = Vec2(0,0);
		self.radius = 0;
		self.color = (0,0,0);
		self.id = 0;
		self.mass = 1;
		self.orpos = Vec2(0,0);
		self.out = False;


class Verlet:
	def __init__(self, w, h):
		self.w = 950;
		self.h = 450;
		self.max_radius = 0;
		self.objs = [];
		self.holes = [];
		self.walls = [];
		self.score1 = 0;
		self.score2 = 0;
		self.ball = 1;
		self.turn = 1;
		self.hit = False;
		self.free = False;
		self.any = False;
		self.psquare = (1250, 10, 50, 50)
		self.ballcolor = (255, 0, 0)
		self.done = False;
		self.game_over = False;

	def reset(self):
		self.score1 = 0;
		self.score2 = 0;
		self.ball = 1;
		self.turn = 1;
		self.hit = False;
		self.free = False;
		self.any = False;
		self.psquare = (1250, 10, 50, 50)
		self.ballcolor = (255, 0, 0)
		self.done = False;
		self.game_over = False;
		for obj in self.objs:
				obj.prev.y = obj.orpos[1];
				obj.curr.y = obj.orpos[1];
				obj.prev.x = obj.orpos[0];
				obj.curr.x = obj.orpos[0];
				obj.out = False;


	def set_bounds(self, w, h):
		self.w = 950;
		self.h = 450;

	def get_velocity(self, idx):
		return self.objs[idx].vel
	
	def get_mass(self, idx):
		return self.objs[idx].mass
	def set_mass(self, idx, new_mass):
		if (new_mass > 0.5 and new_mass < 10):
			self.objs[idx].mass = new_mass

	def create_holes(self):
		self.holes = [
			(11, 11 , 30),
			(939, 11, 30),
			(11, 439, 30),
			(939, 439, 30),
			(475, 11, 30),
			(475, 439, 30)
		];

	def create_walls(self):
		self.walls = [
			(40, 10 , 410,7 ),
			(497, 10, 410,7 ),
			(3, 40, 7,368 ),
			(934, 40, 7,368),
			(40, 430, 410, 7),
			(497, 430, 410,7)
		];	
		
	def create_objs(self):
		for i in range(0, 8):
			vo = VerletObject();
			vo.id = i+1;
			vo.orpos = balls_pos[i];
			vo.prev.update(balls_pos[i]);
			vo.curr.update(balls_pos[i]);
			vo.acc.update(0, 0);
			vo.radius = 15;
			vo.color = balls_colors[i];

			self.objs.append(vo);

	def hit_obj(self, pos, force):

		if(not(self.free)):
			self.hit=False
		self.done=True

		all_stopped=True;
		for obj in self.objs:
			if(abs(obj.curr.x-obj.prev.x)>0 or abs(obj.curr.y-obj.prev.y)>0 ):
				all_stopped=False;
				break;		

		if(self.free and self.any): 
			self.any = False;
		else:
			self.free=False

		if(all_stopped):
			if(self.any):
				self.done = False;
			ye=pos[1]
			xe=pos[0]

			if(ye>450):
				ye=450

			disty=ye-self.objs[7].curr.y
			distx=xe-self.objs[7].curr.x

			module=math.sqrt(disty**2+distx**2)

			distx=distx/module
			disty=disty/module

			velocity = (1.5*force*(distx), 1.5*force*(disty));

			self.objs[7].curr += velocity;


			
		self.update()

	def set_max_radius(self, max_radius):
		self.max_radius = max_radius;

	def apply_forces(self, obj):
		vy=obj.curr[1]-obj.prev[1]
		vx=obj.curr[0]-obj.prev[0]

		theta_radians = math.atan2(abs(vy), abs(vx))

		if(abs(vy) > 0):
			obj.acc[1] = -((obj.vel[1])/abs(vy))*ATRITO*math.sin(theta_radians);
		else:
			obj.acc[1] = 0
		if(abs(vx) > 0):
			obj.acc[0] = -((obj.vel[0])/abs(vx))*ATRITO*math.cos(theta_radians);
		else:
			obj.acc[0] = 0
	
	
	def update(self):
		for obj in self.objs:
			self.check_collisions(obj);
			self.apply_forces(obj);
			self.fall(obj);
		
			vx=obj.curr.x-obj.prev.x
			vy=obj.curr.y-obj.prev.y
			ax=obj.acc.x
			ay=obj.acc.y

			vx_temp=vx
			vy_temp=vy

			vx += ax
			vy += ay

			if((vx<0 and vx_temp>0) or (vx>0 and vx_temp<0)):
				vx = 0

			if((vy<0 and vy_temp>0) or (vy>0 and vy_temp<0) ):
				vy = 0
		
			velocity = (vx,vy)

			obj.prev.x = obj.curr.x;
			obj.prev.y = obj.curr.y;

			obj.curr += velocity;
			obj.vel = velocity;

		all_stopped=True;
		for obj in self.objs:
			if(abs(obj.curr.x-obj.prev.x)>0 or abs(obj.curr.y-obj.prev.y)>0 ):
				all_stopped=False;
				break;

		if(all_stopped):
			if(not(self.any)):
				if(not(self.hit)):
					self.hit=True
					if(self.turn==1):
						if(self.score1>5):
							self.score1-=1
					elif(self.score2>5):
						self.score2-=1
				if(self.turn==1 and self.done):
					self.turn=2
					self.psquare = (1250, 75, 50, 50)
					self.done = False
				elif(self.done):
					self.turn=1
					self.psquare = (1250, 10, 50, 50)
					self.done = False

			if(self.ball>=8):
				self.game_over=True
		self.keep_inbounds();
	
	def check_collisions(self, obj):
		particle_restitution = -0.001;
		max_overlap_correction = 1000;
		velocity_threshold = 0.2;
		slow_collision_factor = 0.4;
		damp_fac = 0.97;

		for other in self.objs:
			if other.id == obj.id:
				continue;

			delta = other.curr - obj.curr;
			dist = delta.length();

			if dist <= obj.radius + other.radius:
				if((other.id==self.ball and obj.id==8) or (other.id==8 and obj.id==self.ball)):
					self.hit=True;

			if dist <= obj.radius + other.radius:
				if dist > 0:
					normal = delta/dist;
				else:
					normal = delta*0;

				overlap = (obj.radius + other.radius) - dist;

				correction = min(overlap, max_overlap_correction);

				obj.curr -= normal * (correction * (other.radius / (obj.radius + other.radius)));
				other.curr += normal * (correction * (obj.radius / (obj.radius + other.radius)));

				obj_vel = obj.curr - obj.prev;
				other_vel = other.curr - other.prev;
				rel_vel = other_vel - obj_vel;

				velocity_along_normal = rel_vel.dot(normal);

				if velocity_along_normal > 0:
					return;

				if obj_vel.length() < velocity_threshold and other_vel.length() < velocity_threshold:
					collision_response_factor = slow_collision_factor;
				else:
					collision_response_factor = 1.0;

				obj_mass = obj.radius;
				other_mass = other.radius;

				new_obj_vel = (obj_vel - normal * (collision_response_factor * (1 + particle_restitution)
												  * (other_mass / (obj_mass + other_mass)) * velocity_along_normal))*damp_fac;

				new_other_vel = (other_vel - normal * (collision_response_factor * (1 + particle_restitution)
													  * (obj_mass / (obj_mass + other_mass)) * velocity_along_normal))*damp_fac;

				obj.prev = obj.curr - new_obj_vel;
				other.prev = other.curr - new_other_vel;

	def keep_inbounds(self):
		ground_res = 0.5;

		for obj in self.objs:
			if(obj.curr.y<500):
				vel = obj.curr-obj.prev;

				if obj.curr.y+obj.radius>self.h:
					obj.curr.y = self.h-obj.radius;
					obj.prev.y = obj.curr.y+vel.y*ground_res;

				if obj.curr.x-obj.radius<0:
					obj.curr.x = obj.radius;
					obj.prev.x = obj.curr.x+vel.x*ground_res;

				if obj.curr.x+obj.radius>self.w:
					obj.curr.x = self.w-obj.radius;
					obj.prev.x = obj.curr.x+vel.x*ground_res;

				if obj.curr.y-obj.radius<0:
					obj.curr.y = obj.radius;
					obj.prev.y = obj.curr.y+vel.y*ground_res;

				if(obj.curr.x-obj.radius>10 and obj.curr.x-obj.radius<450):
					if obj.curr.y-obj.radius<17:
						obj.curr.y = 17+obj.radius;
						obj.prev.y = obj.curr.y+vel.y*ground_res;

					if obj.curr.y+obj.radius>430:
						obj.curr.y = 430-obj.radius;
						obj.prev.y = obj.curr.y+vel.y*ground_res;


				if(obj.curr.x-obj.radius>497 and obj.curr.x-obj.radius<908):
					if obj.curr.y-obj.radius<17:
						obj.curr.y = 17+obj.radius;
						obj.prev.y = obj.curr.y+vel.y*ground_res;

					if obj.curr.y+obj.radius>430:
						obj.curr.y = 430-obj.radius;
						obj.prev.y = obj.curr.y+vel.y*ground_res;


				if(obj.curr.y-obj.radius>40 and obj.curr.y-obj.radius<408):
					if obj.curr.x-obj.radius<10:
						obj.curr.x = 10+obj.radius;
						obj.prev.x = obj.curr.x+vel.x*ground_res;

					if obj.curr.x+obj.radius>932:
						obj.curr.x = 932-obj.radius;
						obj.prev.x = obj.curr.x+vel.x*ground_res;


	def fall(self, obj):
		if(obj.out==True):
			return
		out=False
		if((obj.curr.x-obj.radius>895 or obj.curr.x-obj.radius<25) and (obj.curr.y-obj.radius<33 or obj.curr.y-obj.radius>395) or obj.curr.y-obj.radius<17 or obj.curr.y-obj.radius>408):
			out=True

		if (out):
			if(obj.id!=self.ball and (not(self.free)) or obj.id==8):
				obj.prev.y = obj.orpos[1];
				obj.curr.y = obj.orpos[1];
				obj.prev.x = obj.orpos[0];
				obj.curr.x = obj.orpos[0];
				if(self.turn==1):
					if(self.score1>0):
						self.score1-=1;
				else:
					if(self.score2>0):
						self.score2-=1;	
				self.done = True;	
				self.free = False;
				self.any = False;			
			
			else:
				self.free = True
				self.any = True
				if(self.turn==1):
					self.score1+=obj.id;
				else:
					self.score2+=obj.id;
				obj.curr.y = 600;
				obj.prev.y = 600;
				obj.curr.x = 50+(obj.id-1)*30
				obj.prev.x = 50+(obj.id-1)*30
				obj.out=True
				if(obj.id==self.ball):
					self.ball+=1
					id_temp=obj.id;
					while(self.objs[id_temp].out==True):
						id_temp=id_temp+1
						self.ball+=1
					self.ballcolor=self.objs[id_temp].color
