/* verlet integration */
#ifndef VERLET_HH
#define VERLET_HH

#include <vector>
#include <SDL.h>
#include "vec.hh"

class VerletObject {
	public:
	Vec2 curr, prev, vel, acc;
	float radius;
	SDL_Color color;
	unsigned id;
};

class Verlet {
	public:
	Verlet() = default;
	Verlet(unsigned w, unsigned h);
	
	void set_bounds(unsigned w, unsigned h);
	void create_objs(unsigned n);
	void create_obj_at(unsigned x, unsigned y);
	void apply_forces();
	void check_collisions(VerletObject obj);
	void set_max_radius(unsigned max_radius);
	void update();

	std::vector<VerletObject> objs;
	unsigned w, h;

	private:
	void keep_inbounds();

	unsigned max_radius;
};

#endif
