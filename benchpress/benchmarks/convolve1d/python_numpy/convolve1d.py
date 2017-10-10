"""
Convolve filter (1. dimensional)
Parameter: `--size<image-size>*<filter-size>*<niters>`.
"""

from __future__ import print_function
from benchpress import util
import numpy as np


def main():
    B = util.Benchmark()
    (image_size, filter_size, I) = B.size

    image = B.random_array((image_size,))
    image_filter = B.random_array((filter_size,))

    B.start()
    for _ in range(I):
        R = np.convolve(image, image_filter)
        B.flush()
    B.stop()
    B.pprint()
    if B.outputfn:
        B.tofile(B.outputfn, {'res': R})

    if B.verbose:
        print (R)


if __name__ == "__main__":
    main()
