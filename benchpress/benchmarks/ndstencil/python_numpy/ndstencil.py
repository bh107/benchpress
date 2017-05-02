from __future__ import print_function
import itertools as it
from benchpress import util
import numpy as np

def create_shape(dims, size=20):
    """
    Generate a suitable N dimensional shape of size
    size**2 core elements
    """
    shape=[]
    for _ in range(dims):
        ds = size/dims
        shape.append(2**ds+2)
        dims-=1
        size-=ds

    return shape

def create_world(shape, core_v, edge_v, dtype=np.float32):
    """
    Generate an N=len(shape) dimensional world with core values
    set to core_v and edge values set to edge_v
    """
    w = np.empty(shape, dtype=dtype)
    w[:] = w.dtype.type(edge_v)
    v = [s for s in it.starmap(slice,it.repeat((1,-1),len(w.shape)))]
    w[tuple(v)][:] = w.dtype.type(core_v)

    return w

def create_random_world(shape, B):
    """
    Generate an N=len(shape) dimensional world with
    random values.

    .. note:: This is not used...
    """
    return np.array(B.random_array(shape), dtype=B.dtype)

def solve(stencil, world, I):
    """
    Run a simple dence stencil operation on a ND array world
    for I iterations
    """
    FAC = 1.0/len(stencil)
    for _ in range(I):
        stencil[len(stencil)/2][:] = sum(stencil)*FAC
        util.Benchmark().flush()

    return world

def main():
    B = util.Benchmark()
    size    = B.size[0]
    I       = B.size[1]
    D       = B.size[2]

    if B.inputfn:
        world = B.load_array()
    else:
        world = create_world(create_shape(D, size), 0.0, 255.0, dtype=B.dtype)
        #world = create_random_world(create_shape(D, size), B)

    stencil = [world[tuple(s)] for s in [map((lambda se : slice(se[0],se[1])),i)
                                  for i in it.product([(0,-2),(1,-1),(2,None)],
                                                      repeat=len(world.shape))]]
    if B.dumpinput:
        B.dump_arrays("ndstencil", {'input': world})

    B.start()
    R = solve(stencil, world, I)
    B.stop()
    B.pprint()
    if B.verbose:
        print( "Solving",D, "dimensional",world.shape,"problem with",       \
               len([i for i in it.product([None,None,None], repeat=D)]),    \
               "point stencil.")
    if B.outputfn:
        B.tofile(B.outputfn, {'res': R})
    if B.visualize and D in [2]:
        util.visualize_grid(world, "World", block=True)

if __name__ == "__main__":
    main()