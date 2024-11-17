from pygame.math import Vector2 as Vec2
from random import randint as randi
import math
import pygame as pg

ATRITO = 0.01;


class VerletObject:
	def __init__(self):
		self.curr = Vec2(0,0);
		self.prev = Vec2(0,0);
		self.vel  = Vec2(0,0);
		self.acc  = Vec2(0,0);
		self.radius = 0;
		self.color = (0,0,0);
		self.id = 0;


class Verlet:
	def __init__(self, w, h):
		self.w = 950;
		self.h = 450;
		self.max_radius = 0;
		self.objs = [];
		self.holes = [];
		self.walls = [];
	
	def set_bounds(self, w, h):
		self.w = 950;
		self.h = 450;


	def create_holes(self):
		self.holes = [
	    (11, 11 , 22),
	    (939, 11, 22),
	    (11, 439, 22),
	    (939, 439, 22),
	    (475, 11, 22),
	    (475, 439, 22)]

	def create_walls(self):
		self.walls = [
		(33, 8 , 420,7 ),
		(497, 8, 421,7 ),
		(0, 32, 7,385 ),
		(943, 32, 7,385 ),
		(33, 435, 420, 7),
		(497, 435, 421,7)]	
		
	
	def create_objs(self):
	
		vo = VerletObject();
		vo.id = 1;
		vo.prev.update((150, 125));
		vo.curr.update((150, 125));
		vo.acc.update(0, 0);
		vo.radius = 15;
		vo.color = (200,0,0);

		self.objs.append(vo);


		vo = VerletObject();
		vo.id = 2;
		vo.prev.update((750, 295));
		vo.curr.update((750, 295));
		vo.acc.update(0, 0);
		vo.radius = 15;
		vo.color = (200,200,0);
		self.objs.append(vo);


		vo = VerletObject();
		vo.id = 3;
		vo.prev.update((750, 155));
		vo.curr.update((750, 155));
		vo.acc.update(0, 0);
		vo.radius = 15;
		vo.color = (0,200,0);
		self.objs.append(vo);


		vo = VerletObject();
		vo.id = 4;
		vo.prev.update((750, 225));
		vo.curr.update((750, 225));
		vo.acc.update(0, 0);
		vo.radius = 15;
		vo.color = (200, 100, 0);
		self.objs.append(vo);


		vo = VerletObject();
		vo.id = 5;
		vo.prev.update((475, 225));
		vo.curr.update((475, 225));
		vo.acc.update(0, 0);
		vo.radius = 15;
		vo.color = (0,0,200);
		self.objs.append(vo);


		vo = VerletObject();
		vo.id = 6;
		vo.prev.update((150, 225));
		vo.curr.update((150, 225));
		vo.acc.update(0, 0);
		vo.radius = 15;
		vo.color = (200,100,100);
		self.objs.append(vo);


		vo = VerletObject();
		vo.id = 7;
		vo.prev.update((20, 225));
		vo.curr.update((20, 225));
		vo.acc.update(0, 0);
		vo.radius = 15;
		vo.color = (25,25,25);
		self.objs.append(vo);
		
	def create_obj_at(self, pos):
		vo = VerletObject();

		vo.id = len(self.objs)+1;
		
		vo.prev.update(pos);
		vo.curr.update(pos);

		vo.acc.update(0, 0);
		vo.radius = 15;

		vo.color = (220, 220, 220);

		self.objs.append(vo);

	def hit_obj(self, pos, force):
		all_stopped=True;
		for obj in self.objs:
			if(abs(obj.curr.x-obj.prev.x)>0.001 or abs(obj.curr.y-obj.prev.y)>0.001 ):
				all_stopped=False;
				break;
		if(all_stopped):

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

		if(abs(vy) > 0.001):
			obj.acc[1] = -((obj.vel[1])/abs(vy))*ATRITO*math.sin(theta_radians);
		else:
			obj.acc[1] = 0
		if(abs(vx) > 0.001):
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

			

			if(abs(vx)<0.1):
				vx = 0
			else:
				vx += ax
			if(abs(vy)<0.1):
				vy=0
			else:
				vy += ay


			velocity = (vx,vy)

			obj.prev.x = obj.curr.x;
			obj.prev.y = obj.curr.y;

			obj.curr += velocity;
			obj.vel = velocity;

		self.keep_inbounds();
	
	def check_collisions(self, obj):
		particle_restitution = -0.001;
		max_overlap_correction = 1000;
		velocity_threshold = 0.2;
		slow_collision_factor = 0.7;
		damp_fac = 0.97;

		for other in self.objs:
			if other.id == obj.id:
				continue;

			delta = other.curr - obj.curr;
			dist = delta.length();

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
		ground_res = 0.9;

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



				if(obj.curr.x-obj.radius>33 and obj.curr.x-obj.radius<453):
					if obj.curr.y-obj.radius<8:
						obj.curr.y = 8+obj.radius;
						obj.prev.y = obj.curr.y+vel.y*ground_res;

					if obj.curr.y+obj.radius>435:
						obj.curr.y = 435-obj.radius;
						obj.prev.y = obj.curr.y+vel.y*ground_res;


				if(obj.curr.x-obj.radius>497 and obj.curr.x-obj.radius<918):
					if obj.curr.y-obj.radius<8:
						obj.curr.y = 8+obj.radius;
						obj.prev.y = obj.curr.y+vel.y*ground_res;

					if obj.curr.y+obj.radius>435:
						obj.curr.y = 435-obj.radius;
						obj.prev.y = obj.curr.y+vel.y*ground_res;


				if(obj.curr.y-obj.radius>32 and obj.curr.y-obj.radius<417):
					if obj.curr.x-obj.radius<7:
						obj.curr.x = 7+obj.radius;
						obj.prev.x = obj.curr.x+vel.x*ground_res;

					if obj.curr.x+obj.radius>943:
						obj.curr.x = 943-obj.radius;
						obj.prev.x = obj.curr.x+vel.x*ground_res;


	def fall(self, obj):
		out=False
		if(obj.curr.x-obj.radius>453 and obj.curr.x-obj.radius<497):
			if obj.curr.y-obj.radius<4:
				out=True

			if obj.curr.y+obj.radius>431:
				out=True


		if(obj.curr.y-obj.radius<8 or obj.curr.y-obj.radius>417):
			if obj.curr.x-obj.radius<3:
				out=True

			if obj.curr.x+obj.radius>947:
				out=True

		if(obj.curr.x-obj.radius<33 or obj.curr.x-obj.radius>918):
			if obj.curr.y-obj.radius<4:
				out=True

			if obj.curr.y+obj.radius>431:
				out=True

		if(out):
			if(obj.id==8):
				obj.curr.y = 225;
				obj.prev.y = 225
				obj.curr.x = 825;
				obj.prev.x = 825;
			else:
				obj.curr.y = 600;
				obj.prev.y = 600;
				obj.curr.x = 50+(obj.id-1)*30
				obj.prev.x = 50+(obj.id-1)*30








	


			


