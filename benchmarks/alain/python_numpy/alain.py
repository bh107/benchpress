from __future__ import print_function
from benchpress import util
import numpy as np

def alain(E):
    N = len(E)-2
    A = np.empty(N+2)
    B = np.empty(N+2)
    C = np.empty(N+2)
    D = np.empty(N+2)
    H = np.empty(N+2)

    A[1:N] = E[0:N-1]
    B[1:N] = A[1:N]*2+3
    C[1:N] = B[1:N] + 99

    D[1:N] = A[N:1:-1] + A[1:N]
    E[1:N] = B[1:N] + C[1:N]*D[1:N]
    F = E[1:N]*4+2
    G = E[1:N]*8-3
    H[1:N] = F + G*E[N:1:-1]
    return H

def main():
    B = util.Benchmark()
    N = B.size[0]
    I = B.size[1]

    E = np.ones(N+2)
    B.start()
    for _ in xrange(I):
        H = alain(E)
        B.flush()
    B.stop()
    B.pprint()

if __name__ == "__main__":
    main()
