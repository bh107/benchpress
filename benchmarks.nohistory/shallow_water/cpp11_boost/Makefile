CC = gcc
CPP = g++
FLAGS = -O2 -lm
BOOST = /opt/local/include/ 

all: swater-boost

bench: all
	./swater.sh

clean:
	rm -f swater-boost *~

swater-boost: swater-boost.cc
	$(CPP) -I$(BOOST) swater-boost.cc -o swater-boost $(FLAGS)
