from __future__ import print_function
from benchpress import util
import numpy as np
from numpy.lib.stride_tricks import as_strided
import numpy_force as numpy

def main():
    U = util.Benchmark()
    N = U.size[0]
    I = U.size[1]

    T = np.ones(N)
    S = np.ones(N)
    R = np.array(numpy.random.random_integers(0,N,N), dtype=np.uint64)
    U.start()
    for _ in range(I):
        A = np.ones_like(T)
        B = np.empty(len(T)+1,dtype=T.dtype)
        B[1:] = A
        C = B[1:] + T + np.gather(S,R) + A
        D = B[:-1] + np.gather(S,R)
        E = D + T + C
        del A
        U.flush()
    U.stop()
    U.pprint()

if __name__ == "__main__":
    main()
