from __future__ import print_function
from benchpress.benchmarks import util
import numpy as np

bench = util.Benchmark("Gaussian elimination on matrix a without pivoting", "<size>")


def gauss(a):
    """
    Perform Gaussian elimination on matrix a without pivoting
    """
    for c in range(1, a.shape[0]):
        a[c:, c - 1:] = a[c:, c - 1:] - (a[c:, c - 1] / a[c - 1, c - 1:c])[:, None] * a[c - 1, c - 1:]
        bench.flush()
    a /= np.diagonal(a)[:, None]
    return a


def main():
    n = bench.args.size[0]

    matrix = bench.load_data()
    if matrix is not None:
        matrix = matrix['matrix']
    else:
        matrix = bench.random_array((n, n))

    bench.start()
    res = gauss(matrix)
    bench.stop()
    bench.save_data({'matrix': res})
    bench.pprint()


if __name__ == "__main__":
    main()
