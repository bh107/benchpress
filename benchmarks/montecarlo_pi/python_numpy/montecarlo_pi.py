from __future__ import print_function
from benchpress import util
import numpy as np

def montecarlo_pi_se(samples, B):

    return np.sum(np.sqrt(
        B.random_array((samples,), dtype=B.dtype)**2 + \
        B.random_array((samples,), dtype=B.dtype)**2
    ) <= 1.0) * 4.0 / samples

def montecarlo_pi(samples, B):

    x = B.random_array((samples,), dtype=B.dtype)
    y = B.random_array((samples,), dtype=B.dtype)
    m = np.sqrt(x*x + y*y) <= 1.0

    return np.sum(m) * 4.0 / samples

def solve(samples, iterations, B):
    acc=0.0
    for _ in range(iterations):
        acc += montecarlo_pi(samples, B)
	util.Benchmark().flush()
    acc /= iterations
    return acc

def main():
    B = util.Benchmark()
    samples, iterations = B.size
    B.start()
    R = solve(samples, iterations, B)
    B.stop()
    B.pprint()
    if B.verbose:
        print(R)

if __name__ == "__main__":
    main()
