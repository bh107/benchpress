from __future__ import print_function
from benchpress import util
import numpy as np

def init_grid(height, width, dtype=np.float32):
    grid        = np.zeros((height+2,width+2), dtype=dtype)
    grid[:,0]   = dtype(-273.15)
    grid[:,-1]  = dtype(-273.15)
    grid[-1,:]  = dtype(-273.15)
    grid[0,:]   = dtype(40.0)
    return grid

def jacobi(grid, iterations, visualize=False):

    center = grid[1:-1, 1:-1]
    north  = grid[0:-2, 1:-1]
    east   = grid[1:-1, 2:  ]
    west   = grid[1:-1, 0:-2]
    south  = grid[2:  , 1:-1]

    for i in xrange(iterations):
        center[:] = 0.2*(center+north+east+west+south)

        if util.Benchmark().bohrium:
            np.flush()
        if visualize:
            util.plot_surface(grid, "2d", 0, 200, -200)

    return grid

def main():
    B = util.Benchmark()
    H = B.size[0]
    W = B.size[1]
    I = B.size[2]

    if B.inputfn:
        grid = B.load_array()
    else:
        grid = init_grid(H, W, dtype=B.dtype)

    if B.dumpinput:
        B.dump_arrays("jacobi_solve", {'input': grid})

    B.start()
    grid = jacobi(grid, I, visualize=B.visualize)
    B.stop()

    B.pprint()
    if B.verbose:
        print(grid)
    if B.outputfn:
        B.tofile(B.outputfn, {'res': grid})
    if B.visualize:
        util.confirm_exit()

if __name__ == "__main__":
    main()
