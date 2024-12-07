# Janela Principal
from pool.renderer import Renderer # Renderização
from pool.verlet   import Verlet # Fisíca implementada
from pool.game	   import Game # Mecânica do jogo
import pygame as pg

# Classe "botão" do menu
class Button:
	def __init__(self, idx, msg, color, color_hover, pos, dim):
	# Parâmetros:	idx (int): índice do botão na lista
	#		msg (string): mensagem exibida
	#		color (tupla): Cor do botão (R, G, B)
	#		color_hover (tupla): Cor do botão quando o mouse está sobre ele (R, G, B)
	#		pos (tupla): Posição do botão (x,y)
	#		dim (tupla): Dimensões do botão (largura, altura)
		self.idx = idx;
		self.msg = msg;
		self.color = color;
		self.color_hover = color_hover;
		self.hover = False; # Indica se o mouse está em cima do botão
		self.pos = pos;
		self.dim = dim;

	# Verifica se o mouse está em cima do botão
	def check_hover(self, w, h):
	# Parâmetros: 	w (string): largura da janela
	#		h (float): altura da janela
	
		mouse_x = pg.mouse.get_pos()[0]; # Coordenada X do mouse
		mouse_y = pg.mouse.get_pos()[1]; # Coordenada Y do mouse

		# Atualiza o estado de hover conforme as coordenadas
		self.hover = mouse_x > self.pos[0] and \
					 mouse_x < self.pos[0]+self.dim[0] and \
					 mouse_y > self.pos[1] and \
					 mouse_y < self.pos[1]+self.dim[1];
		
# Janela principal do projeto
class Window:
	def __init__(self, title, w, h):
	# Parâmetros: 	title (string): título da janela
	#		w (float): largura da janela
	#		h (float): altura da janela
		self.title = title;
		self.w = w;
		self.h = h;
		self.clk = pg.time.Clock(); # Relógio para controlar os FPS

		# Janela do Pygame (inicialização)
		pg.display.init();
		surface = pg.display.set_mode(size=(w, h), vsync=1);
		pg.display.set_caption(self.title);
		pg.font.init();

		self.fonts = [
			pg.font.SysFont(None, 30, bold=True) # Definição da fonte
		];

		# Posições padrão dos botões
		def_btn_x = (self.w/2)-200;
		def_btn_y = (self.h)/7; 

		# Definições dos botões
		self.buttons = [
			Button(0, "Jogar", (127, 200, 127), (200, 255, 200),
				(def_btn_x, def_btn_y), (400, self.h/7)),
			Button(1, "Gráficos", (200, 127, 127), (255, 200, 200),
				(def_btn_x, 3*def_btn_y), (400, self.h/7)),
			Button(2, "Sair",  (127, 127, 200), (200, 200, 255),
				(def_btn_x, 5*def_btn_y), (400, self.h/7))
		];
		
		self.btn_pos = [(self.w)/2-200, self.h/7]; # Posição base dos botões
		self.btn_dim = [400, self.h/7]; # Dimensão dos botões

		# Inicialização dos outros componentes do projeto
		self.ren = Renderer(surface); # Renderizador
		self.vl = Verlet(w, h); # Física implementada
		self.game = Game(w, h, self.ren, self.vl); # Mecânica do jogo

	# Desenha os botões do menu na tela
	def draw_buttons(self):
		for btn in self.buttons:
			# Muda a cor do botão ao passar o mouse sobre
			color = btn.color_hover if btn.hover else btn.color;

			# Renderiza o retângulo do botão
			self.ren.render_rect(self.btn_pos[0],
								 (1+2*btn.idx)*self.btn_pos[1],
								 self.btn_dim[0], self.btn_dim[1],
								 color);
			# Renderiza o texto do botão
			self.ren.render_text(btn.msg, self.fonts[0],
								 (0, 0, 0), (self.w/2,
								 (3+4*btn.idx)*(self.h/14)), "center",
								 "middle");
	
	# Loop principal da janela
	def loop(self):
		brk = False; # Flag para sair do loop
		pause = True; # Indica se o jogo está pausado
		surf = self.ren.surf; # Superfície de renderização
		menu_click = False; # Indica se houve clique no menu

		while not brk:
			# Configuração da força do taco
			if pg.key.get_pressed()[pg.K_w]:
				self.game.increase_force(); # Aumento (W)
			if pg.key.get_pressed()[pg.K_s]:
				self.game.decrease_force(); # Redução (S)

			# Lidando com as entradas via teclado e mouse
			for e in pg.event.get():
				if e.type == pg.MOUSEBUTTONDOWN:
					if pause: # Se o jogo estiver pausado
						menu_click = True;

						if self.buttons[1].hover: # "GRÁFICOS"
							self.game.plot(); 
							continue;
						if self.buttons[2].hover: # "SAIR"
							brk = True;
							continue;
					else:
						menu_click = False;
						self.game.aiming = True; # Começa a mirar com o taco

				if e.type == pg.MOUSEBUTTONUP: # Soltar o clique do mouse
					if not pause and not menu_click:
						menu_click = not menu_click;
						self.game.shoot_ball(self.game.cue_force, pg.math.Vector2.normalize(e.pos - self.vl.objs[0].curr)) # Dispara a bola branca
						self.game.aiming = False; # Para de mirar com o taco

					if pause and menu_click:
						menu_click = not menu_click;
						if self.buttons[0].hover: # Opção "JOGAR"
							if pause:
								pg.display.set_caption(self.title);

							pause = not pause; # Jogo é iniciado
							continue;

				if e.type == pg.QUIT: # Fechamento da janela
					brk = True;
				if e.type == pg.KEYDOWN: # Tecla pressionada
					key = pg.key.name(e.key);
					if key=='q': # Saída do jogo
						brk = True;
					if key=='p': # Pausa / continua o jogo
						if pause:
							pg.display.set_caption(self.title);

						pause = not pause;
						
			surf.fill(self.bgcolor); # Limpa a tela

			if pause:
				# Menu
				pg.display.set_caption("Menu");

				for btn in self.buttons:
					# Verifica o estado de hover
					btn.check_hover(self.w, self.h); 

				self.draw_buttons(); # Exibe os botões
			else:
				# Jogo
				self.clk.tick(60); # FPS
				self.game.tick(); # Atualização do estado do jogo
				if self.game.end: # Reinicialização
					self.vl = Verlet(self.w, self.h);
					self.game = Game(self.w, self.h, self.ren, self.vl);
					pause = True;

			# Atualiza tela
			pg.display.flip();
