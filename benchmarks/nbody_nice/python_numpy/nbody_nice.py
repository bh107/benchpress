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

    G = 6.673e-11

    dx = b['x'] - a['x'][np.newaxis,:].T
    dy = b['y'] - a['y'][np.newaxis,:].T
    dz = b['z'] - a['z'][np.newaxis,:].T
    pm = b['m'] * a['m'][np.newaxis,:].T

    if a is b:
        fill_diagonal(dx,1.0)
        fill_diagonal(dy,1.0)
        fill_diagonal(dz,1.0)
        fill_diagonal(pm,0.0)

    r = ( dx ** 2 + dy ** 2 + dz ** 2) ** 0.5

    # In the below calc of the the forces the force of a body upon itself
    # becomes nan and thus destroys the data
    
    Fx = G * pm / r ** 2 * (dx / r) 
    Fy = G * pm / r ** 2 * (dy / r) 
    Fz = G * pm / r ** 2 * (dz / r) 
    
    # The diagonal nan numbers must be removed so that the force from a body
    # upon itself is zero
    if a is b:
        fill_diagonal(Fx,0)
        fill_diagonal(Fy,0)
        fill_diagonal(Fz,0)

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

def random_system(x_max, y_max, z_max, n, b):
    """Generate a galaxy of random bodies"""

    solarmass=1.98892e30

    def circlev(rx, ry, rz):
        """Helper function..."""
        r2=np.sqrt(rx*rx+ry*ry+rz*rz)
        numerator=(6.67e-11)*1e6*solarmass
        return np.sqrt(numerator/r2)

    solarsystem = {}

    solarsystem['x'] = np.random.random(n)
    solarsystem['y'] = np.random.random(n)
    solarsystem['z'] = np.random.random(n)*.01
    dist = (1.0/np.sqrt(solarsystem['x']**2+solarsystem['y']**2+solarsystem['z']**2))-(0.8-np.random.random()*.1)

    solarsystem['x'] = x_max*solarsystem['x']*dist*np.sign(.5-np.random.random(n))
    solarsystem['y'] = y_max*solarsystem['y']*dist*np.sign(.5-np.random.random(n))
    solarsystem['z'] = z_max*solarsystem['z']*dist*np.sign(.5-np.random.random(n))
    magv = circlev(
        solarsystem['x'],
        solarsystem['y'],
        solarsystem['z']
    )
    
    absangle = np.arctan(np.absolute(solarsystem['y']/solarsystem['x']))
    thetav= np.pi/2-absangle
    solarsystem['vx']   = -1*np.sign(solarsystem['y'])*np.cos(thetav)*magv
    solarsystem['vy']   = np.sign(solarsystem['x'])*np.sin(thetav)*magv
    solarsystem['vz']   = np.zeros(n)
    solarsystem['m']    = np.random.random(n)*solarmass*10+1e20;

    solarsystem['m'][0]= 1e6*solarmass
    solarsystem['x'][0]= 0
    solarsystem['y'][0]= 0
    solarsystem['z'][0]= 0
    solarsystem['vx'][0]= 0
    solarsystem['vy'][0]= 0
    solarsystem['vz'][0]= 0

    asteroids = {}
    asteroids['x'] = np.random.random(b)
    asteroids['y'] = np.random.random(b)
    asteroids['z'] = np.random.random(b)*.01
    dist = (1.0/np.sqrt(asteroids['x']**2 + asteroids['y']**2 + asteroids['z']**2))-(np.random.random()*.2)
    asteroids['x'] = x_max*asteroids['x']*dist*np.sign(.5-np.random.random(b))
    asteroids['y'] = y_max*asteroids['y']*dist*np.sign(.5-np.random.random(b))
    asteroids['z'] = z_max*asteroids['z']*dist*np.sign(.5-np.random.random(b))
    magv = circlev(
        asteroids['x'],
        asteroids['y'],
        asteroids['z']
    )
        
    absangle = np.arctan(np.absolute(asteroids['y'] / asteroids['x']))
    thetav= np.pi/2-absangle
    asteroids['vx']   = -1*np.sign(asteroids['y'])*np.cos(thetav)*magv
    asteroids['vy']   = np.sign(asteroids['x'])*np.sin(thetav)*magv
    asteroids['vz']   = 0
    asteroids['m']    = np.random.random(b)*solarmass*10+1e14;
    
    return solarsystem, asteroids

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
        nbodies
    )

    if B.visualize:                                     # Init visuals
        plt, P3 = gfx_init(x_max, y_max, z_max)

    B.start()                                           # Timer start
    for timestep in xrange(0, timesteps):               # Run simulation
        if B.visualize and timestep % 10 == 0:          # With or without..
            gfx_show(plt, P3, solarsystem, asteroids)   # ..visuals
        move(solarsystem, asteroids, dt)
    B.stop()                                            # Timer stop

    B.pprint()                                          # Print results..
    if B.verbose:                                       # ..and more.
        print(R)
    if B.visualize:                                     # Keep showing visuals
        plt.show(block=True)

if __name__ == "__main__":
    main()
