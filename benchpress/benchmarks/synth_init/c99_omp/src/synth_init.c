#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <bp_util.h>
#include <omp.h>

void ser_init(double* grid, size_t nelements) {
    memset(grid, 0, sizeof(*grid)*nelements);
}

void ser_exec(double* grid, size_t nelements) {
    for(size_t eidx=0; eidx<nelements; ++eidx) {
        grid[eidx] = (grid[eidx]+1)*0.2;
    }
}

void par_init(double* grid, size_t nelements) {
    #pragma omp parallel for
    for(size_t eidx=0; eidx<nelements; ++eidx) {
        grid[eidx] = 0.0;
    }
}

void par_exec(double* grid, size_t nelements) {
    #pragma omp parallel for
    for(size_t eidx=0; eidx<nelements; ++eidx) {
        grid[eidx] = (grid[eidx]+1)*0.2;
    }
}

int main (int argc, char **argv)
{
    bp_util_type bp = bp_util_create(argc, argv, 2);
    if (bp.args.has_error) {
        return 1;
    }
    const size_t nelements     = bp.args.sizes[0];
    const size_t iterations    = bp.args.sizes[1];

    char* env = getenv("SYNTH_INIT_MODE");
    if (!env) {
        fprintf(stderr, "No init mode provided, set SYNTH_INIT_MODE to 0,1,2, or 3.\n");
        return 0;
    }
    const int mode = atoi(env);
    if ((mode<0) || (mode>3)) {
        fprintf(stderr, "Invalid init mode, set SYNTH_INIT_MODE to 0,1,2, or 3.\n");
    }

    double *grid = malloc(sizeof(*grid)*nelements);

    switch(mode) {
        case 0:
        case 2:
            fprintf(stdout, "Serial initialization\n");
            ser_init(grid, nelements);
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
                ser_exec(grid, nelements);
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

    if (bp.args.verbose) {
        double sum = 0.0;
        for(size_t i=0; i<nelements; ++i) {
            sum += grid[i];
        }
        fprintf(stdout, "Sum = %f\n", sum);
    }
    free(grid);
    return 0;
}

