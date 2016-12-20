#!/usr/bin/env python
import numpy as np
import pprint
import glob
import os

def cells_from_file(path):

    def p2i(p):
        if p == ".":
            return 0
        elif p == "*":
            return 1
        elif p == "O":
            return 1

    patterns = []               # Grab patterns
    with open(path) as fd:
        height, width       = 1, 1
        y_offset, x_offset  = 0, 0
        pattern = None
        for line in fd.readlines():
            line = line.strip()
            if line.startswith("#P "):
                prefix, cy, cx = line.split(" ")
                if pattern:
                    patterns.append((pattern, y_offset, x_offset, height, width))
                pattern = []    # Reset pattern
                y_offset, x_offset = int(cy), int(cx)
                height, width = 1, 1
                continue
            elif line.startswith("#"):
                continue
            ptn = [p2i(l) for l in line]
            height += 1
            width = max(len(line), width)
            pattern.append(ptn)

        patterns.append((pattern, y_offset, x_offset, height, width))

    arrays = []                 # Convert to NumPy arrays
    for pattern, y_offset, x_offset, height, width in patterns:
        ary = np.zeros((height, width))
        for y, line in enumerate(pattern):
            for x, cell in enumerate(line):
                ary[y][x] = cell
        arrays.append((ary, y_offset, x_offset))

    return arrays

def pprint_world(world):

    world_h, world_w = world.shape
    for y in range(world_h):
        line = []
        for x in range(world_w):
            line.append("%d" % int(world[y][x]))
        print("".join(line))

def insert_cells(world, patterns):

    world_h, world_w    = world.shape
    offset_h, offset_w  = world_h/2, world_w/2

    for nr, (pattern, y, x) in enumerate(patterns):
        height, width = pattern.shape
        y = y + offset_h
        x = x + offset_w
        world[y:y+height, x:x+width] = pattern

def pattern_paths(path="cells"):
    paths = {}
    for path in glob.glob(os.sep.join([path, os.sep, "*.LIF"])):
        basename = os.path.basename(path)
        name = os.path.splitext(basename)[0]
        paths[name] = path
    return paths

def main():
    world = np.zeros((50, 185))

    paths = pattern_paths()
    for i, name in enumerate(paths):
        print (i, name)
        path = paths[name]
        patterns = cells_from_file(path)
        print (len(patterns))
        for p in patterns:
            print (p)
        insert_cells(world, patterns)
        pprint_world(world)
        break

if __name__ == "__main__":
    main()
