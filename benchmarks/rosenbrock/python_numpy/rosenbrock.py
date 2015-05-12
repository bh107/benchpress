from __future__ import print_function
from benchpress import util
import numpy as np

def rosen(x):
    return np.sum((1-x[:-1])**2.0 + 100.0*(x[1:]-x[:-1]**2.0)**2.0)

def main():
    B = util.Benchmark()                        # Initialize Benchpress
    N, T = B.size                               # Grab command-line arguments
    dataset = np.arange(
        N,
        dtype=np.float64
    ) / np.float64(N)                           # Create psuedo-data
    B.start()                                   # Sample wall-clock start
    for _ in xrange(0, T):                      # Do T trials of..
        R = rosen(dataset)                      # ..executing rosenbrock.
    B.stop()                                    # Sample wall-clock stop
    B.pprint()                                  # Print elapsed wall-clock etc.
    if B.verbose:                               # Print more, such as results
        print(R)

if __name__ == "__main__":
    main()
