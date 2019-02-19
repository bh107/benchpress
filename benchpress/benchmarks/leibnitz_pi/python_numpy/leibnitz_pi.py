from __future__ import print_function
from benchpress.benchmarks import util
import numpy as np

bench = util.Benchmark("Leibnitz Pi", "<size>*<niters>")


def leibnitz_pi(N):
    n = np.arange(0, N)
    return np.sum(1.0 / (4 * n + 1) - 1.0 / (4 * n + 3))


def main():
    (size, niter) = bench.args.size

    bench.start()
    pi = 0.0
    for _ in range(niter):
        pi += 4.0 * leibnitz_pi(size)  # Execute benchmark
        bench.flush()
    pi /= niter
    bench.stop()
    bench.pprint()
    if bench.args.verbose:
        print(pi)


if __name__ == "__main__":
    main()
