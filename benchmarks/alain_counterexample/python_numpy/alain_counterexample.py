from __future__ import print_function
from benchpress import util
import numpy as np
from numpy.lib.stride_tricks import as_strided

def mshare(T,S):
    A = np.empty(1)

    #Manual broadcast of 'A' to a vector that match 'T' and 'S'
    A = as_strided(A, shape=T.shape, strides=(0,))
    A.strides = (0,)
    A[:] = 42

    C = A + 43
    A[:] += C / T / S
    D = C[::-1] - T - S
    return D

def main():
    B = util.Benchmark()
    N = B.size[0]
    I = B.size[1]

    T = np.ones(N)
    S = np.ones(N)
    B.start()
    for _ in xrange(I):
        T = mshare(T,S)
        B.flush()
    B.stop()
    B.pprint()

if __name__ == "__main__":
    main()
