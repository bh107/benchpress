from __future__ import print_function
from benchpress import util
import numpy as np
from numpy.lib.stride_tricks import as_strided
import numpy_force as numpy

def mshare(T,S,R):
    A = np.empty(1)

    #Manual broadcast of 'A' to a vector that match 'T'
    A = as_strided(A, shape=T.shape, strides=(0,))
    A.strides = (0,)
    A[:] = 42

    C = A + 43
    E = C * T * np.gather(S,R) * A
    D = C[::-1] * T * np.gather(S,R)
    return (D,C)

def main():
    B = util.Benchmark()
    N = B.size[0]
    I = B.size[1]

    T = np.ones(N)
    S = np.ones(N)
    R = np.array(numpy.random.random_integers(0,N,N))
    B.start()
    for _ in xrange(I):
        t = mshare(T,S,R)
        B.flush()
    B.stop()
    B.pprint()

if __name__ == "__main__":
    main()
