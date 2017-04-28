# --- encoding: iso-8859-1 ---

"""Seawater density module

dens(S, T[, P])   -- Density
svan(S, T[, P])   -- Specific volume anomaly
sigma(S, T[, P])  -- Density anomaly
drhodt(S, T[, P]) -- Temperature derivative of density
alpha(S, T[, P])  -- Thermal expansion coefficient
drhods(S, T[, P]) -- Salinity derivative of density
beta(S, T[, P])   -- Saline expansion coefficient

Bjørn Ådlandsvik <bjorn@imr.no>, 07 November 2004

"""

# -----------------------------------------------

def _dens0(S,T):
    """Density of seawater at zero pressure"""

    # --- Define constants ---
    a0 = 999.842594
    a1 =   6.793952e-2
    a2 =  -9.095290e-3
    a3 =   1.001685e-4
    a4 =  -1.120083e-6
    a5 =   6.536332e-9

    b0 =   8.24493e-1
    b1 =  -4.0899e-3
    b2 =   7.6438e-5
    b3 =  -8.2467e-7
    b4 =   5.3875e-9

    c0 =  -5.72466e-3
    c1 =   1.0227e-4
    c2 =  -1.6546e-6

    d0 =   4.8314e-4

    # --- Computations ---
    # Density of pure water
    SMOW = a0 + (a1 + (a2 + (a3 + (a4 + a5*T)*T)*T)*T)*T

    # More temperature polynomials
    RB = b0 + (b1 + (b2 + (b3 + b4*T)*T)*T)*T
    RC = c0 + (c1 + c2*T)*T
    
    return SMOW + RB*S + RC*(S**1.5) + d0*S*S 
       
# -----------------------------------------------------------------

def _seck(S, T, P=0):
    """Secant bulk modulus"""
  
    # --- Pure water terms ---

    h0 =  3.239908  
    h1 =  1.43713E-3
    h2 =  1.16092E-4
    h3 = -5.77905E-7
    AW = h0 + (h1 + (h2 + h3*T)*T)*T

    k0 =  8.50935E-5  
    k1 = -6.12293E-6
    k2 =  5.2787E-8
    BW = k0 + (k1 + k2*T)*T

    e0 = 19652.21
    e1 = 148.4206
    e2 = -2.327105
    e3 =  1.360477E-2
    e4 = -5.155288E-5
    KW = e0 + (e1 + (e2 + (e3 + e4*T)*T)*T)*T  

    # --- seawater, P = 0 ---

    SR = S**0.5

    i0 =  2.2838E-3
    i1 = -1.0981E-5
    i2 = -1.6078E-6
    j0 =  1.91075E-4
    A  = AW + (i0 + (i1 + i2*T)*T + j0*SR)*S 

    f0 = 54.6746
    f1 = -0.603459
    f2 =  1.09987E-2
    f3 = -6.1670E-5
    g0 =  7.944E-2
    g1 =  1.6483E-2
    g2 = -5.3009E-4
    K0 = KW + (f0 + (f1 + (f2 + f3*T)*T)*T  \
            + (g0 + (g1 + g2*T)*T)*SR)*S   

    # --- General expression ---
    
    m0 = -9.9348E-7
    m1 =  2.0816E-8
    m2 =  9.1697E-10
    B = BW + (m0 + (m1 + m2*T)*T)*S  

    K = K0 + (A + B*P)*P 

    return K
 
# ----------------------------------------------

def dens(S, T, P=0):
    """Compute density of seawater from salinity, temperature, and pressure

    Usage: dens(S, T, [P])
 
    Input:               
        S = Salinity,     [PSS-78]
        T = Temperature,  [°C]
        P = Pressure,     [dbar = 10**4 Pa]
    P is optional, with default value zero

    Output:
        Density,          [kg/m**3]
 
    Algorithm: UNESCO 1983

    """
    
    P = 0.1*P # Convert to bar
    return _dens0(S,T)/(1 - P/_seck(S,T,P))
# -------------------------------------------




### SALINITY FUNCTIONS #################################

## def _sal(XR,XT):
    
##     a0 =  0.0080
##     a1 = -0.1692
##     a2 = 25.3851
##     a3 = 14.0941
##     a4 = -7.0261
##     a5 =  2.7081
    
##     b0 =  0.0005
##     b1 = -0.0056
##     b2 = -0.0066
##     b3 = -0.0375
##     b4 =  0.0636
##     b5 = -0.0144
    
##     k  =  0.0162

##     DS = (XT / (1+k*XT) ) *        \
##          (b0 + (b1 + (b2 + (b3 + (b4 + b5*XR)*XR)*XR)*XR)*XR)

##     return a0 + (a1 + (a2 + (a3 + (a4 + a5*XR)*XR)*XR)*XR)*XR + DS

## # ---------------------------------------------------

## def _dsal(XR,XT):
    
##     a1 = -0.1692
##     a2 = 25.3851
##     a3 = 14.0941
##     a4 = -7.0261
##     a5 =  2.7081

##     b1 = -0.0056
##     b2 = -0.0066
##     b3 = -0.0375
##     b4 =  0.0636
##     b5 = -0.0144

##     k  =  0.0162
    
##     dDS = (XT / (1+k*XT) ) *      \
##           (b1 + (b2*2 + (b3*3 + (b4*4 + b5*5*XR)*XR)*XR)*XR)
    
##     return a1 + (a2*2 + (a3*3 + (a4*4 + a5*5*XR)*XR)*XR)*XR + dDS

## # ---------------------------------------------

## def _rt(T):
    
##     c0 =  0.6766097
##     c1 =  2.00564e-2
##     c2 =  1.104259e-4
##     c3 = -6.9698e-7
##     c4 =  1.0031e-9
    
##     return c0 + (c1 + (c2 + (c3 + c4*T)*T)*T)*T

## # ---------------------------------------------------

## def _c(P):
    
##     e1 =  2.070e-5
##     e2 = -6.370e-10
##     e3 =  3.989e-15
    
##     return (e1 + (e2 + e3*P)*P)*P

## # ---------------------------------------------------

## def _b(T):
    
##     d1 =  3.426e-2
##     d2 =  4.464e-4
    
##     return 1.0 + (d1 + d2*T)*T

## # ---------------------------------------------------

## def _a(T):
    
##     d3 =  4.215e-1
##     d4 = -3.107e-3    
##     return d3 + d4*T

