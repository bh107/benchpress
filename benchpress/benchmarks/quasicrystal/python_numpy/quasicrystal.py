# -*- coding: utf-8 -*-
from benchpress.benchmarks import util
import numpy as np

bench = util.Benchmark("Quasi Crystal simulation", "k*stripes*image_size*iterations")


def main():
    k = bench.args.size[0]  # number of plane waves
    stripes = bench.args.size[1]  # number of stripes per wave
    N = bench.args.size[2]  # image size in pixels
    ite = bench.args.size[3]  # iterations

    phases = np.arange(0, 2 * np.pi, 2 * np.pi / ite)
    image = np.empty((N, N), dtype=bench.dtype)
    d = np.arange(-N / 2, N / 2, dtype=bench.dtype)

    xv, yv = np.meshgrid(d, d)
    theta = np.arctan2(yv, xv)
    r = np.log(np.sqrt(xv * xv + yv * yv))
    r[np.isinf(r) == True] = 0

    tcos = theta * np.cos(np.arange(0, np.pi, np.pi / k))[:, np.newaxis, np.newaxis]
    rsin = r * np.sin(np.arange(0, np.pi, np.pi / k))[:, np.newaxis, np.newaxis]
    inner = (tcos - rsin) * stripes

    cinner = np.cos(inner)
    sinner = np.sin(inner)

    bench.start()
    for phase in phases:
        image[:] = np.sum(cinner * np.cos(phase) - sinner * np.sin(phase), axis=0) + k
        bench.flush()
    bench.stop()
    bench.pprint()


if __name__ == "__main__":
    main()
