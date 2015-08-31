#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <bp_util.h>
#include <omp.h>

void seq_init(double* grid, size_t nelements)
{
    memset(grid, 0, nelements);
}

void seq_exec(double* grid, size_t nelements)
{
    for(size_t eidx=0; eidx<nelements; ++eidx) {
        grid[eidx] = eidx / 2.0;
    } 
}

void par_init(double* grid, size_t nelements)
{
    #pragma omp parallel for
    for(size_t eidx=0; eidx<nelements; ++eidx) {
        grid[eidx] = 0;
    }
}

void par_exec(double* grid, size_t nelements)
{
    #pragma omp parallel for
    for(size_t eidx=0; eidx<nelements; ++eidx) {
        grid[eidx] = eidx / 2.0;
    } 
}

int main (int argc, char **argv)
{
    bp_util_type bp = bp_util_create(argc, argv, 3);
    if (bp.args.has_error) {
        return 1;
    }
    const size_t nelements     = bp.args.sizes[0];
    const size_t iterations    = bp.args.sizes[1];
    const size_t mode          = bp.args.sizes[2];

    double *grid = malloc(sizeof(*grid)*nelements);

    switch(mode) {
        case 0:
        case 2:
            fprintf(stdout, "Serial initialization\n");
            seq_init(grid, nelements);
            break;
        case 1:
        case 3:
            fprintf(stdout, "Parallel initialization\n");
            par_init(grid, nelements);
            break;
        default:
            fprintf(stderr, "Unknown mode.\n");
    }

    bp.timer_start();
    switch(mode) {
        case 0:
        case 1:
            fprintf(stdout, "Serial execution\n");
            for(size_t i=0; i<iterations; ++i) {
                seq_exec(grid, nelements);
            }
            break;
        case 2:
        case 3:
            fprintf(stdout, "Parallel execution\n");
            for(size_t i=0; i<iterations; ++i) {
                par_exec(grid, nelements);
            }
            break;
        default:
            fprintf(stderr, "Unknown mode.\n");
    }
    bp.timer_stop();

    bp.print("synth_init(c99_omp)");

    free(grid);
    return 0;
}

