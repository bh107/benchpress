from __future__ import print_function
from benchpress import util
import numpy as np
import math
try:
    import numpy_force as npf
except ImportError:
    import numpy as npf

def model(N, B):
    """Construct pseudo-data representing price samples?"""
    # Create the outside of bohrium
    S = npf.random.random(N).astype(B.dtype)*4.0 + 58.0 # Price is between 58-62
    S = np.array(S)
    return S

def CND(X):
    """
    Cumulative normal distribution.
    Helper function used by BS(...).
    """

    (a1,a2,a3,a4,a5) = (0.31938153, -0.356563782, 1.781477937, -1.821255978, 1.330274429)
    L = np.absolute(X)
    K = 1.0 / (1.0 + 0.2316419 * L)
    w = 1.0 - 1.0 / math.sqrt(2*np.pi)*np.exp(-L*L/2.) * \
        (a1 * K + \
         a2 * (K**2) + \
         a3 * (K**3) + \
         a4 * (K**4) + \
         a5 * (K**5))

    mask    = X<0
    w       = w * ~mask + (1.0-w)*mask

    return w

def BS(CallPutFlag, S, X, T, r, v):
    """Black Sholes Function."""

    d1 = (np.log(S/X)+(r+v*v/2.)*T)/(v*math.sqrt(T))
    d2 = d1-v*math.sqrt(T)
    if CallPutFlag=='c':
        return S*CND(d1)-X*math.exp(-r*T)*CND(d2)
    else:
        return X*math.exp(-r*T)*CND(-d2)-S*CND(-d1)

def price(S, I, flag='c', X=65.0, dT=(1.0/365.0), r=0.08, v=0.3, visualize=False):
    """Model price as a function of time."""

    T   = dT
    Ps  = []
    N   = len(S)
    for i in range (I):
        P = np.sum(BS(flag, S, X, T, r, v)) / N
        Ps.append(P)
        T += dT
        if visualize:   #NB: this is only for experiments
            np.visualize(P, "3d", 0, 0.0, 10)
        util.Benchmark().flush()

    return Ps

def main():
    B = util.Benchmark()
    (N, I) = B.size

    if B.inputfn:
        S = B.load_array()
    else:
        S = model(N, B)                     # Construct pseudo-data

    if B.dumpinput:
        B.dump_arrays("black_scholes", {'input': S})

    B.start()
    R = price(S, I, visualize=B.visualize)  # Run the model
    B.stop()
    B.pprint()

    for i in range(len(R)):                 # Convert to one array
        if hasattr(R[i], "copy2numpy"):
            R[i] = R[i].copy2numpy()[()]
    if B.outputfn:
        B.tofile(B.outputfn, {'res':R})

    if B.verbose:
        print (R)

if __name__ == "__main__":
    main()
