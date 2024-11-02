CC=g++
CCFLAGS=-g -std=c++11 -Wall -Wno-narrowing -I/usr/include/SDL2/
LDFLAGS=-lSDL2 -lSDL2_gfx

BIN=sim
SRC=$(shell find . -name "*.cc")
OBJ=$(SRC:.cc=.o)

all: $(BIN)

%.o: %.cc
	$(CC) $(CCFLAGS) -c -o $@ $<

$(BIN): $(OBJ)
	$(CC) -o $@ $^ $(LDFLAGS)

clean:
	rm -rf $(OBJ) $(BIN)
