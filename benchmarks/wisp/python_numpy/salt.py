# -*- coding: utf-8 -*-
"""
Created on Wed Dec 17 19:33:44 2014

@author: Rasmus Nordfang
"""

#from __future__ import division
import numpy as np
import time as time

def salt(S, p, h, x_ice, I_export, dV_dt):
    '''function that calculates the new salinity level
    INPUT
    S - Salinity [g/kg]
    p - density  [kg/m]
    x_ice - percent ice cover []
    I_export - Yearly Ice removel [m]
    dV/dt - ice growth [m/s]

    OUTPUT
    dS/dt [g/(kg*s)]
    '''
    [NL, NW, layers] = S.shape


    p_ice = 910 #[kg/m^3] density ice
    k_s = np.array([[0, 10**(-4),   10**(-6), 10**(-8)],    #ice ML-PC, PC-DP, DP-AB
                    [0, 6*10**(-4), 10**(-6), 10**(-8)]])   #no ice ML-PC, PC-DP, DP-AB

    #combine both with and without ice
    k_tot = k_s[None,0,:] * x_ice[:,:,None] + (1 - x_ice[:,:,None]) * k_s[None,1,:]


    #Mixing paramters in the horizontal plane NOT CORRECT
    k_horiz = np.array([10**(-3), 10**(-3), 10**(-3), 10**(-3)])


    W_brine = np.zeros(shape=(NL, NW))
    W_melt = np.zeros(shape=(NL, NW))


    #np.putmask(W_brine[:,:], dV_dt[:,:] > 0, p_ice * 34 * dV_dt[:,:] / (1- 34/1000))
    putmask = dV_dt[:,:] > 0
    W_brine[:,:] = ~putmask * W_brine[:,:] + putmask *(p_ice * 34 * dV_dt[:,:] / (1- 34/1000))
    #np.putmask(W_melt[:,:], dV_dt[:,:] <= 0, p_ice * 34 * dV_dt[:,:] / (1- 34/1000))
    putmask = dV_dt[:,:] <= 0
    W_melt[:,:] = ~putmask * W_melt[:,:] + putmask *(p_ice * 34 * dV_dt[:,:] / (1- 34/1000))

    W_int = np.zeros(shape=(NL,NW,layers)) #[kg * m/s * g/kg]

    W_int[:,:,1] = 2 * k_tot[:,:,1] * (p[:,:,0] * S[:,:,0] - p[:,:,1] * S[:,:,1]) / (h[0] + h[1]) #ML- PC
    W_int[:,:,2] = 2 * k_tot[:,:,2] * (p[:,:,1] * S[:,:,1] - p[:,:,2] * S[:,:,2]) / (h[1] + h[2]) #PC - DP
    W_int[:,:,3] = 2 * k_tot[:,:,3] * (p[:,:,2] * S[:,:,2] - p[:,:,3] * S[:,:,3]) / (h[2] + h[3]) #DP - AB


    #Salt diffusion from neighbors in 'Lenght' direction
    W_int_L = np.zeros(shape=(NL+1, NW, layers)) #[kg * m/s * g/kg]
    W_int_L[1:NL,:,:] = k_horiz[:] * (p[0:NL-1,:,:] * S[0:NL-1,:,:] - p[1:NL,:,:] * S[1:NL,:,:]) / (h[:])

    #Salt diffusion from neighbors in 'Width' direction
    W_int_W = np.zeros(shape=(NL, NW+1, layers)) #[kg * m/s * g/kg]
    W_int_W[:,1:NW,:] = k_horiz[:] * (p[:,0:NW-1,:] * S[:,0:NW-1,:] - p[:,1:NW,:] * S[:,1:NW,:]) / (h[:])

    #combined diffusion nearest neighbor. Can be put together at W_tot instead
    W_int_LW = W_int_L[0:NL,:,:] - W_int_L[1:NL+1,:,:] + W_int_W[:,0:NW,:] - W_int_W[:,1:NW+1,:]


    #Salt diffusion from diagonal neighboors. The mixing coeffecient is probably not correct
    W_int_dia_L = np.zeros(shape=(NL+1, NW+1, layers))
    W_int_dia_L[1:NL, 1:NW,:] =  k_horiz[:] * (p[0:NL-1, 0:NW-1,:] * S[0:NL-1, 0:NW-1,:] - p[1:NL, 1:NW,:] * S[1:NL, 1:NW,:] ) / h[:] * 2**(0.5)

    W_int_dia_W = np.zeros(shape=(NL+1, NW+1,layers))
    W_int_dia_W[1:NL, 1:NW,:] = k_horiz[:] * (p[0:NL-1, 1:NW, :] * S[0:NL-1, 1:NW, :] - p[0:NL-1, 1:NW, :] * S[1:NL, 0:NW-1, :]) / h[:] * 2 ** (0.5)

    #Combined diffussion from all diagonal neighbors with a sqrt(2)
    W_int_dia_tot = -W_int_dia_L[1:NL+1,1:NW+1,:] -W_int_dia_W[1:NL+1,0:NW,:] + W_int_dia_L[0:NL, 0:NW,:] + W_int_dia_W[0:NL, 1:NW+1,:]



#    W_int_dL = np.zeros(shape=(NL + 1,NW + 1,layers))
#    W_int_dL[1:NL,1:NW,:] = k_horiz[:] * (p[0:NL-1,0:NW-1,:])

    W_export = p_ice * 34 * I_export / (1- 34/1000) / (60*60*24*365) #[kg*m/s g/kg] #pos

    W_tot = np.zeros(shape=(NL, NW, layers))


#    W_tot[:,:,0] =  -W_int[:,:,1] + W_melt + W_int_L[0:NL,:,0] - W_int_L[1:NL+1,:,0] + W_int_W[:,0:NW,0] - W_int_W[:,1:NW+1,0] + Q_int_dia_tot[:,:,0]
#    W_tot[:,:,1] =  -W_int[:,:,2] + W_int[:,:,1] + W_brine - 0.8 * W_export + W_int_L[0:NL,:,1] - W_int_L[1:NL+1,:,1] + W_int_W[:,0:NW,1] - W_int_W[:,1:NW+1,1]#PC
#    W_tot[:,:,2] =  -W_int[:,:,3] + W_int[:,:,2] - 0.2 * W_export + W_int_L[0:NL,:,2] - W_int_L[1:NL+1,:,2] + W_int_W[:,0:NW,2] - W_int_W[:,1:NW+1,2]#DP
#    W_tot[:,:,3] = +W_int[:,:,3] + + W_int_L[0:NL,:,3] - W_int_L[1:NL+1,:,3] + W_int_W[:,0:NW,3] - W_int_W[:,1:NW+1,3] #AB

    W_tot[:,:,0] =  -W_int[:,:,1] + W_melt + W_int_LW[:,:,0] + W_int_dia_tot[:,:,0]
    W_tot[:,:,1] =  -W_int[:,:,2] + W_int[:,:,1] + W_brine - 0.8 * W_export + W_int_LW[:,:,1] + W_int_dia_tot[:,:,1]#PC
    W_tot[:,:,2] =  -W_int[:,:,3] + W_int[:,:,2] - 0.2 * W_export + W_int_LW[:,:,2] + W_int_dia_tot[:,:,2]#DP
    W_tot[:,:,3] =  W_int[:,:,3] + W_int_LW[:,:,3] + W_int_dia_tot[:,:,3] #AB




#    print 'W_tot', W_tot[1:5]


    S = W_tot / (p * h) #[m/s * g/kg]

    return S


#Test

#T = np.array([[1,2,3],
#              [4,5,6],
#              [7,8,9])
