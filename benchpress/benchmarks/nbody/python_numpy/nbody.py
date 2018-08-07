from __future__ import print_function

"""
NBody in N^2 complexity

Note that we are using only Newtonian forces and do not consider relativity
Neither do we consider collisions between stars
Thus some of our stars will accelerate to speeds beyond c
This is done to keep the simulation simple enough for teaching purposes

All the work is done in the calc_force, move and random_galaxy functions.
To vectorize the code these are the functions to transform.
"""
from benchpress.benchmarks import util
import numpy as np

bench = util.Benchmark("Gaussian elimination on matrix a without pivoting", "<size>")

G = 6.67384e-11  # m/(kg*s^2)
dt = 60 * 60 * 24 * 365.25  # Years in seconds
r_ly = 9.4607e15  # Lightyear in m
m_sol = 1.9891e30  # Solar mass in kg


def diagonal(ary, offset=0):
    if ary.ndim != 2:
        raise Exception("diagonal only supports 2 dimensions\n")
    if offset < 0:
        offset = -offset
        if (ary.shape[0] - offset) > ary.shape[1]:
            ary_diag = ary[offset, :]
        else:
            ary_diag = ary[offset:, 0]
    else:
        if ary.shape[1] - offset > ary.shape[0]:
            ary_diag = ary[:, offset]
        else:
            ary_diag = ary[0, offset:]
    ary_diag.strides = (ary.strides[0] + ary.strides[1],)
    return ary_diag


def random_galaxy(N):
    """Generate a galaxy of random bodies"""

    galaxy = {  # We let all bodies stand still initially
        'm': (bench.random_array((N,)) + 10) * m_sol / 10,
        'x': (bench.random_array((N,)) - 0.5) * r_ly / 100,
        'y': (bench.random_array((N,)) - 0.5) * r_ly / 100,
        'z': (bench.random_array((N,)) - 0.5) * r_ly / 100,
        'vx': np.zeros(N, dtype=bench.dtype),
        'vy': np.zeros(N, dtype=bench.dtype),
        'vz': np.zeros(N, dtype=bench.dtype)
    }
    if bench.dtype == np.float32:
        galaxy['m'] /= 1e10
        galaxy['x'] /= 1e5
        galaxy['y'] /= 1e5
        galaxy['z'] /= 1e5
    return galaxy


def move(galaxy, dt):
    """Move the bodies
    first find forces and change velocity and then move positions
    """
    n = len(galaxy['x'])
    # Calculate all dictances component wise (with sign)
    dx = galaxy['x'][np.newaxis, :].T - galaxy['x']
    dy = galaxy['y'][np.newaxis, :].T - galaxy['y']
    dz = galaxy['z'][np.newaxis, :].T - galaxy['z']

    # Euclidian distances (all bodys)
    r = np.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
    diagonal(r)[:] = 1.0

    # prevent collision
    mask = r < 1.0
    r = r * ~mask + 1.0 * mask

    m = galaxy['m'][np.newaxis, :].T

    # Calculate the acceleration component wise
    Fx = G * m * dx / r ** 3
    Fy = G * m * dy / r ** 3
    Fz = G * m * dz / r ** 3
    # Set the force (acceleration) a body exerts on it self to zero
    diagonal(Fx)[:] = 0.0
    diagonal(Fy)[:] = 0.0
    diagonal(Fz)[:] = 0.0

    galaxy['vx'] += dt * np.sum(Fx, axis=0)
    galaxy['vy'] += dt * np.sum(Fy, axis=0)
    galaxy['vz'] += dt * np.sum(Fz, axis=0)

    galaxy['x'] += dt * galaxy['vx']
    galaxy['y'] += dt * galaxy['vy']
    galaxy['z'] += dt * galaxy['vz']


def main():
    nbodies, niters = bench.args.size
    galaxy = random_galaxy(nbodies)

    bench.start()
    for i in range(niters):
        move(galaxy, dt)
        bench.flush()
    bench.stop()
    bench.pprint()


if __name__ == "__main__":
    main()
