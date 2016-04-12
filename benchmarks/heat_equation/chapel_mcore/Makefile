# Makefile that builds each src/*.chpl file into a binary in bin/*

CC=chpl
CFLAGS=-g
LDFLAGS=

SRC=$(wildcard src/*.chpl)
PROGRAM=$(addprefix bin/, $(subst .chpl,, $(subst src/,,$(SRC))))

all: mkdir $(PROGRAM)

bin/% : src/%.chpl
	$(CC) $(CFLAGS) -o $@ $<

.PHONY: clean mkdir

mkdir:
	mkdir -p bin
clean:
	rm -R bin
