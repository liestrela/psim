#include <cmath>
#include "vec.hh"

Vec2::Vec2()
{
	this->set(0, 0);
}

Vec2::Vec2(float x, float y)
{
	this->set(x, y);
}

void
Vec2::set(float x, float y)
{
	this->x = x;
	this->y = y;
}

Vec2
Vec2::sum(Vec2 op)
{
	Vec2 res(this->x, this->y);
	
	res.x += op.x;
	res.y += op.y;

	return res;
}

Vec2
Vec2::mul(float a)
{
	Vec2 res(this->x, this->y);

	res.x*=a;
	res.y*=a;

	return res;
}

Vec2
Vec2::sub(Vec2 op)
{
	Vec2 res = this->sum(op.mul(-1));
	return res;
}

Vec2
Vec2::normalize()
{
	return this->mul(1/(this->norm()));
}

float
Vec2::norm()
{
	return sqrt(x*x+y*y);
}

float
Vec2::dot(Vec2 op)
{
	return vec2_dot(*this, op);
}

float
Vec2::dist(Vec2 op)
{
	return this->sub(op).norm();
}

float
vec2_dot(Vec2 a, Vec2 b)
{
	return a.x*b.x+a.y*b.y;
}
