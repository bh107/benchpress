#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
NBody in N^2 complexity

Note that we are using only Newtonian forces and do not consider relativity
Neither do we consider collisions between stars
Thus some of our stars will accelerate to speeds beyond c
This is done to keep the simulation simple enough for teaching purposes

"""
from __future__ import print_function
from benchpress import util
import numpy as np
try:
    import numpy_force as npf
except ImportError:
    import numpy as npf


from nbody_nice_visualization import gfx_init, gfx_show

def fill_diagonal(a, val):
    d,_ = a.shape   # This only makes sense for square matrices
    a.shape=d*d     # Flatten a without making a copy
    a[::d+1]=val    # Assign the diagonal values
    a.shape = (d,d) # Return a to its original shape

def calc_force(a, b, dt):
    """
    Calculate forces between bodies
    F = ((G m_a m_b)/r^2)/((x_b-x_a)/r)
    """
    # Ignore division by zero since we fix it explicitely by setting the diagonal in the forces arrays
    npf.seterr(divide='ignore',invalid='ignore')

    G = 6.673e-11

    dx = b['x'] - a['x'][:,None]
    dy = b['y'] - a['y'][:,None]
    dz = b['z'] - a['z'][:,None]
    pm = b['m'] * a['m'][:,None]

    #
    # For some reason then this pow(T, 0.5) is deadly to performance...
    # sqrt(T) is equivalent math, trying it out instead.
    #
    # This might actually be a neat optimization:
    # pow(T, 0.K) => k-root(T)
    #
    #r = ( dx ** 2 + dy ** 2 + dz ** 2) ** 0.5
    r = np.sqrt( dx ** 2 + dy ** 2 + dz ** 2)

    Fx = G * pm / r ** 2 * (dx / r)
    Fy = G * pm / r ** 2 * (dy / r)
    Fz = G * pm / r ** 2 * (dz / r)

    # The diagonal nan numbers must be removed so that the force from a body
    # upon itself is zero
    if a is b:
        fill_diagonal(Fx,0.)
        fill_diagonal(Fy,0.)
        fill_diagonal(Fz,0.)

    a['vx'] += np.add.reduce(Fx, axis=1)/ a['m'] * dt
    a['vy'] += np.add.reduce(Fy, axis=1)/ a['m'] * dt
    a['vz'] += np.add.reduce(Fz, axis=1)/ a['m'] * dt

def move(solarsystem, asteroids, dt):
    """
    Move the bodies
    first find forces and change velocity and then move positions
    """
    calc_force(solarsystem, solarsystem, dt)
    calc_force(asteroids, solarsystem, dt)
    solarsystem['x'] += solarsystem['vx'] * dt
    solarsystem['y'] += solarsystem['vy'] * dt
    solarsystem['z'] += solarsystem['vz'] * dt

    asteroids['x'] += asteroids['vx'] * dt
    asteroids['y'] += asteroids['vy'] * dt
    asteroids['z'] += asteroids['vz'] * dt

def random_system(x_max, y_max, z_max, n, b, dtype=npf.float):
    """Generate a galaxy of random bodies"""

    solarmass=1.98892e30

    def circlev(rx, ry, rz):
        """Helper function..."""
        r2=npf.sqrt(rx*rx+ry*ry+rz*rz)
        numerator=(6.67e-11)*1e6*solarmass
        return npf.sqrt(numerator/r2)

    solarsystem = {}

    solarsystem['x'] = npf.random.random(n)
    solarsystem['y'] = npf.random.random(n)
    solarsystem['z'] = npf.random.random(n)*.01
    dist = (1.0/npf.sqrt(solarsystem['x']**2+solarsystem['y']**2+solarsystem['z']**2))-(0.8-npf.random.random()*.1)

    solarsystem['x'] = x_max*solarsystem['x']*dist*npf.sign(.5-npf.random.random(n))
    solarsystem['y'] = y_max*solarsystem['y']*dist*npf.sign(.5-npf.random.random(n))
    solarsystem['z'] = z_max*solarsystem['z']*dist*npf.sign(.5-npf.random.random(n))
    magv = circlev(
        solarsystem['x'],
        solarsystem['y'],
        solarsystem['z']
    )

    absangle = npf.arctan(npf.absolute(solarsystem['y']/solarsystem['x']))
    thetav= npf.pi/2-absangle
    solarsystem['vx']   = -1*npf.sign(solarsystem['y'])*npf.cos(thetav)*magv
    solarsystem['vy']   = npf.sign(solarsystem['x'])*npf.sin(thetav)*magv
    solarsystem['vz']   = npf.zeros(n)
    solarsystem['m']    = npf.random.random(n)*solarmass*10+1e20;

    solarsystem['m'][0]= 1e6*solarmass
    solarsystem['x'][0]= 0
    solarsystem['y'][0]= 0
    solarsystem['z'][0]= 0
    solarsystem['vx'][0]= 0
    solarsystem['vy'][0]= 0
    solarsystem['vz'][0]= 0

    asteroids = {}
    asteroids['x'] = npf.random.random(b)
    asteroids['y'] = npf.random.random(b)
    asteroids['z'] = npf.random.random(b)*.01
    dist = (1.0/npf.sqrt(asteroids['x']**2 + asteroids['y']**2 + asteroids['z']**2))-(npf.random.random()*.2)
    asteroids['x'] = x_max*asteroids['x']*dist*npf.sign(.5-npf.random.random(b))
    asteroids['y'] = y_max*asteroids['y']*dist*npf.sign(.5-npf.random.random(b))
    asteroids['z'] = z_max*asteroids['z']*dist*npf.sign(.5-npf.random.random(b))
    magv = circlev(
        asteroids['x'],
        asteroids['y'],
        asteroids['z']
    )

    absangle = npf.arctan(npf.absolute(asteroids['y'] / asteroids['x']))
    thetav= npf.pi/2-absangle
    asteroids['vx']   = -1*npf.sign(asteroids['y'])*npf.cos(thetav)*magv
    asteroids['vy']   = npf.sign(asteroids['x'])*npf.sin(thetav)*magv
    asteroids['vz']   = npf.zeros(b)
    asteroids['m']    = npf.random.random(b)*solarmass*10+1e14;

    ss = {}
    for key in solarsystem:
        ss[key] = np.array(solarsystem[key].astype(dtype))
    a = {}
    for key in asteroids:
        a[key] = np.array(asteroids[key].astype(dtype))

    return ss, a

def main():
    B = util.Benchmark()                            # Initialize Benchpress
    nplanets, nbodies, timesteps = B.size           # Grab arguments

    x_max = 1e18                                    # Simulation constants
    y_max = 1e18
    z_max = 1e18
    dt = 1e12

    solarsystem, asteroids = random_system(         # Setup galaxy
        x_max,
        y_max,
        z_max,
        nplanets,
        nbodies,
        B.dtype
    )

    if B.visualize:                                     # Init visuals
        plt, P3 = gfx_init(x_max, y_max, z_max)

    B.start()                                           # Timer start
    for timestep in range(0, timesteps):               # Run simulation
        if B.visualize and timestep % 10 == 0:          # With or without..
            gfx_show(plt, P3, solarsystem, asteroids)   # ..visuals
        move(solarsystem, asteroids, dt)
        util.Benchmark().flush()
    B.stop()                                            # Timer stop

    B.pprint()                                          # Print results..
    if B.verbose:                                       # ..and more.
        print(R)
    if B.visualize:                                     # Keep showing visuals
        plt.show(block=True)

if __name__ == "__main__":
    main()
