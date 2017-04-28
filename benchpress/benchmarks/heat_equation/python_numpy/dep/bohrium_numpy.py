import bohrium as np
import time
import sys

def solve(grid, iter):
    center = grid[1:-1,1:-1]
    north  = grid[ :-2,1:-1]
    south  = grid[2:  ,1:-1]
    east   = grid[1:-1,2:  ]
    west   = grid[1:-1, :-2]
    for _ in range(iter):
        tmp = 0.2*(center+north+south+east+west)
        delta = np.sum(np.absolute(tmp-center))
        center[:] = tmp

if len(sys.argv) != 3:
    raise RuntimeError("Need two arguments: domain-size and number of iterations")

width = int(sys.argv[1])
iter  = int(sys.argv[2])

grid = np.arange(width**2).reshape((width,width))

np.flush()
now = time.time()
solve(grid, iter)
np.flush()
delta = time.time() - now

print "bohrium_numpy.py - iter: %d size: %d elapsed-time: %f"%(iter, width, delta)

