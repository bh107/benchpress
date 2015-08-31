from __future__ import print_function
import sys
from benchpress import util
import numpy as np

def stream_this(generator, N):

    x = generator(N)
    y = generator(N)
    z = (x*x + y*y) / 4
    r = np.sum(z)

    return r

def main():
    B = util.Benchmark()
    if len(B.size) != 3:
        sys.exit("Invalid amount of arguments.")
        return
    N, I, S = B.size

    if S not in [0,1,2]:
        sys.exit("Invalid choice of generator [%d], should be: 0, 1, 2." % S)
        return

    generator = [
        np.ones,
        np.arange,
        np.random.random
    ]

    B.start()
    R = 0.0
    for _ in xrange(I):
        R += stream_this(generator[S], N)
    R /= I

    B.stop()
    B.pprint()

    if B.verbose:
        print(R)
    if B.outputfn:
        B.tofile(B.outputfn, {'res': R})

if __name__ == "__main__":
    main()
