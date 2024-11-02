#include <cstdio>
#include <cmath>
#include <unistd.h>
#include "vec.hh"
#include "verlet.hh"

#define GRAVITY   0.3f

Verlet::Verlet(unsigned w, unsigned h)
{
	this->w = w;
	this->h = h;
}

void
Verlet::set_bounds(unsigned w, unsigned h)
{
	this->w = w;
	this->h = h;
}

/* create n random objects */
void
Verlet::create_objs(unsigned n)
{
	for (unsigned i=0; i<n; i++) {
		VerletObject vo;
		float start_y = (rand()%h)+10;

		vo.id = i;
		vo.prev.set(max_radius*1.5*(i+1)-((rand()%15)), start_y);
		vo.curr.set(max_radius*1.5*(i+1), start_y);
		
		vo.acc.set(0.f, 0.f);
		vo.radius = (rand()%max_radius)+2;

		vo.color = {rand()%0xff, rand()%0xff, rand()%0xff, 0xff};

		objs.push_back(vo);
	}
}

void
Verlet::create_obj_at(unsigned x, unsigned y)
{
	VerletObject vo;

	vo.id = objs.size()+1;
	
	vo.prev.set(x, y);
	vo.curr.set(x, y);

	vo.acc.set(0.f, 0.f);
	vo.radius = (rand()%max_radius)+2;

	vo.color = {rand()%0xff, rand()%0xff, rand()%0xff, 0xff};

	objs.push_back(vo);
}

void
Verlet::set_max_radius(unsigned max_radius)
{
	this->max_radius = max_radius;
}

void
Verlet::apply_forces()
{
	for (auto &obj : objs) obj.acc.y = GRAVITY;
}

void
Verlet::update()
{
	apply_forces();

	for (auto &obj : objs) {
		Vec2 velocity;

		check_collisions(obj);

		velocity = obj.curr.sub(obj.prev).sum(obj.acc);

		obj.prev.x = obj.curr.x;
		obj.prev.y = obj.curr.y;

		obj.curr = obj.curr.sum(velocity);
	}
	
	keep_inbounds();
}

void
Verlet::check_collisions(VerletObject obj)
{
	float dist;
    const float particle_restitution = 0.9f;
    const float max_overlap_correction = 0.7f;
    const float velocity_threshold = 0.3f;
    const float slow_collision_factor = 0.9f;
    Vec2 normal;

    for (size_t i = 0; i < objs.size(); ++i) {
        auto &other = objs[i];

        if (other.id == obj.id) continue;

        Vec2 delta = other.curr.sub(obj.curr);
        dist = delta.norm();

        if (dist < obj.radius + other.radius) {
            float overlap, correction, velocity_along_normal;
			float collision_response_factor, obj_mass, other_mass;
			Vec2 obj_vel, other_vel, rel_vel;

			normal = delta.mul(1.0f / dist);
            overlap = (obj.radius + other.radius) - dist;

            correction = fmin(overlap, max_overlap_correction);
            
			obj.curr = obj.curr.sub(normal.mul(correction*
			                        (other.radius/(obj.radius+
								    other.radius))));

            other.curr = other.curr.sum(normal.mul(correction*
			                            (obj.radius/(obj.radius+
										other.radius))));

            obj_vel = obj.curr.sub(obj.prev);
            other_vel = other.curr.sub(other.prev);
			rel_vel = other_vel.sub(obj_vel);
            
			velocity_along_normal = rel_vel.dot(normal);

            if (velocity_along_normal > 0) return;

			if (obj_vel.norm()<velocity_threshold&&other_vel.norm()<
			    velocity_threshold)
				collision_response_factor = slow_collision_factor;
			else
				collision_response_factor = 1.0f;

            obj_mass = obj.radius; 
            other_mass = other.radius;
            
			Vec2 new_obj_vel = obj_vel.sub(normal.mul(collision_response_factor*
			                   (1 + particle_restitution)*(other_mass/(obj_mass+other_mass))
							   * velocity_along_normal));

            Vec2 new_other_vel = other_vel.sub(normal.mul(collision_response_factor*
			                     (1 + particle_restitution) * (obj_mass/(obj_mass+other_mass))
								 * velocity_along_normal));

            obj.prev = obj.curr.sub(new_obj_vel);
            other.prev = other.curr.sub(new_other_vel);
        }
    }
}

void
Verlet::keep_inbounds()
{
	const float ground_restitution = 0.9f;

    for (auto &obj : objs) {
        Vec2 vel = obj.curr.sub(obj.prev);

        if (obj.curr.y + obj.radius > h) {
            obj.curr.y = h - obj.radius;
            obj.prev.y = obj.curr.y + vel.y * ground_restitution;
        }

        if (obj.curr.x - obj.radius < 0) {
            obj.curr.x = obj.radius;
            obj.prev.x = obj.curr.x + vel.x;
        }

        if (obj.curr.x + obj.radius > w) {
            obj.curr.x = w - obj.radius;
            obj.prev.x = obj.curr.x + vel.x;
        }

        if (obj.curr.y - obj.radius < 0) {
            obj.curr.y = obj.radius;
            obj.prev.y = obj.curr.y + vel.y;
        }
    }
}
