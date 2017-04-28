from __future__ import print_function
from benchpress import util
import numpy as np

def comparison_01(x):
    x = x +1
    return x

def comparison_02(x):
    x = x +1
    return x

comparisons = {
    1: comparison_01,
    2: comparison_02
}

def main():
    B = util.Benchmark()
    
    samples, iterations, comp = B.size
    x = np.ones(samples) 
    B.start()
    R = comparisons[comp](x)
    B.stop()
    B.pprint()
    if B.verbose:
        print(R)

if __name__ == "__main__":
    main()

