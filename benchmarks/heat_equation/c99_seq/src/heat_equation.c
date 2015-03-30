#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <bp_util.h>

void sequential(int height, int width, double *grid, int iter)
{
  double *T = (double*)malloc(height*width*sizeof(double));
  memcpy(T, grid, height*width*sizeof(double));
  for(int n=0; n<iter; ++n)
  {
    double *a = grid;
    double *t = T;
    double delta=0;
    for(int i=1; i<height-1; ++i)
    {
      double *up     = a+1;
      double *left   = a+width;
      double *right  = a+width+2;
      double *down   = a+1+width*2;
      double *center = a+width+1;
      double *t_center = t+width+1;
      for(int j=0; j<width-2; ++j)
      {
        *t_center = (*center + *up + *left + *right + *down) * 0.2;
        delta += fabs(*t_center - *center);
        center++;up++;left++;right++;down++;t_center++;
      }
      a += width;
      t += width;
    }
#ifdef DEBUG
    printf("Delta: %lf\n",delta);
#endif
    memcpy(grid, T, height*width*sizeof(double));
  }
  free(T);
}

int main (int argc, char **argv)
{
    bp_arguments_type args = parse_args(argc, argv);        // Parse args
    printf(
        "Running heat_equation_jacobi on %d*%d for %i iterations.\n",
        args.sizes[0],
        args.sizes[1],
        args.sizes[2]
    );

    const int width     = args.sizes[0];
    const int height    = args.sizes[1];
    const int iter      = args.sizes[2];

    size_t grid_size = height*width*sizeof(double);
    double *grid = (double*)malloc(grid_size);
    memset(grid, 0, grid_size);
    for(int j=0; j<width;j++)
    {
        grid[j] = 40.0;
        grid[j+(height-1)*width] = -273.15;
    }
    for(int j=1; j<height-1;j++)
    {
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
    size_t start = bp_sample_time();
    sequential(height,width,grid,iter);
    size_t end = bp_sample_time();
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
    size_t elapsed = end - start;

    printf("sequential.c - iter: %d size: %d elapsed-time: %lf\n", iter, width, elapsed/(double)1000000.0);
    free(grid);
    return 0;
}
