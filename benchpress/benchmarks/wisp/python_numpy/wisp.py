# -*- coding: utf-8 -*-
"""
Created on Thu Nov 20 10:47:25 2014
GPL

@author: Rasmus Nordfang
"""

from benchpress.benchmarks import util
import numpy as np
from salt import salt
from temp import temp
from density_imr import dens
from heat_imr import heatcap

bench = util.Benchmark("Wisp", "length*width*steps")

length = 1  # size of the grid unit m
width = 1  # size of the grid unit m

N_L = bench.args.size[0]  # number of grids in Length direction
N_W = bench.args.size[1]  # number of grids in width direction

n_years = 10  # number of years
# parameters

# Generel Start Values
# temp,[C]     density[kg/m^3],  depth,[m]      mass[kg]        Salinity[g/kg]
T_ML = -4;
p_ML = 10;
h_ML = 50;
m_ML = 3000;
S_ML = 33.0  # Mixed Layer
T_PC = 0.1;
p_PC = 20;
h_PC = 350;
m_PC = 2000;
S_PC = 34.5  # PycoCline
T_DP = 5.0;
p_DP = 30;
h_DP = 800;
m_DP = 1000;
S_DP = 32.0  # DeeP atlantic layer
T_AB = 2.0;
p_AB = 40;
h_AB = 3000;
m_AB = 8000;
S_AB = 35.0  # AByssal Layer

T_start = np.array([T_ML, T_PC, T_DP, T_AB])  # temperature
p_start = np.array([p_ML, p_PC, p_DP, p_AB])  # density
m_start = np.array([m_ML, m_PC, m_DP, m_AB])  # mass of layer
S_start = np.array([S_ML, S_PC, S_DP, S_AB])  # Salinity of layer
h = np.array([h_ML, h_PC, h_DP, h_AB])  # depth

hight = np.array([50, 300, 400, 1800])  # [m]

Volume = np.array(length * width * hight)  # [m^3]

pres = np.array([60.4, 360, 814, 3030])  # [kg/m^3] general pressure

# time
year = 60 * 60 * 24 * 365  # [s] seconds a year
dt = year / 200  # [s] Generel time stepsize
dt_top = year / 20  # [s] time stepsize for top layers

dt_temp = dt_top / dt  # fraction between generel stepsize and top stepsize
time = n_years * year  # [s] total time
steps = int(time / dt)  # [] number of timesteps

steps = bench.args.size[2]

# define a total matrix for all timesteps. With big calculations (I should maybe save them differently)
T = np.ones(shape=(steps + 1, N_L, N_W, 4));
T[0, :, :, :] = T_start
p = np.ones(shape=(steps + 1, N_L, N_W, 4));
m = np.ones(shape=(steps + 1, N_L, N_W, 4));
m[0, :, :, :] = m_start
S = np.ones(shape=(steps + 1, N_L, N_W, 4));
S[0, :, :, :] = S_start
c_w = np.ones(shape=(steps + 1, N_L, N_W, 4));  # [J / (K * kg)] water specefic heat

V = np.zeros(shape=(steps + 1, N_L, N_W));
V[0, :, :] = 2.0  # [m^3] Ice volume

h_ice = np.ones(shape=(steps + 1, N_L, N_W));  # [m] ice height
x_ice = np.ones(shape=(steps + 1, N_L, N_W));  # percentage ice cover

I_export = 0  # [m^3] volume of ice exportet away

bench.start()
for i in range(steps):  # Forward euler
    h_ice[i, :, :] = V[i, :, :]  # if V > 0.5 -> h_ice = V and h_ice = 1
    putmask = V[i, :, :] <= 0.5

    h_ice[i, :, :] = ~putmask * h_ice[i, :, :] + putmask * (V[i, :, :] ** 0.5 / 2.0)
    x_ice[i, :, :] = ~putmask * x_ice[i, :, :] + putmask * (2 * h_ice[i, :, :])

    if i % dt_temp == 0:
        p[i, :, :, :] = dens(S[i, :, :, :], T[i, :, :, :], pres[:])  # [kg/m]   (3d [kg/m^3])
        c_w[i, :, :, :] = heatcap(S[i, :, :, :], T[i, :, :, :], pres[:])  # [J/(kg*C)]
        m[i, :, :, :] = hight[:] * p[i, :, :, :]  # [kg]
        [dT, dV] = temp(T[i, :, :, :], p[i, :, :, :], h, m[i, :, :, :], c_w[i, :, :, :], x_ice[i, :, :],
                        0 if i < (0.5 * year / dt) else 1, h_ice[i, :, :], I_export)

        T[i + 1:i + 1 + dt_temp, :, :, :] = T[i, :, :, :] + dt * dT[:, :, :]
        V[i + 1:i + 1 + dt_temp, :, :] = V[i, :, :] + dt * dV[:, :]
        S[i + 1:i + 1 + dt_temp, :, :, :] = salt(S[i, :, :, :], p[i, :, :, :], h, x_ice[i, :, :], I_export,
                                                 dV / dt) * dt + S[i, :, :, :]

    else:
        p[i, :, :, 0] = dens(S[i, :, :, 0], T[i, :, :, 0], pres[0])
        p[i, :, :, 1] = dens(S[i, :, :, 1], T[i, :, :, 1], pres[1])
        c_w[i, :, :, 0] = heatcap(S[i, :, :, 0], T[i, :, :, 0], pres[0])  # [J/(kg*C)]
        c_w[i, :, :, 1] = heatcap(S[i, :, :, 1], T[i, :, :, 1], pres[1])  # [J/(kg*C)]

        m[i, :, :, 0:2] = hight[0:2] * p[i, :, :, 0:2]  # [kg]

        # all layers
        [dT, dV] = temp(T[i, :, :, :], p[i, :, :, :], h, m[i, :, :, :], c_w[i, :, :, :], x_ice[i, :, :],
                        0 if i < (0.5 * year / dt) else 1, h_ice[i, :, :], I_export)
        T[i + 1, :, :, 0] = dT[:, :, 0] * dt + T[i, :, :, 0]
        V[i + 1, :, :] = dV[:, :] * dt + V[i, :, :]

        dS = salt(S[i, :, :, :], p[i, :, :, :], h, x_ice[i, :, :], I_export, dV / dt)
        S[i + 1, :, :, 0] = dS[:, :, 0] * dt + S[i, :, :, 0]

    I_export = 14.22

bench.stop()
bench.pprint()
