#include <cstdlib>
#include "window.hh"

#define DEFAULT_N 5
#define DEFAULT_MR 50
#define W 800
#define H 600

#define USAGE_MSG \
	"usage: %s [n] [max_radius]\n"\
	"n - number of particles;\n"\
	"max_radius - max radius of particle\n"\
	"-----------------------------------\n"\
	"press \'p\' to pause the simulation\n"\
	"left click to add a particle\n"

int
main(int argc, char **argv)
{
 	unsigned n_par = (argc>1)?atoi(argv[1]):DEFAULT_N;
	unsigned max_radius = (argc>2)?atoi(argv[2]):DEFAULT_MR;
	Window win("Particle Sandbox", W, H, n_par, max_radius);

	if (argc>1&&(argv[1][0]=='-'&&argv[1][1]=='h')) {
		printf(USAGE_MSG, argv[0]);
		return EXIT_SUCCESS;
	}

	win.set_bgcolor(0, 0x28, 0x3c);

	win.loop();

	return EXIT_SUCCESS;
}
