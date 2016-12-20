from __future__ import print_function
from benchpress import util
import numpy as np

def main():

    B = util.Benchmark()
    try:
        N,I = B.size                            # Grab command-line arguments
    except ValueError:
        N,I = (B.size[0], 1)
    nelements = B.dtype(N*N)

    # Load or create matrices
    if B.inputfn:
        arrays = B.load_arrays()
        x = arrays['x']
        y = arrays['y']
    else:
        x = np.arange(nelements, dtype=B.dtype)/nelements
        x.shape = (N, N)

        y = np.arange(N**2, dtype=B.dtype)/nelements
        y.shape = (N, N)

    if B.dumpinput:
        B.dump_arrays("mxmul", {'x': x, 'y': y})

    C = np.zeros_like(x)

    # Do the matrix multiplication
    B.start()
    for _ in range(I):
        C += np.add.reduce(x[:,np.newaxis] * np.transpose(y), -1)
        B.flush()
    #R = np.dot(x, y)
    B.stop()

    # Print / dump
    B.pprint()
    if B.outputfn:
        B.tofile(B.outputfn, {'res': C})
    if B.verbose:
        print(np.sum(C))

if __name__ == "__main__":
    main()
