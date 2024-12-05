#!/bin/env python3
from pool.window import Window
import sys

# Default window resolution
W = 1300;
H = 600;
bg_color = (35, 125, 15);

if __name__ == "__main__":
	win = Window("Sinuca", W, H);

	win.bgcolor = bg_color;
	win.loop();
