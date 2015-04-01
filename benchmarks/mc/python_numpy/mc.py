from __future__ import print_function
from benchpress import util
import numpy as np

def solve(N, B):
    x = B.random_array((N,), dtype=B.dtype)
    y = B.random_array((N,), dtype=B.dtype)
    z = np.sqrt(x**2 + y**2) <= 1.0
    return np.sum(z) * 4.0 / N

def montecarlo_pi(N, I, B):
    acc=0.0
    for i in xrange(I):
        acc += solve(N, B)
    acc /= I
    return acc

def main():
    B = util.Benchmark()
    N, I = B.size
    B.start()
    R = montecarlo_pi(N, I, B)
    B.stop()
    B.pprint()
    if B.verbose:
        print(R)

if __name__ == "__main__":
    main()
