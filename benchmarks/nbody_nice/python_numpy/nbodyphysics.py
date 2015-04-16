#!/usr/bin/python
# -*- coding: utf-8 -*-

"""NBody in N^2 complexity
Note that we are using only Newtonian forces and do not consider relativity
Neither do we consider collisions between stars
Thus some of our stars will accelerate to speeds beyond c
This is done to keep the simulation simple enough for teaching purposes

All the work is done in the calc_force, move and random_galaxy functions.
To vectorize the code these are the functions to transform.
"""
import numpy
import numpy
from numpy import exp, arctan, sqrt, pi, cos, sin, sign
from numpy.random import random

G = 6.673e-11
solarmass=1.98892e30


def fill_diagonal(a, val):
    d,_ = a.shape   #This only makes sense for square matrices
    a.shape=d*d     #Flatten a without making a copy
    a[::d+1]=val    #Assign the diagonal values
    a.shape = (d,d) #Return a to its original shape 



def calc_force(a, b, dt):
    """Calculate forces between bodies
    F = ((G m_a m_b)/r^2)/((x_b-x_a)/r)
    """

    dx = b['x'] - a['x'][numpy.newaxis,:].T
    if a==b:
        fill_diagonal(dx,1.0)
    dy = b['y'] - a['y'][numpy.newaxis,:].T
    if a==b:
        fill_diagonal(dy,1.0)
    dz = b['z'] - a['z'][numpy.newaxis,:].T
    if a==b:
        fill_diagonal(dz,1.0)
    pm = b['m'] * a['m'][numpy.newaxis,:].T
    if a==b:
        fill_diagonal(pm,0.0)

    r = ( dx ** 2 + dy ** 2 + dz ** 2) ** 0.5

    #In the below calc of the the forces the force of a body upon itself
    #becomes nan and thus destroys the data
    
    Fx = G * pm / r ** 2 * (dx / r) 
    Fy = G * pm / r ** 2 * (dy / r) 
    Fz = G * pm / r ** 2 * (dz / r) 
    
    #The diagonal nan numbers must be removed so that the force from a body
    #upon itself is zero
    if a==b:
        fill_diagonal(Fx,0)
        fill_diagonal(Fy,0)
        fill_diagonal(Fz,0)

    a['vx'] += numpy.add.reduce(Fx, axis=1)/ a['m'] * dt
    a['vy'] += numpy.add.reduce(Fy, axis=1)/ a['m'] * dt
    a['vz'] += numpy.add.reduce(Fz, axis=1)/ a['m'] * dt

def move(solarsystem, asteroids, dt):
    """Move the bodies
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

def circlev(rx, ry, rz):
    r2=sqrt(rx*rx+ry*ry+rz*rz)
    numerator=(6.67e-11)*1e6*solarmass
    return sqrt(numerator/r2)

#def sign(x):
#    if x<0: return -1
#    if x>0: return 1
#    return 0


def random_system(
                  x_max,
                  y_max,
                  z_max,
                  n,
                  b
                  ):
    """Generate a galaxy of random bodies"""
    
    solarsystem = {}

    solarsystem['x'], solarsystem['y'], solarsystem['z'] = random(n), random(n), random(n)*.01
    dist = (1.0/sqrt(solarsystem['x']**2+solarsystem['y']**2+solarsystem['z']**2))-(0.8-random()*.1)
    solarsystem['x'] = x_max*solarsystem['x']*dist*sign(.5-random(n))
    solarsystem['y'] = y_max*solarsystem['y']*dist*sign(.5-random(n))
    solarsystem['z'] = z_max*solarsystem['z']*dist*sign(.5-random(n))
    magv = circlev(solarsystem['x'],solarsystem['y'], solarsystem['z'])
    
    absangle = arctan(abs(solarsystem['y']/solarsystem['x']))
    thetav= pi/2-absangle
    solarsystem['vx']   = -1*sign(solarsystem['y'])*cos(thetav)*magv
    solarsystem['vy']   = sign(solarsystem['x'])*sin(thetav)*magv
    solarsystem['vz']   = numpy.zeros(n)
    solarsystem['m']    = random(n)*solarmass*10+1e20;

    solarsystem['m'][0]= 1e6*solarmass
    solarsystem['x'][0]= 0
    solarsystem['y'][0]= 0
    solarsystem['z'][0]= 0
    solarsystem['vx'][0]= 0
    solarsystem['vy'][0]= 0
    solarsystem['vz'][0]= 0

    asteroids = {}
    asteroids['x'], asteroids['y'], asteroids['z'] = random(b), random(b), random(b)*.01
    dist = (1.0/sqrt(asteroids['x']**2+asteroids['y']**2+asteroids['z']**2))-(random()*.2)
    asteroids['x'] = x_max*asteroids['x']*dist*sign(.5-random(b))
    asteroids['y'] = y_max*asteroids['y']*dist*sign(.5-random(b))
    asteroids['z'] = z_max*asteroids['z']*dist*sign(.5-random(b))
    magv = circlev(asteroids['x'],asteroids['y'], asteroids['z'])
        
    absangle = arctan(abs(asteroids['y']/asteroids['x']))
    thetav= pi/2-absangle
    asteroids['vx']   = -1*sign(asteroids['y'])*cos(thetav)*magv
    asteroids['vy']   = sign(asteroids['x'])*sin(thetav)*magv
    asteroids['vz']   = 0
    asteroids['m']    = random(b)*solarmass*10+1e14;
    
    return solarsystem, asteroids


