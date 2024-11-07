#!/bin/env python3
from psim.window import Window
import sys

W = 800;
H = 600;
DEFAULT_N  = 5;
DEFAULT_MR = 50;

USAGE_MSG = f"""usage: {sys.argv[0]} [n] [max_radius]
n - number of particles
max_radius - max radius of particle
-----------------------------------
press 'p' to pause the simulation
left click to add a particle""";

if __name__ == "__main__":
	n_par = int(sys.argv[1]) if len(sys.argv)>1 else DEFAULT_N;
	max_radius = int(sys.argv[2]) if len(sys.argv)>2 else DEFAULT_MR;

	win = Window("Particle Sandbox", W, H, n_par, max_radius);

	if len(sys.argv)>1:
		if sys.argv[1]=="-h":
			print(USAGE_MSG);
			exit();
	
	win.bgcolor = (0x0, 0x28, 0x3c);
	win.loop();
