from __future__ import print_function

"""
Game of Life
------------

"""
from benchpress.benchmarks import util
import numpy as np

bench = util.Benchmark("Game of Life", "height*width*iterations*rules")

SURVIVE_LOW = 2
SURVIVE_HIGH = 3
SPAWN = 3


def world(height, width):
    state = np.ones((height + 2, width + 2), dtype=bench.dtype)
    state[2:-2, 2:-2] = bench.dtype(0)
    return state


def world_zeros(height, width):
    state = np.zeros((height + 2, width + 2), dtype=bench.dtype)
    return state


def play(state, iterations, version=1, visualize=False):
    cells = state[1:-1, 1:-1]
    ul = state[0:-2, 0:-2]
    um = state[0:-2, 1:-1]
    ur = state[0:-2, 2:]
    ml = state[1:-1, 0:-2]
    mr = state[1:-1, 2:]
    ll = state[2:, 0:-2]
    lm = state[2:, 1:-1]
    lr = state[2:, 2:]

    def update():
        """
        This is the first implementation of the game rules.
        """
        neighbors = ul + um + ur + ml + mr + ll + lm + lr  # count neighbors
        live = neighbors * cells  # extract live cells neighbors
        stay = (live >= SURVIVE_LOW) & (live <= SURVIVE_HIGH)  # find cells the stay alive
        dead = neighbors * (cells == 0)  # extract dead cell neighbors
        spawn = dead == SPAWN  # find cells that spaw new life

        cells[:] = stay | spawn  # save result for next iteration

    def update_optimized():
        """
        This is an optimized implementation of the game rules.
        """
        neighbors = ul + um + ur + ml + mr + ll + lm + lr  # Count neighbors

        c1 = (neighbors == SURVIVE_LOW)  # Life conditions
        c2 = (neighbors == SPAWN)

        cells[:] = cells * c1 + c2  # Update

    if version == 1:  # Select the update function
        update_func = update
    elif version == 2:
        update_func = update_optimized

    for i in range(iterations):  # Run the game
        if visualize:
            bench.plot_surface(state, "3d", 16, 1, 0)
        update_func()
        bench.flush()

    return state


def main():
    (H, W, I, V) = bench.args.size

    if V not in [1, 2]:
        raise Exception("Unsupported rule-implementation.")

    S = world(H, W)

    bench.start()
    R = play(S, I, V, bench.args.visualize)
    bench.stop()
    bench.save_data({'res': R})
    bench.pprint()


if __name__ == "__main__":
    main()
