#include <SDL2_gfxPrimitives.h>
#include "renderer.hh"

#define RENDER_FLAGS SDL_RENDERER_ACCELERATED|\
                     SDL_RENDERER_PRESENTVSYNC

Renderer::Renderer(SDL_Window *win)
{
	ren = SDL_CreateRenderer(win, -1, RENDER_FLAGS);		
}

Renderer::~Renderer()
{
	SDL_DestroyRenderer(ren);
}

void
Renderer::render_circle(int x, int y, int radius, SDL_Color color)
{
	aacircleRGBA(ren, x, y, radius, color.r, color.g, color.b, 0xff);
	filledCircleRGBA(ren, x, y, radius, color.r, color.g, color.b, 0xff);
}
