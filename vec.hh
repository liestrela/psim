#ifndef VEC_HH
#define VEC_HH

class Vec2 {
	public:
	Vec2();
	Vec2(float x, float y);

	void set(float x, float y);
	Vec2 sum(Vec2 op);
	Vec2 mul(float a);
	Vec2 sub(Vec2 op);
	Vec2 normalize();

	float norm();
	float dot(Vec2 op);
	float dist(Vec2 op);

	float x, y;
};

float vec2_dot(Vec2 a, Vec2 b);

#endif
