# -*- coding: utf-8 -*-
from benchpress import util
import numpy as np

def main():
    B = util.Benchmark()

    k       = B.size[0] # number of plane waves
    stripes = B.size[1] # number of stripes per wave
    N       = B.size[2] # image size in pixels
    ite     = B.size[3] # iterations

    phases  = np.arange(0, 2*np.pi, 2*np.pi/ite)
    image   = np.empty((N, N), dtype=B.dtype)
    d       = np.arange(-N/2, N/2, dtype=B.dtype)

    xv, yv = np.meshgrid(d, d)
    theta  = np.arctan2(yv, xv)
    r      = np.log(np.sqrt(xv*xv + yv*yv))
    r[np.isinf(r) == True] = 0

    tcos   = theta * np.cos(np.arange(0, np.pi, np.pi/k))[:, np.newaxis, np.newaxis]
    rsin   = r * np.sin(np.arange(0, np.pi, np.pi/k))[:, np.newaxis, np.newaxis]
    inner  = (tcos - rsin) * stripes

    cinner = np.cos(inner)
    sinner = np.sin(inner)

    B.start()

    for phase in phases:
        image[:] = np.sum(cinner * np.cos(phase) - sinner * np.sin(phase), axis=0) + k
        util.Benchmark().flush()

    B.stop()
    B.pprint()

    if B.outputfn:
        B.tofile(B.outputfn, {'res': image})

if __name__ == "__main__":
    main()
