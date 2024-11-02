#ifndef RENDERER_HH
#define RENDERER_HH

#include <vector>
#include <SDL.h>

class Renderer {
	public:
	Renderer(SDL_Window *win);
	~Renderer();

	void render_circle(int x, int y, int radius, SDL_Color color);

	SDL_Renderer *ren;
};

#endif
