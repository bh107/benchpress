// Adapted from: http://people.sc.fsu.edu/~jburkardt/m_src/shallow_water_2d/
// Saved images may be converted into an animated gif with:
// convert   -delay 20   -loop 0   swater*.png   swater.gif
#include <math.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <bp_util.h>

#define WIDTH 5000
#define HEIGHT 5000

int main (int argc, char **argv)
{
    bp_util_type bp = bp_util_create(argc, argv, 3);
    if (bp.args.has_error) {
        return 1;
    }
    const int height    = bp.args.sizes[0];
    const int width     = bp.args.sizes[1];
    const int T         = bp.args.sizes[2];

    if (width != WIDTH) {
        fprintf(stderr, "Unsupported size, size must be %dx%d\n", WIDTH, HEIGHT);
        exit(0);
    }
    if (height != WIDTH) {
        fprintf(stderr, "Unsupported size, size must be %dx%d\n", WIDTH, HEIGHT);
        exit(0);
    }

    if (width != height) {
        fprintf(stderr, "Implementation only supports quadratic grid.\n");
        exit(0);
    }

    const double g   = 9.8;       // gravitational constant
    const double dt  = 0.02;      // hardwired timestep
    const double dx  = 1.0;
    const double dy  = 1.0;
    const int droploc = WIDTH/4;

    auto H = new double[WIDTH+2][WIDTH+2];
    auto U = new double[WIDTH+2][WIDTH+2];
    auto V = new double[WIDTH+2][WIDTH+2];

    auto Hx = new double[WIDTH+1][WIDTH+1];
    auto Ux = new double[WIDTH+1][WIDTH+1];
    auto Vx = new double[WIDTH+1][WIDTH+1];
    auto Hy = new double[WIDTH+1][WIDTH+1];
    auto Uy = new double[WIDTH+1][WIDTH+1];
    auto Vy = new double[WIDTH+1][WIDTH+1];

    for(int i=0; i<HEIGHT+2; i++) {
        for(int j=0; j<WIDTH+2; j++) {
          H[i][j]=0.1;
          U[i][j]=0.1;
          V[i][j]=0.1;
        }
    }


    for(int i=0; i<HEIGHT+1; i++) {
        for(int j=0; j<WIDTH+1; j++) {
          Hx[i][j]=0.1;
          Ux[i][j]=0.1;
          Vx[i][j]=0.1;

          Hy[i][j]=0.1;
          Uy[i][j]=0.1;
          Vy[i][j]=0.1;
        }
    }
    H[droploc][droploc] += 5.0;

    bp.timer_start();

    for(int iter=0; iter < T; iter++) {
        
        for(int i=0; i<WIDTH+2; i++) {  // Reflecting boundary conditions
            H[i][0] = H[i][1];
            U[i][0] = U[i][1];
            V[i][0] = -V[i][1];
            H[i][WIDTH+1] = H[i][WIDTH];
            U[i][WIDTH+1] = U[i][WIDTH];
            V[i][WIDTH+1] = -V[i][WIDTH];
            H[0][i] = H[1][i];
            U[0][i] = -U[1][i];
            V[0][i] = V[1][i];
            H[HEIGHT+1][i] = H[HEIGHT][i];
            U[HEIGHT+1][i] = -U[HEIGHT][i];
            V[HEIGHT+1][i] = V[HEIGHT][i];
        }

        //
        // First half step
        //

        for(int i=0; i<HEIGHT+1; i++) {
            for(int j=0; j<WIDTH; j++) {

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

        for(int i=0; i<HEIGHT; i++) {
            for(int j=0; j<WIDTH+1; j++) {
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

        for(int i=1; i<HEIGHT+1; i++) {
            for(int j=1; j<WIDTH+1; j++) {
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

    /* NumPy implementation does not do this!?
    // res = numpy.add.reduce(numpy.add.reduce(H / n))
    double res = 0.0;
    for(int i=0;i<HEIGHT+2;i++) {
        for(int j=0;j<WIDTH+2;j++) {
            res+=H[i][j]/WIDTH;
        }
    }
    */

    bp.timer_stop();
    bp.print("shallow_water(cpp11_seq)");
}
