#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <bp_util.h>

/*
Without collapsing
void solve(int height, int width, double *grid, double epsilon, int max_iterations)
{
    double *T = (double*)malloc(height*width*sizeof(double));

    double delta = epsilon+1.0;
    int iterations = 0;

    while(delta>epsilon) {
        ++iterations;

        #pragma omp parallel for shared(grid, T) reduction(+:delta)
        for(int i=0; i<height-2; ++i)
        {
            int a = i * width;
            const double *up     = &grid[a+1];
            const double *left   = &grid[a+width];
            const double *right  = &grid[a+width+2];
            const double *down   = &grid[a+1+width*2];
            const double *center = &grid[a+width+1];
            double *t_center = &T[a+width+1];

            double delta_local = 0;
            for(int j=0; j<width-2; ++j)
            {
                *t_center = (*center + *up + *left + *right + *down) * 0.2;
                delta_local += fabs(*t_center - *center);
                center++;up++;left++;right++;down++;t_center++;
            }
            delta += delta_local;
        }

        #pragma omp parallel for shared(grid, T)
        for(int i=0; i<height-2; ++i)
        {
            int a = i * width;
            const double *center = &grid[a+width+1];
            double *t_center = &T[a+width+1];

            for(int j=0; j<width-2; ++j)
            {
                *t_center = *center;
                ++t_center;
                ++center;
            }
        }

        if (iterations>=max_iterations) {
            break;
        }
    }
    free(T);
}*/

void solve(int height, int width, double *grid, double epsilon, int max_iterations)
{
    double *T = (double*)malloc(height*width*sizeof(double));

    double delta = epsilon+1.0;
    int iterations = 0;

    while (delta>epsilon) {
        ++iterations;

        #pragma omp parallel for reduction(+:delta) collapse(2)
        for (int i=1; i<height-1; ++i) {
            for (int j=1; j<width-1; ++j) {
                const int a = i * width + j;
                const double *up     = &grid[a-width];
                const double *left   = &grid[a-1];
                const double *right  = &grid[a+1];
                const double *down   = &grid[a+width];
                const double *center = &grid[a];
                double *t_center = &T[a];

                *t_center = (*up + *down + *center + *left + *right) * 0.2;
                delta += fabs(*t_center - *center);
            }
        }

        #pragma omp parallel for collapse(2)
        for (int i=1; i<height-1; ++i) {
            for (int j=1; j<width-1; ++j) {
                const int a = i * width + j;
                const double *center = &grid[a];
                double *t_center = &T[a];

                *t_center = *center;
            }
        }

        if (iterations>=max_iterations) {
            break;
        }
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
    double epsilon = 0.005;

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
    for (int i=0; i<height; ++i) {
        for (int j=0; j<width; ++j) {
            *grid_i = 0;
            ++grid_i;
        }
    }
    //
    // NumaEffects - end
    for (int j=0; j<height; j++) {
        grid[j*width]           = -273.15;
        grid[j*width+width-1]   = -273.15;
    }
    for (int j=0; j<width; j++) {
        grid[j+(height-1)*width] = -273.15;
        grid[j]                  = 40.0;
    }

    bp.timer_start();
    solve(height, width, grid, epsilon, iter);
    bp.timer_stop();

    bp.print("heat_equation(c99_omp)");
    free(grid);
    return 0;
}
