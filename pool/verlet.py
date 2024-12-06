# Método de Verlet
from pygame.math import Vector2 as Vec2
import math
from random import randint as randi

# Constante de atrito
ATRITO = 0.02;

# Objeto de simulação
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
	
	# Configura limites de simulação (paredes)
	def set_bounds(self, w0, w1, h0, h1):
		self.w0 = w0;
		self.w1 = w1;
		self.h0 = h0;
		self.h1 = h1;
	
	# Aplica as forças num objeto (atrito)
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

	# Atualiza os atributos do objeto pelo método de Verlet
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
	
	# Calcula colisões
	def check_collisions(self, obj):
		# Constantes
		particle_restitution = -0.98;
		max_overlap_correction = 1000;
		velocity_threshold = 0.2;
		slow_collision_factor = 0.7;
		damp_fac = 0.97;

		# Checa as outras bolas e procura contato/overlapping
		for other in self.objs:
			if other.id == obj.id:
				continue;
	
			# Calculando a direção ideal da bola acertada pela branca após colisao: a diferenca entre a posicao entre as duas bolas
			delta = other.curr - obj.curr;
			dist = delta.length();

			if dist <= obj.radius + other.radius:
				if dist > 0:
					normal = delta/dist;
				else:
					normal = delta*0;

				# As bolas estao ocupando o mesmo espaco devido a erros do Verlet e pelo fato do nosso tick nao ser "infinitesimal"
				# Vamos tentar compensar isso movendo ambas as bolas na direcao que calculamos a cima para eliminar a sobreposicao
				# Isso introduz um problema: as bolas ganharam uma velocidade devido a forma como o Verlet funciona
				overlap = (obj.radius + other.radius) - dist;
				correction = min(overlap, max_overlap_correction);

				obj.curr -= normal * (correction * (other.radius / (obj.radius + other.radius)));
				other.curr += normal * (correction * (obj.radius / (obj.radius + other.radius)));

				# Calculamos as velocidades e checamos se elas estão se afastando
				obj_vel = obj.curr - obj.prev;
				other_vel = other.curr - other.prev;
				rel_vel = other_vel - obj_vel;

				velocity_along_normal = rel_vel.dot(normal);

				if velocity_along_normal > 0:
					return;

				# Caso algo de errado, tentamos compensar utilizando os fatores
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

	# Mantém os objetos dentro dos limites da tela
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
