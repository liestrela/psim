# Método de Verlet
from pygame.math import Vector2 as Vec2
import math
from random import randint as randi

# Constante de atrito
ATRITO = 0.02;

# Objeto de simulação
class VerletObject:
	def __init__(self):
		self.curr = Vec2(0,0); # Posição atual
		self.prev = Vec2(0,0); # Posição anterior
		self.vel  = Vec2(0,0); # Velocidade
		self.acc  = Vec2(0,0); # Aceleração
		self.radius = 0; # Raio
		self.color = (0,0,0); # Cor
		self.id = 0; # Identificador

# Funcionamento da simulação
class Verlet:
	def __init__(self, w, h):
		# Parâmetros: 	w (float): largura
		#		h (float): altura
		
		# Paredes da simulação
		self.w0 = 0; # limite esquerdo
		self.h0 = 0; # limite superior
		self.w1 = w; # limite direito
		self.h1 = h; # limite inferior
		# Raio máximo para os objetos (não utilizado na sinuca)
		self.max_radius = 0;
		# Lista dos objetos
		self.objs = [];
	
	# Configura limites de simulação (paredes)
	def set_bounds(self, w0, w1, h0, h1):
		# Parâmetros: 	w0 (float): limite esquerdo
		#		w1 (float): limite direito
		#		h0 (float): limite superior
		#		h1 (float): limite inferior
		self.w0 = w0;
		self.w1 = w1;
		self.h0 = h0;
		self.h1 = h1;
	
	# Aplica as forças num objeto (atrito)
	def apply_forces(self, obj):
	# Parâmetro: objeto Verlet

		# Cálculo da velocidade em cada eixo
		vy=obj.curr[1]-obj.prev[1]
		vx=obj.curr[0]-obj.prev[0]

		# Cálculo do ângulo da velocidade em relação ao eixo X
		theta_radians = math.atan2(abs(vy), abs(vx))

		# Cálculo da aceleração em Y
		if(abs(vy) > 0):
			obj.acc[1] = -((obj.vel[1])/abs(vy))*ATRITO*math.sin(theta_radians);
		else:
			obj.acc[1] = 0
			
		# Cálculo da aceleração em X
		if(abs(vx) > 0):
			obj.acc[0] = -((obj.vel[0])/abs(vx))*ATRITO*math.cos(theta_radians);
		else:
			obj.acc[0] = 0

	# Atualiza os atributos do objeto pelo método de Verlet
	def update(self):
		# Aplica a força de atrito a cada um dos objetos
		for obj in self.objs:
			self.apply_forces(obj);

		# Verificação de colisões e atualização da posição dos objetos
		for obj in self.objs:
			self.check_collisions(obj);

			# Cálculo da velocidade anterior
			velocity_prev = obj.vel = obj.curr-obj.prev
			# Cálculo da nova velocidade
			velocity = (obj.curr-obj.prev)+obj.acc;
			obj.vel = velocity

			 # Se o sinal da velocidade mudou, zera seu valor (garantir que os objetos parem, e não fiquem vibrando)
			if (velocity_prev * velocity < 0):
				velocity = Vec2(0, 0);
			# Atualização da posição anterior para a posição atual
			obj.prev.x = obj.curr.x;
			obj.prev.y = obj.curr.y;

			# Atualização da posição atual conforme a velocidade
			obj.curr += velocity;

		# Mantém os objetos dentro dos limites definidos
		self.keep_inbounds();
	
	# Calcula colisões
	def check_collisions(self, obj):
	# Parâmetro: objeto Verlet
		# Constantes
		particle_restitution = -0.98; # Fator de restituição (elasticidade)
		max_overlap_correction = 1000; # Correção máxima para sobreposição
		velocity_threshold = 0.2; # Limite para considerar colisões lenta
		slow_collision_factor = 0.7; # Fator de colisão lenta
		damp_fac = 0.97; # Fator de amortecimento pós-colisão

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

				# Velocidade ao longo da direção da colisão
				velocity_along_normal = rel_vel.dot(normal);

				# Se as velocidades estão se afastando, não há colisão
				if velocity_along_normal > 0:
					return;

				# Caso algo de errado, tentamos compensar utilizando os fatores
				if obj_vel.length() < velocity_threshold and other_vel.length() < velocity_threshold:
					collision_response_factor = slow_collision_factor;
				else:
					collision_response_factor = 1.0;

				# Massas baseadas nos raios dos objetos
				obj_mass = obj.radius;
				other_mass = other.radius;

				# Cálculo das novas velocidades após a colisão
				new_obj_vel = (obj_vel - normal * (collision_response_factor * (1 + particle_restitution)
												  * (other_mass / (obj_mass + other_mass)) * velocity_along_normal))*damp_fac;

				new_other_vel = (other_vel - normal * (collision_response_factor * (1 + particle_restitution)
													  * (obj_mass / (obj_mass + other_mass)) * velocity_along_normal))*damp_fac;
				# Atualização das posições anteriores, conforme as novas velocidades
				obj.prev = obj.curr - new_obj_vel;
				other.prev = other.curr - new_other_vel;

	# Mantém os objetos dentro dos limites da tela
	def keep_inbounds(self):
		ground_res = 0.9; # Restituição da colisão com os limites da mesa

		for obj in self.objs:
			vel = obj.curr-obj.prev; # Cálculo da velocidade atual

			# Colisão com a parte inferior
			if obj.curr.y+obj.radius>self.h1:
				obj.curr.y = self.h1-obj.radius;
				obj.prev.y = obj.curr.y+vel.y*ground_res;

			# Colisão com a parte esquerda
			if obj.curr.x-obj.radius<self.w0:
				obj.curr.x = obj.radius;
				obj.prev.x = obj.curr.x+vel.x;

			 # Colisão com a parte direita
			if obj.curr.x+obj.radius>self.w1:
				obj.curr.x = self.w1-obj.radius;
				obj.prev.x = obj.curr.x+vel.x;

			# Colisão com a parte superior
			if obj.curr.y-obj.radius<self.h0:
				obj.curr.y = self.h0+obj.radius;
				obj.prev.y = obj.curr.y+vel.y;
