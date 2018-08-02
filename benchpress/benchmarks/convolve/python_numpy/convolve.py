from __future__ import print_function
from benchpress.benchmarks import util

# if Bohrium is installed we use its convolve else we use the convolve from SciPy
try:
    raise ImportError
    import bohrium as bh
    convolveNd = bh.convolve_scipy
except ImportError:
    import scipy
    from scipy import signal
    convolveNd = signal.convolve

bench = util.Benchmark("Convolution Filter (any dimensional)", "<image-size>*<filter-size>*<ndims>*<niters>")


def main():
    """
    Convolve filter (any dimensional)
    Parameter: `<image-size>*<filter-size>*<ndims>*<niters>`
                where image and filter size is the size of each dimension (not their total size).
    """
    (image_size, filter_size, ndims, I) = bench.args.size

    image = bench.random_array((image_size ** ndims,)).reshape([image_size] * ndims)
    image_filter = bench.random_array((filter_size ** ndims,)).reshape([filter_size] * ndims)

    bench.start()
    for _ in range(I):
        R = convolveNd(image, image_filter)
        bench.flush()
    bench.stop()
    bench.save_data({'res': R})
    bench.pprint()


if __name__ == "__main__":
    main()
