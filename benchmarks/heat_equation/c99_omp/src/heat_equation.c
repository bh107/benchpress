#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <bp_util.h>

inline double innerloop(const double* grid, double* T, int width, int i)
{
    int a = i * width;
    const double *up     = &grid[a+1];
    const double *left   = &grid[a+width];
    const double *right  = &grid[a+width+2];
    const double *down   = &grid[a+1+width*2];
    const double *center = &grid[a+width+1];
    double *t_center = &T[a+width+1];

    double delta = 0;
    for(int j=0; j<width-2; ++j)
    {
        *t_center = (*center + *up + *left + *right + *down) * 0.2;
        delta += fabs(*t_center - *center);
        center++;up++;left++;right++;down++;t_center++;
    }
    return delta;
}

void openmp(int height, int width, double *grid, int iter)
{
    double* grid_i;
    double* T_i;

    double *T = (double*)malloc(height*width*sizeof(double));

    //
    // NumaEffects - begin
    //
    // memcpy(T, grid, height*width*sizeof(double)); <-- bad idea
    //
    // memcpy is sequentiel and will touch the entire
    // grid on one numa-node.
    //
    // Instead of memset, parallel copy
    // is performed with the following loop construct:
    //
    grid_i = grid;
    T_i = T;
    #pragma omp parallel for collapse(2)
    for(int i=0; i<height; ++i) {
        for(int j=0; j<width; ++j) {
            *T_i = *grid_i;
            ++T_i;
            ++grid_i;
        }
    }
    //
    // NumaEffects - end
    for(int n=0; n<iter; ++n)
    {
        double delta=0;
        #pragma omp parallel for shared(grid, T) reduction(+:delta)
        for(int i=0; i<height-2; ++i)
        {
            delta += innerloop(grid, T, width, i);
        }
        //
        // NumaEffects - begin
        //
        // memcpy(grid, T, height*width*sizeof(double)); // <-- bad idea
        //
        // memcpy is sequentiel and will touch the entire
        // grid on one numa-node.
        //
        // Instead of memset, parallel copy
        // is performed with the following loop construct:
        //
        grid_i = grid;
        T_i = T;
        #pragma omp parallel for collapse(2)
        for(int i=0; i<height; ++i) {
            for(int j=0; j<width; ++j) {
                ++grid_i;
                ++T_i;
                *grid_i = *T_i;
            }
        }
        //
        // NumaEffects - end
    }
    free(T);
}

int main (int argc, char **argv)
{
    bp_util_type bp = bp_util_create(argc, argv, 3);
    if (bp.args.has_error) {
        return 1;
    }
    const int height    = bp.args.sizes[0];
    const int width     = bp.args.sizes[1];
    const int iter      = bp.args.sizes[2];

    size_t grid_size = height*width*sizeof(double);
    double *grid = (double*)malloc(grid_size);
    //
    // NumaEffects - begin
    //
    // memset(grid, 0, grid_size);  // <--- bad idea.
    // memset is sequentiel and will touch the entire
    // grid on one numa-node.
    //
    // Instead of memset, parallel initialization
    // is performed with the following loop construct:
    //
    double* grid_i = grid;
    #pragma omp parallel for collapse(2)
    for(int i=0; i<height; ++i) {
        for(int j=0; j<width; ++j) {
            *grid_i = 0;
            ++grid_i;
        }
    }
    //
    // NumaEffects - end
    for(int j=0; j<width;j++) {
        grid[j] = 40.0;
        grid[j+(height-1)*width] = -273.15;
    }
    for(int j=1; j<height-1;j++) {
        grid[j*width] = -273.15;
        grid[j*width+width-1]= -273.15;
    }
#ifdef DEBUG
    for (int i = 0; i<height; i++)
    {
        for(int j=0; j<width;j++)
        {
            printf ("%lf ", grid[j+i*width]);
        }
        printf ("\n");
    }       
#endif
    bp.timer_start();
    openmp(height,width,grid,iter);
    bp.timer_stop();
#ifdef DEBUG
    for (int i = 0; i<height; i++)
    {
        for(int j=0; j<width;j++)
        {
            printf ("%lf ", grid[j+i*width]);
        }
        printf ("\n");
    }       
#endif
    bp.print("heat_equation(c99_omp)");
    free(grid);
    return 0;
}
