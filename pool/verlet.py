from pygame.math import Vector2 as Vec2
import math
from random import randint as randi

GRAVITY = 0.3;
ATRITO = 0.02;

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
		self.w0 = 0;
		self.h0 = 0;
		self.w1 = w;
		self.h1 = h;
		self.max_radius = 0;
		self.objs = [];
	
	def set_bounds(self, w0, w1, h0, h1):
		self.w0 = w0;
		self.w1 = w1;
		self.h0 = h0;
		self.h1 = h1;
	
	# create n random objects
	def create_objs(self, n, radius):
		for i in range(0, n):
			vo = VerletObject();
			start_y = randi(10, self.h1-1);

			vo.id = i;
			vo.prev.update((self.max_radius*1.5*(i+1)-randi(0,14),
						   start_y));
			vo.curr.update((self.max_radius*1.5*(i+1), start_y,));

			vo.acc.update(0, 0);
			vo.radius = randi(2, radius);

			vo.color = (randi(0, 0xff), randi(0, 0xff),
						randi(0, 0xff));
			
			self.objs.append(vo);
	
	def create_obj_at(self, pos):
		vo = VerletObject();

		vo.id = len(self.objs)+1;
		
		vo.prev.update(pos);
		vo.curr.update(pos);

		vo.acc.update(0, 0);
		vo.radius = randi(2, self.max_radius-1);

		vo.color = (randi(0, 0xff), randi(0, 0xff), randi(0, 0xff));

		self.objs.append(vo);
	
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
			self.apply_forces(obj);

		for obj in self.objs:
			self.check_collisions(obj);

			velocity_prev = obj.vel = obj.curr-obj.prev
			velocity = (obj.curr-obj.prev)+obj.acc;
			obj.vel = velocity
			
			if (velocity_prev * velocity < 0):
				velocity = Vec2(0, 0);

			obj.prev.x = obj.curr.x;
			obj.prev.y = obj.curr.y;

			obj.curr += velocity;

		self.keep_inbounds();
	
	def check_collisions(self, obj):
		particle_restitution = -0.98;
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
			vel = obj.curr-obj.prev;

			if obj.curr.y+obj.radius>self.h1:
				obj.curr.y = self.h1-obj.radius;
				obj.prev.y = obj.curr.y+vel.y*ground_res;

			if obj.curr.x-obj.radius<self.w0:
				obj.curr.x = obj.radius;
				obj.prev.x = obj.curr.x+vel.x;

			if obj.curr.x+obj.radius>self.w1:
				obj.curr.x = self.w1-obj.radius;
				obj.prev.x = obj.curr.x+vel.x;

			if obj.curr.y-obj.radius<self.h0:
				obj.curr.y = self.h0+obj.radius;
				obj.prev.y = obj.curr.y+vel.y;
