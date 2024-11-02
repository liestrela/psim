#ifndef WINDOW_HH
#define WINDOW_HH

#include <string>
#include <SDL.h>
#include "renderer.hh"
#include "verlet.hh"

class Window {
	public:
	unsigned w, h;
	std::string title;

	Window(const char *title, unsigned w, unsigned h, unsigned n,
	       float max_radius);
	~Window();

	void set_bgcolor(unsigned r, unsigned g, unsigned b);

	void loop();

	private:
	SDL_Window *win;
	SDL_Color bgcolor;
	Renderer *ren;
	Verlet vl;
};

#endif
