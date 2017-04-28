from __future__ import print_function
"""
Game of Life
------------

So what does this code example illustrate?
"""
from benchpress import util
from gameoflife_utils import pattern_paths, insert_cells, cells_from_file
import numpy as np

SURVIVE_LOW     = 2
SURVIVE_HIGH    = 3
SPAWN           = 3

def world(height, width, B):
    state = np.ones((height+2, width+2), dtype=B.dtype)
    state[2:-2, 2:-2] = B.dtype(0)
    return state

def world_zeros(height, width, B):
    state = np.zeros((height+2, width+2), dtype=B.dtype)
    return state

def play(state, iterations, version=1, visualize=False):

    cells = state[1:-1,1:-1]
    ul = state[0:-2, 0:-2]
    um = state[0:-2, 1:-1]
    ur = state[0:-2, 2:  ]
    ml = state[1:-1, 0:-2]
    mr = state[1:-1, 2:  ]
    ll = state[2:  , 0:-2]
    lm = state[2:  , 1:-1]
    lr = state[2:  , 2:  ]

    def update():
        """
        This is the first implementation of the game rules.
        """
        neighbors = ul + um + ur + ml + mr + ll + lm + lr       # count neighbors
        live = neighbors * cells                                # extract live cells neighbors
        stay = (live >= SURVIVE_LOW) & (live <= SURVIVE_HIGH)   # find cells the stay alive
        dead = neighbors * (cells == 0)                         # extract dead cell neighbors
        spawn = dead == SPAWN                                   # find cells that spaw new life

        cells[:] = stay | spawn                                 # save result for next iteration

    def update_optimized():
        """
        This is an optimized implementation of the game rules.
        """
        neighbors = ul + um + ur + ml + mr + ll + lm + lr       # Count neighbors

        c1 = (neighbors == SURVIVE_LOW)                         # Life conditions
        c2 = (neighbors == SPAWN)

        cells[:] = cells * c1 + c2                              # Update

    if version == 1:                # Select the update function
        update_func = update
    elif version == 2:
        update_func = update_optimized

    for i in range(iterations):    # Run the game
        if visualize:
            util.plot_surface(state, "3d", 16, 1, 0)
        update_func()
        util.Benchmark().flush()

    return state

def main():

    B = util.Benchmark()
    (H, W, I, V) = B.size

    if V not in [1, 2]:
        raise Exception("Unsupported rule-implementation.")
    if B.inputfn:
        if "LIF" in B.inputfn:
            paths = pattern_paths("cells")
            S = world_zeros(H, W, B)
            cells = cells_from_file(B.inputfn)
            insert_cells(S, cells)
        else:
            S = B.load_array()
    else:
        S = world(H, W, B)

    B.start()
    R = play(S, I, V, B.visualize)
    B.stop()

    B.pprint()
    if B.outputfn:
        B.tofile(B.outputfn, {'res': R})
    if B.visualize:
        util.confirm_exit()

if __name__ == "__main__":
    main()
