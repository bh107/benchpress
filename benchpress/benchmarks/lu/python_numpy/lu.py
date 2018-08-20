from __future__ import print_function
from benchpress.benchmarks import util
import numpy as np

bench = util.Benchmark("LU decomposition on the matrix so that A = L*U", "<size>")


def lu(a):
    """
    Perform LU decomposition on the matrix `a` so that A = L*U
    """
    u = a.copy()
    l = np.identity(a.shape[0], a.dtype)
    for c in range(1, u.shape[0]):
        l[c:, c - 1] = (u[c:, c - 1] / u[c - 1, c - 1:c])
        u[c:, c - 1:] = u[c:, c - 1:] - l[c:, c - 1][:, None] * u[c - 1, c - 1:]
        bench.flush()
    return (l, u)


def main():
    n = bench.args.size[0]
    matrix = bench.random_array((n, n))
    bench.start()
    res = lu(matrix)
    bench.stop()
    bench.pprint()


if __name__ == "__main__":
    main()
