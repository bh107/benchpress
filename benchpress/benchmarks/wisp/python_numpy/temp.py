# -*- coding: utf-8 -*-
"""
Created on Wed Dec 17 20:09:02 2014

@author: Rasmus Nordfang
"""
#from __future__ import division
import numpy as np
import time as time

#NOTER ang. mulige fejl
'''
NOTER
c_w er nok en konstant og/eller tager muligvis fra det forkerte lag


'''



def temp(T, p, h, m, c_w, x_ice,season, h_ice, I_export):
    '''
    INPUT
    T - temperature [°C]
    p - density     [kg/m]
    h - layer depth [m]
    c_w - specific heat capacity [J / (K * kg)]
    x_ice - ice parameter. [] number between 0 and 1
    season [0 winter, 1 summer]
    h_ice [m]
    I_export [m] Ice export factor

    OUTPUT
    T (dT/dt) [C/s]
    V (dV/dt) [m/s]
    '''

    [NL, NW, layers] = T.shape
    #PARAMATERS

    #OHFC paramaters
    Q_tot_NoIce = 3 #Unit W/m^2 look at page 4343 middle
    Q_tot_Ice = 0.5 #Unit W/m^2
    A = 320 #[W/m^2]
    B = 4.6 #[w/m^2]
    D = 90 #[W/m^2]
    T_ref = -1.8 #[C] minimum temp for ML layer
    T_bot = -1.8 #[C] ice temp bottom ice present winter eq. 3 Singh
    B_t = 5.0 #[w/(m^2 * C)]
    n_w = 2.5
    n_s = 2.8
    k_c = 2.0 #[w/(m * C)] thermal conductivity of ice
    C_0 = 20 #[W/(m^2 * C)]
    p_ice = 910 #[kg/m] density ice
    L_f = 297000 #[J/kg] #heat of fusion for seawater. Taken as constant S=4 [0/00] T = -1.8 [C]

    #mixing parameters #Unit m^2/s
    k_t = np.array([[0, 10**(-4),   10**(-5), 10**(-7)],    #ice ML-PC, PC-DP, DP-AB
                    [0, 6*10**(-4), 10**(-5), 10**(-7)]])   #no ice ML-PC, PC-DP, DP-AB

    #combine both with and without ice
    k_tot = k_t[None,0,:] * x_ice[:,:,None] + (1 - x_ice[:,:,None]) * k_t[None,1,:]

    #mixing paramters horizontal
    k_horiz = np.array([10**(-4), 10**(-1), 10**(-1), 10**(-1)])


    T_top = (x_ice > 0) * (1 / (B/n_w + k_c / h_ice[:,:]) * (k_c * T_bot / h_ice[:,:] - A / n_w + D / 2 ))

#    tid3 = time.time()
#    print k_tot3 - k_tot


    Q_trans = np.zeros(shape=(NL, NW, layers)) #[W/m^2]                          #Ice layer
    Q_trans[:,:,0] = (1 - x_ice) * 2/3 * Q_tot_NoIce  #ML
    Q_trans[:,:,1] = (1 - x_ice) * 1/3 * Q_tot_NoIce  #PC
    Q_trans[:,:,2] = Q_tot_Ice * x_ice                #DP
    Q_trans[:,:,3] = 0                                #AB


    Q_int = np.zeros(shape=(NL, NW, layers))
    Q_int[:,:,0] = C_0 * (T[:,:,0] - T_bot) #ice - ML
    Q_int[:,:,1] = 2 * k_tot[:,:,1] * c_w[:,:,1] * (p[:,:,0] * T[:,:,0] - p[:,:,1] * T[:,:,1]) / (h[0] + h[1]) #ML- PC
    Q_int[:,:,2] = 2 * k_tot[:,:,2] * c_w[:,:,2] * (p[:,:,1] * T[:,:,1] - p[:,:,2] * T[:,:,2]) / (h[1] + h[2]) #PC - DP
    Q_int[:,:,3] = 2 * k_tot[:,:,3] * c_w[:,:,3] * (p[:,:,2] * T[:,:,2] - p[:,:,3] * T[:,:,3]) / (h[2] + h[3]) #DP - AB



    #Temperature diffusion from neighbors in 'Lenght' direction
    Q_int_L = np.zeros(shape=(NL+1, NW, layers)) #[kg * m/s * g/kg]
    Q_int_L[1:NL,:,:] = k_horiz[:] * (p[0:NL-1,:,:] * T[0:NL-1,:,:] - p[1:NL,:,:] * T[1:NL,:,:]) / (h[:])

    #Temperature diffusion from neighbors in 'Width' direction
    Q_int_W = np.zeros(shape=(NL, NW+1, layers)) #[kg * m/s * g/kg]
    Q_int_W[:,1:NW,:] = k_horiz[:] * (p[:,0:NW-1,:] * T[:,0:NW-1,:] - p[:,1:NW,:] * T[:,1:NW,:]) / (h[:])

    #combined diffusion nearest neighbor. Can be put together at W_tot instead
    Q_int_LW = Q_int_L[0:NL,:,:] - Q_int_L[1:NL+1,:,:] + Q_int_W[:,0:NW,:] - Q_int_W[:,1:NW+1,:]




    #Temperature diffusion from diagonal neighboors. The mixing coeffecient is probably not correct
    Q_int_dia_L = np.zeros(shape=(NL+1, NW+1, layers))
    Q_int_dia_L[1:NL, 1:NW,:] =  k_horiz[:] * (p[0:NL-1, 0:NW-1,:] * T[0:NL-1, 0:NW-1,:] - p[1:NL, 1:NW,:] * T[1:NL, 1:NW,:] ) / h[:]# * 2**(0.5)

    Q_int_dia_W = np.zeros(shape=(NL+1, NW+1,layers))
    Q_int_dia_W[1:NL, 1:NW,:] = k_horiz[:] * (p[0:NL-1, 1:NW, :] * T[0:NL-1, 1:NW, :] - p[0:NL-1, 1:NW, :] * T[1:NL, 0:NW-1, :]) / h[:]# * 2 ** (0.5)

    #Combined Temperature diffussion from all diagonal neighbors with a sqrt(2)
    Q_int_dia_tot = -Q_int_dia_L[1:NL+1,1:NW+1,:] -Q_int_dia_W[1:NL+1,0:NW,:] + Q_int_dia_L[0:NL, 0:NW,:] + Q_int_dia_W[0:NL, 1:NW+1,:]



    #Q for the ML layer
    Q_turb = B_t * (T[:,:,0] - T_ref) #[w/m^2]


    #Q_cond = k_c * (T_top - T_bot) / h_ice

    dp_ice = np.zeros(shape=(NL,NW))

    if season == 0: #winter
        Q_sw = 0 #[W/m^2]eq 18 Singh

        Q_lw = ((1 - x_ice) * ((A + B * T[:,:,0]) /  n_w - D / 2) #over open ocean winter
        + x_ice * ((A + B * T_top) / n_w - D/2)) #over sea ice winter eq 20 Singh

        putmask = h_ice >= 1
        dp_ice[:] = ~putmask * dp_ice + putmask * (2/(60*60*24*365)) #[m/s] int_(cold season) dp_ice dt = 1
