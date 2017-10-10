from __future__ import print_function
from benchpress import util
import bohrium as bh


def main():
    """
    Convolve filter (any dimensional)
    Parameter: `--size<image-size>*<filter-size>*<ndims>*<niters>`
                where image and filter size is the size of each dimension (not their total size).
    """
    B = util.Benchmark()
    (image_size, filter_size, ndims, I) = B.size

    image = B.random_array((image_size**ndims,)).reshape([image_size]*ndims)
    image_filter = B.random_array((filter_size**ndims,)).reshape([filter_size]*ndims)

    B.start()
    for _ in range(I):
        R = bh.convolve_scipy(image, image_filter)
        B.flush()
    B.stop()
    B.pprint()
    if B.outputfn:
        B.tofile(B.outputfn, {'res': R})

    if B.verbose:
        print (R)


if __name__ == "__main__":
    main()
