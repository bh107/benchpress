#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Non-interactive command line front end to NBody implementation"""

import time
from nbodyphysics import move, random_system

def nbody_benchmark(bodies_list, time_step):
    """Run benchmark simulation without visualization"""

    x_max = 1e18
    y_max = 1e18
    z_max = 1e18
    dt = 1e12

    for bodies in bodies_list:
        solarsystem, asteroids = random_system(x_max, y_max, z_max, 10, bodies)
        start = time.time()
        for _ in range(time_step):
            move(solarsystem, asteroids, dt)
        stop = time.time()

        print 'Simulated ' + str(bodies) + ' bodies for ' \
            + str(time_step) + ' timesteps in ' + str(stop - start) \
            + ' seconds'


if __name__ == '__main__':
    nbody_benchmark([10000, 100000, 1000000], 10)
