#include <cstdlib>
#include <string>
#include <ctime>
#include <SDL.h>

#include "window.hh"
#include "renderer.hh"
#include "verlet.hh"

#define WIN_CENTER SDL_WINDOWPOS_CENTERED
#define WIN_FLAGS SDL_WINDOW_OPENGL|SDL_WINDOW_RESIZABLE

Window::Window(const char *title, unsigned w, unsigned h, unsigned n,
               float max_radius)
{
	srand(time(0));

	win = SDL_CreateWindow(title, WIN_CENTER, WIN_CENTER,
	                       w, h, WIN_FLAGS);

	this->title = std::string(title);
	this->w = w;
	this->h = h;
	
	set_bgcolor(0, 0, 0);

	ren = new Renderer(win);

	SDL_SetHint(SDL_HINT_RENDER_SCALE_QUALITY, "1");

	vl.set_bounds(w, h);
	vl.set_max_radius(max_radius);
	vl.create_objs(n);
	vl.apply_forces();
}

Window::~Window()
{
	delete ren;
	SDL_DestroyWindow(win);
}

void
Window::set_bgcolor(unsigned r, unsigned g, unsigned b)
{
	this->bgcolor = {r, g, b, 0xff};
}

void
Window::loop()
{
	bool brk = false, pause = false;
	SDL_Event e;

	while (!brk) {
		while (SDL_PollEvent(&e)) {
			switch (e.type) {
				case SDL_QUIT:
				brk = true;
				break;

				case SDL_KEYDOWN:
				if (e.key.keysym.sym==SDLK_q) {
					brk = true;
					break;
				}

				if (e.key.keysym.sym==SDLK_p) {
					if (!pause)
						SDL_SetWindowTitle(win, (title+" (paused)")
						                   .c_str());
					else SDL_SetWindowTitle(win, title.c_str());
				
					pause = !pause;
					break;
				}
				break;

				case SDL_MOUSEBUTTONDOWN:
				switch(e.button.button) {
					case SDL_BUTTON_LEFT:
					vl.create_obj_at(e.button.x, e.button.y);
					break;
				}
				break;
			}
		}

		SDL_SetRenderDrawColor(ren->ren, bgcolor.r, bgcolor.g,
		                       bgcolor.b, 0xff);
		SDL_RenderClear(ren->ren);

		for (auto &vo : vl.objs)
			ren->render_circle(vo.curr.x, vo.curr.y, vo.radius,
			                   vo.color);

		if (!pause) vl.update();

		SDL_RenderPresent(ren->ren);
	}
}
