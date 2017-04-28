// Adapted from: http://people.sc.fsu.edu/~jburkardt/m_src/shallow_water_2d/
// Saved images may be converted into an animated gif with:
// convert   -delay 20   -loop 0   swater*.png   swater.gif
#include <math.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <bp_util.h>

#include <boost/multi_array.hpp>

int main (int argc, char **argv)
{
    bp_util_type bp = bp_util_create(argc, argv, 3);
    if (bp.args.has_error) {
        return 1;
    }
    const int n         = bp.args.sizes[0];
    const int other_n   = bp.args.sizes[1];
    const int T         = bp.args.sizes[2];

    if (n != other_n) {
        fprintf(stderr, "Implementation only supports quadratic grid.\n");
        exit(0);
    }

    const double g   = 9.8;       // gravitational constant
    const double dt  = 0.02;      // hardwired timestep
    const double dx  = 1.0;
    const double dy  = 1.0;
    const int droploc = n/4;

    typedef boost::multi_array<double, 2> array_type;

    array_type H(boost::extents[n+2][n+2]);
    array_type U(boost::extents[n+2][n+2]);
    array_type V(boost::extents[n+2][n+2]);

    array_type Hx(boost::extents[n+1][n+1]);
    array_type Ux(boost::extents[n+1][n+1]);
    array_type Vx(boost::extents[n+1][n+1]);
    array_type Hy(boost::extents[n+1][n+1]);
    array_type Uy(boost::extents[n+1][n+1]);
    array_type Vy(boost::extents[n+1][n+1]);


    for(int i=0; i<n+2; i++)
        for(int j=0; j<n+2; j++)
        {
          H[i][j]=0.1;
          U[i][j]=0.1;
          V[i][j]=0.1;
        }


    for(int i=0; i<n+1; i++)
        for(int j=0; j<n+1; j++)
        {
          Hx[i][j]=0.1;
          Ux[i][j]=0.1;
          Vx[i][j]=0.1;

          Hy[i][j]=0.1;
          Uy[i][j]=0.1;
          Vy[i][j]=0.1;
        }

    H[droploc][droploc] += 5.0;

    bp.timer_start();

    for(int iter=0; iter < T; iter++)
    {
        // Reflecting boundary conditions
        for(int i=0; i<n+2; i++)
        {
            H[i][0] = H[i][1]   ; U[i][0] = U[i][1]     ; V[i][0] = -V[i][1];
            H[i][n+1] = H[i][n] ; U[i][n+1] = U[i][n]   ; V[i][n+1] = -V[i][n];
            H[0][i] = H[1][i]   ; U[0][i] = -U[1][i]    ; V[0][i] = V[1][i];
            H[n+1][i] = H[n][i] ; U[n+1][i] = -U[n][i]  ; V[n+1][i] = V[n][i];
        }
        //
        // First half step
        //
        for(int i=0; i<n+1; i++)
        {
            for(int j=0; j<n; j++)
            {

                // height
                Hx[i][j] = (H[i+1][j+1]+H[i][j+1])/2 - dt/(2*dx)*(U[i+1][j+1]-U[i][j+1]);

                // x momentum
                Ux[i][j] = (U[i+1][j+1]+U[i][j+1])/2 -          \
                dt/(2*dx)*((pow(U[i+1][j+1],2)/H[i+1][j+1] +	\
                          g/2*pow(H[i+1][j+1],2)) -		\
                         (pow(U[i][j+1],2)/H[i][j+1] +	        \
                          g/2*pow(H[i][j+1],2)));

                // y momentum
                Vx[i][j] = (V[i+1][j+1]+V[i][j+1])/2 -          \
                      dt/(2*dx)*((U[i+1][j+1] *                 \
                                  V[i+1][j+1]/H[i+1][j+1]) -    \
                                 (U[i][j+1] *                   \
                                  V[i][j+1]/H[i][j+1]));
            }
        }

        for(int i=0; i<n; i++)
        {
            for(int j=0; j<n+1; j++)
            {
                //height
                Hy[i][j] = (H[i+1][j+1]+H[i+1][j])/2 - dt/(2*dy)*(V[i+1][j+1]-V[i+1][j]);

                //x momentum
                Uy[i][j] = (U[i+1][j+1]+U[i+1][j])/2 -	   \
                dt/(2*dy)*((V[i+1][j+1] *                  \
                           U[i+1][j+1]/H[i+1][j+1]) -	   \
                                (V[i+1][j] *               \
                                 U[i+1][j]/H[i+1][j]));

                //y momentum
                Vy[i][j] = (V[i+1][j+1]+V[i+1][j])/2 -	\
                dt/(2*dy)*((pow(V[i+1][j+1],2)/H[i+1][j+1] +	\
                           g/2*pow(H[i+1][j+1],2)) -	\
                          (pow(V[i+1][j],2)/H[i+1][j] +	\
                           g/2*pow(H[i+1][j],2)));
            }
        }
        //
        // Second half step
        //

        for(int i=1; i<n+1; i++)
        {
            for(int j=1; j<n+1; j++)
            {
                //height
                H[i][j] -= (dt/dx)*(Ux[i][j-1]-Ux[i-1][j-1]) - (dt/dy)*(Vy[i-1][j]-Vy[i-1][j-1]);

                // x momentum
                U[i][j] -= (dt/dx)*((pow(Ux[i][j-1],2)/Hx[i][j-1] + g/2*pow(Hx[i][j-1],2)) -        \
                                    (pow(Ux[i-1][j-1],2)/Hx[i-1][j-1] + g/2*pow(Hx[i-1][j-1],2))) - \
                           (dt/dy)*((Vy[i-1][j] * Uy[i-1][j]/Hy[i-1][j]) -
                                    (Vy[i-1][j-1] * Uy[i-1][j-1]/Hy[i-1][j-1]));

                // y momentum    - score
                V[i][j] -= (dt/dx)*((Ux[i][j-1] * Vx[i][j-1]/Hx[i][j-1]) -                         \
                                    (Ux[i-1][j-1]*Vx[i-1][j-1]/Hx[i-1][j-1])) -                    \
                           (dt/dy)*((pow(Vy[i-1][j],2)/Hy[i-1][j] + g/2*pow(Hy[i-1][j],2)) -       \
                                    (pow(Vy[i-1][j-1],2)/Hy[i-1][j-1] + g/2*pow(Hy[i-1][j-1],2)));

            }
        }
    }

    // res = numpy.add.reduce(numpy.add.reduce(H / n))
    double res = 0.0;
    for(int i=0;i<n+2;i++)
        for(int j=0;j<n+2;j++)
            res+=H[i][j]/n;

    bp.timer_stop();
    bp.print("shallow_water(cpp11_boost)");
}
