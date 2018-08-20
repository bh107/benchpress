from __future__ import print_function
from benchpress.benchmarks import util
import numpy as np

bench = util.Benchmark("Rosenbrock", "size*iterations")


def rosen(x):
    return np.sum(
        100.0 * (x[1:] - x[:-1] ** 2.0) ** 2.0 + \
        (1 - x[:-1]) ** 2.0
    )


def main():
    N, T = bench.args.size  # Grab command-line arguments
    dataset = np.arange(N, dtype=bench.dtype) / bench.dtype(N)

    bench.start()  # Sample wall-clock start
    res = 0.0
    for _ in range(0, T):  # Do T trials of..
        res += rosen(dataset)  # ..executing rosenbrock.
        bench.flush()
    res /= T
    bench.stop()  # Sample wall-clock stop
    bench.pprint()  # Print elapsed wall-clock etc.


if __name__ == "__main__":
    main()
