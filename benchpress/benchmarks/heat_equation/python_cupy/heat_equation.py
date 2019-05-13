from __future__ import print_function
import cupy as np
from benchpress.benchmarks import util

bench = util.Benchmark("Solving the heat equation using the jacobi method", "height*width*iterations")


def init_grid(height, width, dtype=np.float32):
    grid = np.zeros((height + 2, width + 2), dtype=dtype)
    grid[:, 0] = dtype(-273.15)
    grid[:, -1] = dtype(-273.15)
    grid[-1, :] = dtype(-273.15)
    grid[0, :] = dtype(40.0)
    return grid


def jacobi(grid, epsilon=0.005, max_iterations=None):
    def loop_body(grid):
        center = grid[1:-1, 1:-1]
        north = grid[0:-2, 1:-1]
        east = grid[1:-1, 2:]
        west = grid[1:-1, 0:-2]
        south = grid[2:, 1:-1]
        work = 0.2 * (center + north + east + west + south)
        delta = np.sum(np.absolute(work - center))
        center[:] = work
        bench.plot_surface(grid, "2d", 0, 200, -200)
        return delta > epsilon

    bench.do_while(loop_body, max_iterations, grid)
    return grid


def main():
    H = bench.args.size[0]
    W = bench.args.size[1]
    I = bench.args.size[2]

    grid = bench.load_data()
    if grid is not None:
        grid = grid['grid']
    else:
        grid = init_grid(H, W, dtype=bench.dtype)

    bench.start()
    grid = jacobi(grid, max_iterations=I)
    bench.stop()
    bench.save_data({'grid': grid})
    bench.pprint()


if __name__ == "__main__":
    main()
