from __future__ import print_function
from benchpress import util
import numpy as np

def alain(A,E):
    N = len(E)-2

    A[1:N] = E[0:N-1]
    B = A[1:N]*2+3
    C = B + 99

    D = A[N:1:-1] + A[1:N]
    E[1:N] = B+C*D
    F = E[1:N]*4+2
    G = E[1:N]*8-3
    H = F + G*E[N:1:-1]
    return H

def alain_all_labeled(A,E):
    N = len(E)-2

    A[1:N] = E[0:N-1]

    # B = A[1:N]*2+3
    B = A[1:N]*2
    B += 3

    C = B + 99

    D = A[N:1:-1] + A[1:N]

    # E[1:N] = B+C*D
    E[1:N] = B
    E[1:N] += C
    E[1:N] *= D

    # F = E[1:N]*4+2
    F = E[1:N]*4
    F += 2

    # G = E[1:N]*8-3
    G = E[1:N]*8
    G -= 3

    # H = F + G*E[2:N+1]
    H = F + G
    H *= E[2:N+1]
    return H

def main():
    B = util.Benchmark()
    N = B.size[0]
    I = B.size[1]

    A = np.ones(N+2)
    E = np.ones(N+2)
    B.start()
    for _ in range(I):
        H = alain_all_labeled(A,E)
        B.flush()
    B.stop()
    B.pprint()

if __name__ == "__main__":
    main()
