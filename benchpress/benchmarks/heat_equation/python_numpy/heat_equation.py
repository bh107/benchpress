from __future__ import print_function
from benchpress import util
import numpy as np


def init_grid(height, width, dtype=np.float32):
    grid = np.zeros((height + 2, width + 2), dtype=dtype)
    grid[:, 0] = dtype(-273.15)
    grid[:, -1] = dtype(-273.15)
    grid[-1, :] = dtype(-273.15)
    grid[0, :] = dtype(40.0)
    return grid


def jacobi(B, grid, epsilon=0.005, max_iterations=None, visualize=False):
    def loop_body(grid):
        center = grid[1:-1, 1:-1]
        north = grid[0:-2, 1:-1]
        east = grid[1:-1, 2:]
        west = grid[1:-1, 0:-2]
        south = grid[2:, 1:-1]
        work = 0.2 * (center + north + east + west + south)
        delta = np.sum(np.absolute(work - center))
        center[:] = work

        if visualize:
            util.plot_surface(grid, "2d", 0, 200, -200)
        return delta > epsilon

    B.do_while(loop_body, max_iterations, grid)
    return grid


def main():
    B = util.Benchmark()
    H = B.size[0]
    W = B.size[1]
    I = B.size[2]

    grid = B.load_data()
    if grid is not None:
        grid = grid['grid']
    else:
        grid = init_grid(H, W, dtype=B.dtype)

    B.start()
    grid = jacobi(B, grid, max_iterations=I, visualize=B.visualize)
    B.stop()
    B.save_data({'grid': grid})
    B.pprint()
    if B.verbose:
        print("Iterations=%s, Grid: %s." % (I, grid))
    if B.visualize:
        util.confirm_exit()


if __name__ == "__main__":
    main()
