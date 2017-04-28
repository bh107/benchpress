#!/usr/bin/env python
from __future__ import print_function
import sys
from benchpress import util
import numpy as np

def pow_this_01(n, k):
    return np.sum(n**k)

def pow_this_02(n, k):
    return np.sum(((n*n)**2)*n)

def pow_this_03(n, k):
    return np.sum(((n**2)**2)*n)

def main():
    B = util.Benchmark()
    if len(B.size) != 2:
        sys.exit("Invalid amount of arguments.")
        return
    N, K = B.size

    n = np.arange(0, 1, 1.0/N)

    B.start()
    #R = np.sum(**K)
    R = pow_this_01(n, K)
    #R = pow_this_02(n, k)
    #R = pow_this_03(n, k)

    B.stop()
    B.pprint()

    if B.verbose:
        print(R)

if __name__ == "__main__":
    main()
