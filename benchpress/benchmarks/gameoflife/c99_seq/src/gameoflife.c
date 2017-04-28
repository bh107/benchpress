#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <bp_util.h>

void world(double* state, int height, int width)
{
    for (int h=0; h<height; ++h) {
        for (int w=0; w<width; ++w) {
            state[h*width + w] = (((h < 2) && (h > (height-3))) ||
                                 ((w < 2) && (w > (width-3))));
        }
    }
}

void play(double* state, int height, int width, int iterations, int version)
{
    printf("%p %d %d %d %d\n", state, height, width, iterations, version);
}

int main (int argc, char **argv)
{
    bp_util_type bp = bp_util_create(argc, argv, 4); // Grab arguments
    if (bp.args.has_error) {
        return 1;
    }

    const int height    = bp.args.sizes[0];
    const int width     = bp.args.sizes[1];
    const int iter      = bp.args.sizes[2];
    const int version   = bp.args.sizes[3];

    size_t grid_size = height*width*sizeof(double);
    double *state = (double*)malloc(grid_size);

    world(state, height, width);

    bp.timer_start();
    play(state, height, width, iter, version);
    bp.timer_stop();

    bp.print("gameoflife(c99_seq)");

    free(state);
    return 0;
}
