# This Python file uses the following encoding: utf-8
from __future__ import print_function
from benchpress import util
import numpy as np
import math
try:
    import numpy_force as npf
except ImportError:
    import numpy as npf

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

    uz = math.pi/z_max * u * z[:,None]
    uy = math.pi/y_max * u * y[:,None]
    sinuy = np.sin(uy)
    sinuz = np.sin(uz)
    C =  4.0 / (n-1.0)**2 * np.sum(np.sum((B * sinuy[:,:,None])[:,None] * sinuz[:,None],-1),-1)
    l = math.pi**2 * ((u**2 / y_max)[:,None] + (u**2 / z_max))
    l[0,0] = 1.0
    r = np.sqrt(l - alpha**2)

    sincos = sinuy[:,None,:,None] * (u * np.cos(uz))[None,:,None,:] 
    cossin = (u * np.cos(uy))[:,None,:,None] * sinuz[None,:,None,:]
    exprx = np.exp((-r * x[:,None,None]))
    temp_x = C * sinuy[:,None,:,None] * sinuz[None,:,None,:]
    Cl = C / l
    temp_y = Cl * (alpha * math.pi / z_max * sincos - r * math.pi / y_max * cossin)
    temp_z = Cl * (alpha * math.pi / y_max * cossin + r * math.pi / z_max * sincos)

    Bx = np.sum(np.sum(temp_x * exprx[:,None,None],-1),-1)
    By = np.sum(np.sum(temp_y * exprx[:,None,None],-1),-1)
    Bz = np.sum(np.sum(temp_z * exprx[:,None,None],-1),-1)
    return (Bx, By, Bz)

def main():

    B = util.Benchmark()

    sd = { 512:1, 256:2, 128:4, 64:8, 32:16, 16:32}
    try:
        h = sd[B.size[0]]
        w = sd[B.size[1]]
    except KeyError:
        raise ValueError('Only valid sizes are: '+str(sd.keys()))
    if B.inputfn:
        B_x0 = npf.loadtxt(B.inputfn, dtype=B.dtype)[::h,::w]
    else: 
         B_x0 = npf.loadtxt('../idl_data.txt',dtype=B.dtype)[::h,::w]
    B_x0 = np.array(B_x0)
    B.start()
    B_x0 = window(B_x0)
    R = calcB(B_x0)
    B.stop()
    B.pprint()

    if B.outputfn:
        B.tofile(B.outputfn, {'res':R})

    
if __name__ == '__main__':
    main()