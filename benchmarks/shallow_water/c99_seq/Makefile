CC = gcc
FLAGS = -O2 -lm -std=gnu99
BOOST = /opt/local/include/

all: swater-index-calc


clean:
	rm -f swater-index-calc *~

swater-index-calc: swater-index-calc.c
	$(CC) swater-index-calc.c -o swater-index-calc $(FLAGS)
