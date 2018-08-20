from __future__ import print_function
from benchpress.benchmarks import util
import numpy as np

bench = util.Benchmark("Monte Carlo Pi", "samples*iterations")


def montecarlo_pi(samples):
    x = bench.random_array((samples,))
    y = bench.random_array((samples,))
    m = np.sqrt(x * x + y * y) <= 1.0
    return np.sum(m) * 4.0 / samples


def solve(samples, iterations):
    acc = 0.0
    for _ in range(iterations):
        acc += montecarlo_pi(samples)
        bench.flush()
    acc /= iterations
    return acc


def main():
    samples, iterations = bench.args.size
    bench.start()
    res = solve(samples, iterations)
    bench.stop()
    bench.pprint()
    if bench.args.verbose:
        print(res)


if __name__ == "__main__":
    main()
