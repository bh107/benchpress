#include <iostream>
#include <sstream>
#include <string>
#include <cmath>
#include <bp_util.h>

using namespace std;

// The cumulative normal distribution function 
double CND( double X )
{
    double L, K, w;

    double const a1 =  0.31938153,
                 a2 = -0.356563782,
                 a3 =  1.781477937,
                 a4 = -1.821255978,
                 a5 =  1.330274429;

    L = fabs(X);
    K = 1.0 / (1.0 + 0.2316419 * L);
    w = 1.0 - 1.0 / sqrt(2 * M_PI) * exp(-L *L / 2) * (\
        a1 * K         + \
        a2 * pow(K, 2) + \
        a3 * pow(K, 3) + \
        a4 * pow(K, 4) + \
        a5 * pow(K, 5)
    );

    if (X < 0 ){
        w = 1.0 - w;
    }
    return w;
}

// The Black and Scholes (1973) Stock option formula
double BlackScholes(char CallPutFlag, double S, double X, double T, double r, double v)
{
    double d1, d2;

    d1=(log(S/X)+(r+v*v/2)*T)/(v*sqrt(T));
    d2=d1-v*sqrt(T);

    if (CallPutFlag == 'c') {
        return S *CND(d1)-X * exp(-r*T)*CND(d2);
    } else {
        return X * exp(-r * T) * CND(-d2) - S * CND(-d1);
    }
}

int main(int argc, char* argv[])
{
    bp_util_type bp = bp_util_create(argc, argv, 2);
    if (bp.args.has_error) {
        return 1;
    }

    const int nelements = bp.args.sizes[0];
    double* array = new double[nelements];

    

    /*
    const int ydim = 1000;
    const int xdim = 1000;

    auto grid = new double[ydim][xdim];
    */
    bp.timer_start();

    /*
    cout << "Whatever" << argc << " " << argv[0] << endl;

    cout << "Address " << &(grid[0][0]) << endl;
    cout << "Address " << &(grid[0]) << endl;;
    cout << "Address " << &(*grid) << endl;;
    */

    bp.timer_stop();
    bp.print("black_scholes(cpp11_seq)");
        
    return 0;
}
