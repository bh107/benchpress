#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Interactive visual front end to NBody implementation"""

import time

# Tell pylint that Axes3D import is required although never explicitly used

from mpl_toolkits.mplot3d import Axes3D  # pylint: disable=W0611
import matplotlib.pyplot as plt

from nbodyphysics import move, random_system


def gfx_init(xm, ym, zm):
    """Init plot"""

    plt.ion()
    fig = plt.figure()
    sub = fig.add_subplot(111, projection='3d')
    sub.xm = xm
    sub.ym = ym
    sub.zm = zm
    return sub


def show(sub, solarsystem, bodies):
    """Show plot"""
    #Sun
    sub.clear()

    sub.scatter(
                solarsystem['x'][0],
                solarsystem['y'][0],
                solarsystem['z'][0],
                s=100,
                marker='o',
                c='yellow',
            )
    #Planets
    sub.scatter(
                [solarsystem['x'][1:]],
                [solarsystem['y'][1:]],
                [solarsystem['z'][1:]],
                s=5,
                marker='o',
                c='blue',
        )


#Astoroids
    sub.scatter(
                [bodies['x']],
                [bodies['y']],
                [bodies['z']],
                s=.1,
                marker='.',
                c='green',
        )


    sub.set_xbound(-sub.xm, sub.xm)
    sub.set_ybound(-sub.ym, sub.ym)
    try:
        sub.set_zbound(-sub.zm, sub.zm)
    except AttributeError:
        print 'Warning: correct 3D plots may require matplotlib-1.1 or later'

    plt.draw()


def nbody_debug(n, bodies, time_step):
    """Run simulation with visualization"""

    x_max = 1e18
    y_max = 1e18
    z_max = 1e18
    
    solarsystem, astoroids = random_system(x_max, y_max, z_max, n, bodies)

    P3 = gfx_init(x_max, y_max, z_max)
    dt = 1e12



    start = time.time()
    for step in range(time_step):
        if step%1 == 0:
            show(P3, solarsystem, astoroids)
        move(solarsystem, astoroids, dt)
        print step
    stop = time.time()
    print 'Simulated ' + str(bodies) + ' bodies for ' + str(time_step) \
        + ' timesteps in ' + str(stop - start) + ' seconds'


if __name__ == '__main__':
    nbody_debug(10, 1000, 1000)

