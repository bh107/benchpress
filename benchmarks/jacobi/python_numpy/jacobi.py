from __future__ import print_function
from benchpress import util
import numpy as np
from bohrium.stdviews import no_border, grid, diagonals

def jacobi_init(size):

    v    = np.arange(size)
    data = (v*(v[np.newaxis,:].T+2)+2)/size

    return data

def jacobi(data, max_iterations=0):

    active      = no_border(data,1)
    g           = grid(data,1)
    d           = diagonals(data,1)
    fak         = 1./20
    residual    = 110000000

    iterations = 0
    while residual>(10**-2) * (active.shape[0]**2):
        update    = (4*sum(g) + sum(d))*fak
        residual  = np.sum(abs(update-active))
        active[:] = update
        iterations += 1
        util.Benchmark().flush()

        if max_iterations and iterations >= max_iterations:
            break

    return iterations, data

def main():
    B = util.Benchmark()
    N, I = B.size
    data = jacobi_init(N)

    B.start()
    M, R = jacobi(data, I)
    B.stop()

    B.pprint()
    if B.verbose:
        print(R)
    if B.visualize:
        util.visualize_grid(R, block=True)
    if B.outputfn:
        B.tofile(B.outputfn, {'res': R})

if __name__ == "__main__":
    main()
