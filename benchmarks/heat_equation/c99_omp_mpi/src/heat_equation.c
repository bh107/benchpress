#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <mpi.h>
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
    double *T = (double*)malloc(height*width*sizeof(double));
    memcpy(T, grid, height*width*sizeof(double));
    for(int n=0; n<iter; ++n)
    {
        double delta=0;
        #pragma omp parallel for shared(grid,T) reduction(+:delta)
        for(int i=0; i<height-2; ++i)
        {
            delta += innerloop(grid, T, width, i);
        }
        memcpy(grid, T, height*width*sizeof(double));
    }
    free(T);
}

void openmp_mpi(int height, int width, double *grid, int iter)
{
    int myrank, worldsize;
    MPI_Comm comm;
    MPI_Comm_rank(MPI_COMM_WORLD, &myrank);
    MPI_Comm_size(MPI_COMM_WORLD, &worldsize);

    int periods[] = {0};
    MPI_Cart_create(MPI_COMM_WORLD, 1, &worldsize,
                    periods, 1, &comm);

    double *T = (double*)malloc(height*width*sizeof(double));
    memcpy(T, grid, height*width*sizeof(double));
    for(int n=0; n<iter; ++n)
    {
        int p_src, p_dest;
        //Send/receive - neighbor above
        MPI_Cart_shift(comm,0,1,&p_src,&p_dest);
        MPI_Sendrecv(grid+width,width,MPI_DOUBLE,
                     p_dest,1,
                     grid,width, MPI_DOUBLE,
                     p_src,1,comm,MPI_STATUS_IGNORE);
        //Send/receive - neighbor below
        MPI_Cart_shift(comm,0,-1,&p_src,&p_dest);
        MPI_Sendrecv(grid+(height-2)*width, width,MPI_DOUBLE,
                     p_dest,1,
                     grid+(height-1)*width,
                     width,MPI_DOUBLE,
                     p_src,1,comm,MPI_STATUS_IGNORE);

        double delta=0, global_delta;
        #pragma omp parallel for shared(grid,T) reduction(+:delta)
        for(int i=0; i<height-2; ++i)
        {
            delta += innerloop(grid, T, width, i);
        }
        memcpy(grid, T, height*width*sizeof(double));
        MPI_Allreduce(&global_delta, &delta, 1, MPI_DOUBLE, MPI_SUM, MPI_COMM_WORLD);
    }
    free(T);
}

int main (int argc, char **argv)
{
    MPI_Init(&argc,&argv);
    int myrank, worldsize;
    MPI_Comm_rank(MPI_COMM_WORLD, &myrank);
    MPI_Comm_size(MPI_COMM_WORLD, &worldsize);

    bp_util_type bp = bp_util_create(argc, argv, 3);
    if (bp.args.has_error) {
        return 1;
    }
    int height      = bp.args.sizes[0];
    const int width = bp.args.sizes[1];
    const int iter  = bp.args.sizes[2];

    //Local vertical size. NB: the horizontal size is always the full grid including borders
    height = (width-2) / worldsize;
    if(myrank == worldsize-1)
        height += (width-2) % worldsize;
    height += 2;//Add a ghost line above and below

    double *grid = malloc(height*width*sizeof(double));
    for(int j=0; j<width;j++)
    {
        if(myrank == 0)
           grid[j] = 40.0;
        if(myrank == worldsize-1)
            grid[j+(height-1)*width] = -273.15;
    }
    for(int j=1; j<height-1;j++)
    {
        grid[j*width] = -273.15;
        grid[j*width+width-1]= -273.15;
    }

    MPI_Barrier(MPI_COMM_WORLD);
    bp.timer_start();
    openmp(height,width,grid,iter);

    MPI_Barrier(MPI_COMM_WORLD);
    bp.timer_stop();

    if (myrank == 0) {
        bp.print("heat_equation(c99_omp_mpi)");
    }
    free(grid);
    MPI_Finalize();
    return 0;
}
