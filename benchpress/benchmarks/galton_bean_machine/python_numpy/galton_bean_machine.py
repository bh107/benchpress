from __future__ import print_function
from benchpress import util
import numpy as np


def bean(B, num_beans, height):
    return np.sum(np.sign(B.random_array((num_beans, height))-0.5), axis=1)


def main():
    B = util.Benchmark()
    num_beans, height = B.size

    B.start()
    R = bean(B, num_beans, height)
    B.stop()

    B.pprint()
    if B.verbose:
        print(R)
    if B.visualize:
        from matplotlib import pyplot
        bins   = 100
        pyplot.hist(R, bins)
        pyplot.title("Galton Normal distribution")
        pyplot.xlabel("Value")
        pyplot.ylabel("Frequency")
        pyplot.show()
    if B.outputfn:
        B.tofile(B.outputfn, {'res': R})

if __name__ == "__main__":
    main()
