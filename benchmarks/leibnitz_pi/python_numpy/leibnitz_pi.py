from __future__ import print_function
from benchpress import util
import numpy as np

def leibnitz_pi(N):

    n = np.arange(0, N)
    return np.sum(1.0/(4*n+1) - 1.0/(4*n+3))

def main():
    B = util.Benchmark()                        # Initialize Benchpress
    try:
        N,I = B.size                            # Grab command-line arguments
    except ValueError:
        N,I = (B.size[0], 1)
    B.start()                                   # Sample wall-clock start
    R = 0.0
    for _ in range(I):
        R += 4.0*leibnitz_pi(N)                      # Execute benchmark
        B.flush()
    B.stop()                                    # Sample wall-clock stop
    B.pprint()                                  # Print elapsed wall-clock etc.
    if B.verbose:                               # Print more, such as results
        print(R)

if __name__ == "__main__":
    main()
