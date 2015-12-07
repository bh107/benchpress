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

    uz = math.pi/z_max * u * z[:,None]
    uy = math.pi/y_max * u * y[:,None]
    sinuy = np.sin(uy)
    sinuz = np.sin(uz)
    C =  4.0 / (n-1.0)**2 * np.sum(np.sum((B * sinuy[:,:,None])[:,None] * sinuz[:,None],-1),-1)
    l = math.pi**2 * ((u**2 / y_max)[:,None] + (u**2 / z_max))
    l[0,0] = 1.0
    r = np.sqrt(l - alpha**2)

    Bx = np.empty((n,n,n),dtype=B.dtype)
    By = np.empty((n,n,n),dtype=B.dtype)
    Bz = np.empty((n,n,n),dtype=B.dtype)
    
    exprx = np.exp((-r * x[:,None,None]))
    ucosuz = u * np.cos(uz)
    ucosuy = u * np.cos(uy)
    util.Benchmark().flush()
    for i in range(n):        
        temp_x = C * sinuy[i,:,None] * sinuz[:,None,:] 
        Bx[:,i,:] = np.sum(np.sum(temp_x * exprx[:,None],-1),-1)
        del temp_x
        util.Benchmark().flush()
    if util.Benchmark().bohrium:
        Bx = np.array(Bx,bohrium=False)

    for i in range(n):        
        sincos = sinuy[i,:,None] * ucosuz[:,None,:]
        cossin = ucosuy[i,:,None] * sinuz[:,None,:]
        temp_y = C/l * (alpha * math.pi / z_max * sincos - r * (math.pi / y_max) * cossin)
        del sincos
        del cossin
        By[:,i,:] = np.sum(np.sum(temp_y * exprx[:,None],-1),-1)
        del temp_y
        util.Benchmark().flush()
    if util.Benchmark().bohrium:
        By = np.array(By,bohrium=False)

    for i in range(n):        
        sincos = sinuy[i,:,None] * ucosuz[:,None,:]
        cossin = ucosuy[i,:,None] * sinuz[:,None,:]
        temp_z = C/l * (alpha * math.pi / y_max * cossin + r * (math.pi / z_max) * sincos)
        del sincos
        del cossin
        Bz[:,i,:] = np.sum(np.sum(temp_z * exprx[:,None],-1),-1)
        del temp_z
        util.Benchmark().flush()
    if util.Benchmark().bohrium:
        Bz = np.array(Bz,bohrium=False)

    return (Bx, By, Bz)

def main():

    B = util.Benchmark()

    sd = { 512:1, 256:2, 128:4, 64:8, 32:16, 16:32 }
    try:
        h = sd[B.size[0]]
        w = sd[B.size[1]]
    except KeyError:
        raise ValueError('Only valid sizes are: '+str(sd.keys()))

    inputfn = B.inputfn if B.inputfn else '../idl_input-float64_512*512.npz' 
    B_x0 = B.load_array(inputfn, 'input', dtype=B.dtype)[::h,::w]

    B.start()
    B_x0 = window(B_x0)
    Rx, Ry, Rz = calcB(B_x0)
    B.stop()
    B.pprint()

    if B.outputfn:
        R = Rx+Ry+Rz
        B.tofile(B.outputfn, {'res': R, 'res_x': Rx, 'res_y': Ry, 'res_z': Rz})
    
if __name__ == '__main__':
    main()
