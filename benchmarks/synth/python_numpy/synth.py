from __future__ import print_function
from benchpress import util
import numpy as np

def main():
    B = util.Benchmark()
    N, I = B.size

    B.start()
    a = np.ones(N)
    b = np.ones(N)
    c = np.ones(N)

    for _ in xrange(I):
        R = a+b+c

    B.stop()
    B.pprint()
    R[0]
    if B.verbose:
        print(R)
    if B.outputfn:
        B.tofile(B.outputfn, {'res': R})

if __name__ == "__main__":
    main()
