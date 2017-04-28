// Adapted from: http://people.sc.fsu.edu/~jburkardt/m_src/shallow_water_2d/
// Saved images may be converted into an animated gif with:
// convert   -delay 20   -loop 0   swater*.png   swater.gif


#include <math.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <bp_util.h>

#define iH(y,x) (H[(x)+(y)*(n+2)])
#define iU(y,x) (U[(x)+(y)*(n+2)])
#define iV(y,x) (V[(x)+(y)*(n+2)])

#define iHx(y,x) (Hx[(x)+(y)*(n+1)])
#define iUx(y,x) (Ux[(x)+(y)*(n+1)])
#define iVx(y,x) (Vx[(x)+(y)*(n+1)])

#define iHy(y,x) (Hy[(x)+(y)*(n+1)])
#define iUy(y,x) (Uy[(x)+(y)*(n+1)])
#define iVy(y,x) (Vy[(x)+(y)*(n+1)])

int main (int argc, char **argv)
{
    bp_util_type bp = bp_util_create(argc, argv, 3);
    if (bp.args.has_error) {
        return 1;
    }
    const int n = bp.args.sizes[0];
    const int other_n = bp.args.sizes[1];
    const int T = bp.args.sizes[2];

    if (n != other_n) {
        fprintf(stderr, "Implementation only supports quadratic grid.\n");
        exit(0);
    }

    const double g   = 9.8;       // gravitational constant
    const double dt  = 0.02;      // hardwired timestep
    const double dx  = 1.0;
    const double dy  = 1.0;
    const int droploc = n/4;

    double *H = (double*) malloc((n+2)*(n+2)*sizeof(double));
    double *U = (double*) malloc((n+2)*(n+2)*sizeof(double));
    double *V = (double*) malloc((n+2)*(n+2)*sizeof(double));

    double *Hx = (double*) malloc((n+1)*(n+1)*sizeof(double));
    double *Ux = (double*) malloc((n+1)*(n+1)*sizeof(double));
    double *Vx = (double*) malloc((n+1)*(n+1)*sizeof(double));

    double *Hy = (double*) malloc((n+1)*(n+1)*sizeof(double));
    double *Uy = (double*) malloc((n+1)*(n+1)*sizeof(double));
    double *Vy = (double*) malloc((n+1)*(n+1)*sizeof(double));


    for(int i=0; i<n+2; i++)
        for(int j=0; j<n+2; j++)
        {
          iH(i,j)=0.1;
          iU(i,j)=0.1;
          iV(i,j)=0.1;
        }


    for(int i=0; i<n+1; i++)
        for(int j=0; j<n+1; j++)
        {
          iHx(i,j)=0.1;
          iUx(i,j)=0.1;
          iVx(i,j)=0.1;

          iHy(i,j)=0.1;
          iUy(i,j)=0.1;
          iVy(i,j)=0.1;
        }

    iH(droploc,droploc) += 5.0;

    
    bp.timer_start();

    for(int iter=0; iter < T; iter++)
    {
        // Reflecting boundary conditions
        for(int i=0; i<n+2; i++)
        {
            iH(i,0) = iH(i,1)   ; iU(i,0) = iU(i,1)     ; iV(i,0) = -iV(i,1);
            iH(i,n+1) = iH(i,n) ; iU(i,n+1) = iU(i,n)   ; iV(i,n+1) = -iV(i,n);
            iH(0,i) = iH(1,i)   ; iU(0,i) = -iU(1,i)    ; iV(0,i) = iV(1,i);
            iH(n+1,i) = iH(n,i) ; iU(n+1,i) = -iU(n,i)  ; iV(n+1,i) = iV(n,i);
        }
        //
        // First half step
        //
        for(int i=0; i<n+1; i++)
        {
            for(int j=0; j<n; j++)
            {

                // height
                iHx(i,j) = (iH(i+1,j+1)+iH(i,j+1))/2 - dt/(2*dx)*(iU(i+1,j+1)-iU(i,j+1));

                // x momentum
                iUx(i,j) = (iU(i+1,j+1)+iU(i,j+1))/2 -          \
                dt/(2*dx)*((pow(iU(i+1,j+1),2)/iH(i+1,j+1) +	\
                          g/2*pow(iH(i+1,j+1),2)) -		\
                         (pow(iU(i,j+1),2)/iH(i,j+1) +	        \
                          g/2*pow(iH(i,j+1),2)));

                // y momentum
                iVx(i,j) = (iV(i+1,j+1)+iV(i,j+1))/2 -          \
                      dt/(2*dx)*((iU(i+1,j+1) *                 \
                                  iV(i+1,j+1)/iH(i+1,j+1)) -    \
                                 (iU(i,j+1) *                   \
                                  iV(i,j+1)/iH(i,j+1)));
            }
        }

        for(int i=0; i<n; i++)
        {
            for(int j=0; j<n+1; j++)
            {
                //height
                iHy(i,j) = (iH(i+1,j+1)+iH(i+1,j))/2 - dt/(2*dy)*(iV(i+1,j+1)-iV(i+1,j));

                //x momentum
                iUy(i,j) = (iU(i+1,j+1)+iU(i+1,j))/2 -	   \
                dt/(2*dy)*((iV(i+1,j+1) *                  \
                           iU(i+1,j+1)/iH(i+1,j+1)) -	   \
                                (iV(i+1,j) *               \
                                 iU(i+1,j)/iH(i+1,j)));

                //y momentum
                iVy(i,j) = (iV(i+1,j+1)+iV(i+1,j))/2 -	\
                dt/(2*dy)*((pow(iV(i+1,j+1),2)/iH(i+1,j+1) +	\
                           g/2*pow(iH(i+1,j+1),2)) -	\
                          (pow(iV(i+1,j),2)/iH(i+1,j) +	\
                           g/2*pow(iH(i+1,j),2)));
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
                iH(i,j) -= (dt/dx)*(iUx(i,j-1)-iUx(i-1,j-1)) - (dt/dy)*(iVy(i-1,j)-iVy(i-1,j-1));

                // x momentum
                iU(i,j) -= (dt/dx)*((pow(iUx(i,j-1),2)/iHx(i,j-1) + g/2*pow(iHx(i,j-1),2)) -        \
                                    (pow(iUx(i-1,j-1),2)/iHx(i-1,j-1) + g/2*pow(iHx(i-1,j-1),2))) - \
                           (dt/dy)*((iVy(i-1,j) * iUy(i-1,j)/iHy(i-1,j)) -
                                    (iVy(i-1,j-1) * iUy(i-1,j-1)/iHy(i-1,j-1)));

                // y momentum    - score
                iV(i,j) -= (dt/dx)*((iUx(i,j-1) * iVx(i,j-1)/iHx(i,j-1)) -                         \
                                    (iUx(i-1,j-1)*iVx(i-1,j-1)/iHx(i-1,j-1))) -                    \
                           (dt/dy)*((pow(iVy(i-1,j),2)/iHy(i-1,j) + g/2*pow(iHy(i-1,j),2)) -       \
                                    (pow(iVy(i-1,j-1),2)/iHy(i-1,j-1) + g/2*pow(iHy(i-1,j-1),2)));

            }
        }
    }

    /* NumPy implementation does not do this!
    // res = numpy.add.reduce(numpy.add.reduce(H / n))
    double res = 0.0;
    for(int i=0;i<n+2;i++)
        for(int j=0;j<n+2;j++)
            res+=iH(i,j)/n;
    */
    bp.timer_stop();
    bp.print("shallow_water(c99_seq)");
}
