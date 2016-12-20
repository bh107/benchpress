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

def calcB(B, alpha=1.0,
          x_min = 0.0, x_max = 0.25,
          y_min = 0.0, y_max = 1.0,
          z_min = 0.0, z_max = 1.0):

    n = len(B)
    x = np.linspace(x_min,x_max,num=n,endpoint=False)
    y = np.linspace(y_min,y_max,num=n)
    z = np.linspace(z_min,z_max,num=n)
    u = np.arange(n,dtype=B.dtype)


    uy = math.pi/y_max * u * y[:,None]
    uz = math.pi/z_max * u * z[:,None]

    sinuy = np.sin(uy)
    sinuz = np.sin(uz)

#    C =  4.0 / (n-1.0)**2 * np.sum(np.sum((B * sinuy[:,:,None])[:,None] * sinuz[:,None],-1),-1)
    C = np.empty((n,n,n,n))
    C[:] = sinuy[:,None,:,None]
    C *= B
    C *= sinuz[:,None]
    C = 4.0 / (n-1.0)**2 * np.sum(np.sum(C,-1),-1)

    l = math.pi**2 * ((u**2 / y_max)[:,None] + (u**2 / z_max))
    l[0,0] = 1.0
    r = np.sqrt(l - alpha**2)

    C_l = C / l

    d5 = (n,n,n,n,n)

#    sincos = sinuy[:,None,:,None] * (u * np.cos(uz))[None,:,None,:]
    sincos = np.empty(d5)
    sincos[:] = sinuy[:,None,:,None]
    sincos *= (u * np.cos(math.pi/z_max * u * z[:,None]))[None,:,None,:]

#    cossin = (u * np.cos(uy))[:,None,:,None] * sinuz[None,:,None,:]
    cossin = np.empty(d5)
    cossin[:] = sinuz[None,:,None,:]
    cossin *= (u * np.cos(math.pi/y_max * u * y[:,None]))[:,None,:,None]

#    exprx = np.exp((-r * x[:,None,None]))[:,None,None]
    exprx = np.empty(d5)
    exprx[:] = -x[:,None,None,None,None]
    exprx *= r
    exprx = np.exp(exprx)

#    temp_x = C * sinuy[:,None,:,None] * sinuz[None,:,None,:]
    temp_x = np.empty(d5)
    temp_x[:] = sinuy[:,None,:,None]
    temp_x *= sinuz[None,:,None,:]
    temp_x *= C

#    temp_y = C / l * (alpha * math.pi / z_max * sincos - r * math.pi / y_max * cossin)
    temp_y = -(math.pi/y_max) * cossin
    temp_y *= r
    temp_y += (alpha*math.pi/z_max) * sincos
    temp_y *= C_l

#    temp_z = C / l * (alpha * math.pi / y_max * cossin + r * math.pi / z_max * sincos)
    temp_z = (math.pi/z_max) * sincos
    temp_z *= r
    temp_z += (alpha*math.pi/y_max) * cossin
    temp_z *= C_l

    Bx = np.sum(np.sum(temp_x * exprx,-1),-1)
    By = np.sum(np.sum(temp_y * exprx,-1),-1)
    Bz = np.sum(np.sum(temp_z * exprx,-1),-1)
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
    B.stop()
    B.pprint()

    if B.outputfn:
        R = Rx+Ry+Rz
        B.tofile(B.outputfn, {'res': R, 'res_x': Rx, 'res_y': Ry, 'res_z': Rz})

if __name__ == '__main__':
    main()
