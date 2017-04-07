# This Python file uses the following encoding: utf-8
from __future__ import print_function
from benchpress import util
import numpy as np
import math

def window(B,a=0.37):
    assert (len(B.shape) == 2)
    assert (B.shape[0] == B.shape[1])
    n = B.shape[0]
    wl = np.ones_like(B[0])
    b = int(np.ceil((a * (n-1) / 2)))
    wl[:b]  =  0.5 * (1 + np.cos(math.pi*(2 * np.arange(b) / (a * (n-1)) - 1)))
    wl[-b:] =  0.5 * (1 + np.cos(math.pi*(2 * np.arange(b-1,-1,-1) / (a * (n-1)) - 1)))
    wl *= wl
    w = np.sqrt(wl+wl[:,None])
    return B*w


def calcB(B_x0, alpha=0.0,
          x_min = 0.0, x_max = 0.25,
          y_min = 0.0, y_max = 1.0,
          z_min = 0.0, z_max = 1.0):

    n = len(B_x0)
    x = np.linspace(x_min,x_max,num=n, endpoint=False).astype(B_x0.dtype,copy=False)
    y = np.linspace(y_min,y_max,num=n).astype(B_x0.dtype,copy=False)
    z = np.linspace(z_min,z_max,num=n).astype(B_x0.dtype,copy=False)
    u = np.arange(n,dtype=B_x0.dtype)

    # Making C
    C = 4.0 / (n-1.0)**2 * np.sum(np.sum((B_x0 * np.sin(math.pi/y_max * u * y[:,None])[:,:,None])[:,None] * np.sin(math.pi/z_max * u * z[:,None])[:,None],-1),-1)
    l = np.pi**2 * ((u**2 / y_max)[:,None] + (u**2 / z_max))
    l[0,0] = 1.0
    r = np.sqrt(l - alpha**2)

    # Calculating B
    sincos = np.sin(math.pi/y_max * u * y[:, None])[:, None, :, None] * (u * np.cos(math.pi/z_max * u * z[:,None]))[None, :, None, :]
    cossin = (u * np.cos(math.pi/y_max * u * y[:,None]))[:, None, :, None] * np.sin(math.pi/z_max * u * z[:,None])[None, :, None, :]
    temp_x = C * np.sin(math.pi/y_max * u * y[:,None])[:, None, :, None] * np.sin(math.pi/z_max * u * z[:,None])[None, :, None, :]
    temp_y = C / l * (alpha * math.pi / z_max * sincos - r * math.pi / y_max * cossin)
    temp_z = C / l * (alpha * math.pi / y_max * cossin + r * math.pi / z_max * sincos)
    exprx = np.exp((-r * x[:, None, None]))

    Bx = np.sum(np.sum(temp_x * exprx[:,None,None],-1),-1)
    By = np.sum(np.sum(temp_y * exprx[:,None,None],-1),-1)
    Bz = np.sum(np.sum(temp_z * exprx[:,None,None],-1),-1)
    return (Bx, By, Bz)


def main():

    B = util.Benchmark()

    if B.inputfn is None:
        B_x0 = B.random_array((B.size[0],B.size[1]), dtype=B.dtype)
    else:
        inputfn = B.inputfn if B.inputfn else '../idl_input-float64_512*512.npz'
        sd = { 512:1, 256:2, 128:4, 64:8, 32:16, 16:32 }
        try:
            h = sd[B.size[0]]
            w = sd[B.size[1]]
        except KeyError:
            raise ValueError('Only valid sizes are: '+str(sd.keys()))
        B_x0 = B.load_array(inputfn, 'input', dtype=B.dtype)[::h,::w]

    B.start()
    for _ in range(B.size[2]):
        Rx, Ry, Rz = calcB(window(B_x0))
        B.flush()
    B.stop()
    B.pprint()

    if B.outputfn:
        R = Rx+Ry+Rz
        B.tofile(B.outputfn, {'res': R, 'res_x': Rx, 'res_y': Ry, 'res_z': Rz})

if __name__ == '__main__':
    main()
