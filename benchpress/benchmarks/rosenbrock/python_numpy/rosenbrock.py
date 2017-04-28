from __future__ import print_function
from benchpress import util
import numpy as np

def rosen(x):
    return np.sum(
        100.0*(x[1:]-x[:-1]**2.0)**2.0 + \
        (1-x[:-1])**2.0
    )

def main():
    B = util.Benchmark()                        # Initialize Benchpress
    N, T = B.size                               # Grab command-line arguments

    if B.inputfn:
        dataset = B.load_array()
    else:
        dataset = np.arange(
            N,
            dtype=B.dtype
        ) / B.dtype(N)                       # Create psuedo-data

    if B.dumpinput:
        B.dump_arrays("rosenbrock", {'input': dataset})

    B.start()                                   # Sample wall-clock start
    res = 0.0
    for _ in range(0, T):                      # Do T trials of..
        res += rosen(dataset)                   # ..executing rosenbrock.
        util.Benchmark().flush()
    res /= T
    B.stop()                                    # Sample wall-clock stop
    B.pprint()                                  # Print elapsed wall-clock etc.

    R = np.zeros((1), dtype=B.dtype)
    R[0] = res
    if B.outputfn:
        B.tofile(B.outputfn, {'res':R})

    if B.verbose:                               # Print more, such as results
        print(R)

if __name__ == "__main__":
    main()