#        if h_ice >= 1:
#            dp_ice = 2/(60*60*24*365) #[m/s] int_(cold season) dp_ice dt = 1
#        else:
#            dp_ice = 0
    else: #summer
        Q_sw = x_ice * 80 + (1 - x_ice) * 180 #eq 18 Singh

        Q_lw = ((1 - x_ice) * ((A + B * T[:,:,0]) /  n_s - D / 2) #open ocean summer
        + x_ice * (A / n_s - D / 2)) #sea ice summer eq 20 Singh
#        dp_ice = 0

    Q_tot=np.zeros(shape=(NL,NW,4)) #[w/m^2]
#    for k in range(2,5):
#        Q_tot[k] = Q_trans[k] + Q_int[k] - Q_int[k-1] #N3 should be moved outside the loop. BUT hoooooow


#    Q_tot[:,:,0] = (1 - x_ice) * (Q_sw - Q_lw - Q_turb) - x_ice * Q_int[:,:,0] - Q_int[:,:,1] + Q_trans[:,:,0] + Q_int_L[0:NL,:,0] - Q_int_L[1:NL+1,:,0] + Q_int_W[:,0:NW,0] - Q_int_W[:,1:NW+1,0] #ML
#    Q_tot[:,:,1] = Q_trans[:,:,1] - Q_int[:,:,2] + Q_int[:,:,1] + Q_int_L[0:NL,:,1] - Q_int_L[1:NL+1,:,1] + Q_int_W[:,0:NW,1] - Q_int_W[:,1:NW+1,1] #PC
#    Q_tot[:,:,2] = Q_trans[:,:,2] - Q_int[:,:,3] + Q_int[:,:,2] + Q_int_L[0:NL,:,2] - Q_int_L[1:NL+1,:,2] + Q_int_W[:,0:NW,2] - Q_int_W[:,1:NW+1,2]#DP
#    Q_tot[:,:,3] = Q_int[:,:,3] + Q_int_L[0:NL,:,3] - Q_int_L[1:NL+1,:,3] + Q_int_W[:,0:NW,3] - Q_int_W[:,1:NW+1,3]#AB
#
    Q_tot[:,:,0] = (1 - x_ice) * (Q_sw - Q_lw - Q_turb) - x_ice * Q_int[:,:,0] - Q_int[:,:,1] + Q_trans[:,:,0] + Q_int_LW[:,:,0] + Q_int_dia_tot[:,:,0]  #ML
    Q_tot[:,:,1] = Q_trans[:,:,1] - Q_int[:,:,2] + Q_int[:,:,1] + Q_int_LW[:,:,1] + Q_int_dia_tot[:,:,1]  #PC
    Q_tot[:,:,2] = Q_trans[:,:,2] - Q_int[:,:,3] + Q_int[:,:,2] + Q_int_LW[:,:,2] + Q_int_dia_tot[:,:,2] #DP
    Q_tot[:,:,3] = Q_int[:,:,3] + Q_int_LW[:,:,3] + Q_int_dia_tot[:,:,3]#AB



    T = Q_tot / (c_w * m)  #[C/s]

    #this unit does not make sense
#    print 'Først', x_ice * (Q_lw - Q_sw - Q_int[1]),'anden', p_ice * L_f * dp_ice,'Tredje', I_export

    V = ((x_ice * (Q_lw - Q_sw - Q_int[:,:,0]) + p_ice * L_f * dp_ice - I_export)) / (p_ice * L_f)# / (60*60*24*365)

#    V = ((x_ice * (Q_lw - Q_sw - Q_int[1]) - I_export) / (p_ice * L_f) )

#    print 'dV/dt', V
    return T, V

#test del
#T = np.array([1,2,3,4,4])
#p = np.array([10,9,8,7,6])
#h = np.array([200, 300, 400, 500, 600])
#m = np.array([100, 101, 102, 103, 104])
#c_w = 4000
#x_ice = 0.5
#season = 0
#h_ice = 1
#
#dt = temp(T,p,h,m,c_w,x_ice,season,h_ice)






