"""
Convolve filter (1. dimensional)
Parameter: `--size<image-size>*<filter-size>*<niters>`.
"""

from __future__ import print_function
from benchpress.benchmarks import util
import numpy as np

bench = util.Benchmark("Convolution Filter 1D", "<image-size>*<filter-size>*<niters>")


def main():
    (image_size, filter_size, I) = bench.args.size

    image = bench.random_array((image_size,))
    image_filter = bench.random_array((filter_size,))

    bench.start()
    for _ in range(I):
        R = np.convolve(image, image_filter)
        bench.flush()
    bench.stop()
    bench.save_data({'res': R})
    bench.pprint()


if __name__ == "__main__":
    main()
