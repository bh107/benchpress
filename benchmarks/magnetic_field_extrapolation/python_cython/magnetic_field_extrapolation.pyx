# This Python file uses the following encoding: utf-8
from benchpress import util
from libc.math cimport sin, cos, exp, M_PI
import numpy as np
cimport numpy as np
cimport cython

# The main array data type
T = np.float64
ctypedef np.float64_t T_t

def window(B,a=0.37):
    assert (len(B.shape) == 2)
    assert (B.shape[0] == B.shape[1])
    n = B.shape[0]
    wl = np.ones_like(B[0])
    b = int(np.ceil((a * (n-1) / 2)))
    wl[:b]  =  0.5 * (1 + np.cos(np.pi*(2 * np.arange(b) / (a * (n-1)) - 1)))
    wl[-b:] =  0.5 * (1 + np.cos(np.pi*(2 * np.arange(b-1,-1,-1) / (a * (n-1)) - 1)))
    wl *= wl
    w = np.sqrt(wl+wl[:,None])
    return B*w

@cython.boundscheck(False) # turn off bounds-checking
@cython.cdivision(True) # turn off division-by-zero checking
cdef calcB(np.ndarray B_x0, T_t alpha=0.0,
          T_t x_min = 0.0, T_t x_max = 0.25,
          T_t y_min = 0.0, T_t y_max = 1.0,
          T_t z_min = 0.0, T_t z_max = 1.0):
    cdef size_t i, j, k, m, q
    cdef size_t n = len(B_x0)
    cdef T_t [:] x = np.linspace(x_min, x_max, num=n, endpoint=False).astype(T, copy=False)
    cdef T_t [:] y = np.linspace(y_min, y_max, num=n).astype(T, copy=False)
    cdef T_t [:] z = np.linspace(z_min, z_max, num=n).astype(T, copy=False)
    cdef np.ndarray u = np.arange(n, dtype=T)

    # Making C
    cdef T_t [:, :] C = 4.0 / (n-1.0)**2 * np.sum(np.sum((B_x0 * np.sin(np.pi/y_max * u * y[:,None])[:,:,None])[:,None] * np.sin(np.pi/z_max * u * z[:,None])[:,None],-1),-1)
    cdef T_t [:, :] l = np.pi**2 * ((u[:]*u[:] / y_max)[:,None] + (u*u / z_max))
    l[0,0] = 1.0
    r_np = np.empty((n,n),dtype=T)
    cdef T_t [:, :] r = r_np
    for i in range(n):
        for j in range(n):
            r[i,j] = np.sqrt(l[i,j] - alpha**2)
    cdef T_t [:, :, :] exprx = np.exp((-r_np * x[:, None, None]))

    # Calculating B
    cdef T_t [:, :, :] Bx = np.empty((n,n,n), dtype=T)
    cdef T_t [:, :, :] By = np.empty((n,n,n), dtype=T)
    cdef T_t [:, :, :] Bz = np.empty((n,n,n), dtype=T)
    cdef T_t [:, :] temp_x = np.empty((n, n), dtype=T)
    cdef T_t [:, :] temp_y = np.empty((n, n), dtype=T)
    cdef T_t [:, :] temp_z = np.empty((n, n), dtype=T)
    cdef T_t sincos, cossin
    for i in range(n):
        for j in range(n):
            for k in range(n):
                Bx[k, i, j] = 0
                By[k, i, j] = 0
                Bz[k, i, j] = 0
                for m in range(n):
                    sincos = sin(M_PI * k * y[i] / y_max) * (m * cos(M_PI * m * z[j] / z_max))
                    cossin = (k * cos(M_PI * k * y[i] / y_max)) * (sin(M_PI * m * z[j] / z_max))
                    temp_x[k,m] = C[k,m] * (sin(M_PI * k * y[i] / y_max) * (sin(M_PI * m * z[j] / z_max)))
                    temp_y[k,m] = C[k,m] / l[k,m] * (alpha * M_PI / z_max * sincos - r[k,m] * M_PI / y_max * cossin)
                    temp_z[k,m] = C[k,m] / l[k,m] * (alpha * M_PI / y_max * cossin + r[k,m] * M_PI / z_max * sincos)
            for k in range(n):
                for m in range(n):
                    for q in range(n):
                        Bx[k, i, j] += temp_x[m, q] * exprx[k, m, q]
                        By[k, i, j] += temp_y[m, q] * exprx[k, m, q]
                        Bz[k, i, j] += temp_z[m, q] * exprx[k, m, q]
    return (Bx, By, Bz)


def main():
    B = util.Benchmark()
    assert B.dtype == T
    if B.inputfn is None:
        B_x0 = B.random_array((B.size[0],B.size[1]), dtype=T)
    else:
        inputfn = B.inputfn if B.inputfn else '../idl_input-float64_512*512.npz'
        sd = { 512:1, 256:2, 128:4, 64:8, 32:16, 16:32, 8:64}
        try:
            h = sd[B.size[0]]
            w = sd[B.size[1]]
        except KeyError:
            raise ValueError('Only valid sizes are: '+str(sd.keys()))
        B_x0 = B.load_array(inputfn, 'input', dtype=T)[::h,::w]

    B.start()
    for _ in range(B.size[2]):
        calcB(window(B_x0.copy()))
    B.stop()
    B.pprint()

if __name__ == '__main__':
    main()
