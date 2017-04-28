#include <inttypes.h>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <Random123/philox.h>
#include <bp_util.h>

typedef union philox2x32_as_1x64 {
    philox2x32_ctr_t orig;
    uint64_t combined;
} philox2x32_as_1x64_t;

double montecarlo_pi(uint32_t samples, uint32_t x_index, uint32_t y_index, uint32_t key)
{
    uint64_t darts = 0;
    
    #pragma omp parallel for reduction(+:darts)
    for (uint32_t eidx=0; eidx<samples; ++eidx) {

        uint64_t x_raw = ((philox2x32_as_1x64_t)philox2x32(
          ((philox2x32_as_1x64_t)( (uint64_t)(x_index + eidx) )).orig,
          (philox2x32_key_t){ { key } }
        )).combined;
        double x = x_raw / 18446744073709551616.000000;

        uint64_t y_raw = ((philox2x32_as_1x64_t)philox2x32(
          ((philox2x32_as_1x64_t)( (uint64_t)(y_index + eidx) )).orig,
          (philox2x32_key_t){ { key } }
        )).combined;
        double y = y_raw / 18446744073709551616.000000;

        darts += sqrt(x*x + y*y) <= 1;
    }
    return (double)darts * (double)4.0 / (double)samples;
}

double run_montecarlo_pi(int64_t samples, int64_t iterations)
{
    uint64_t index = 0;                 // Philox index
    const uint64_t key = 0;             // Philox key
    uint64_t x_index = 0;
    uint64_t y_index = 0;

    double pi_accu = 0.0;               // Accumulation over PI-approximations.
    for(int64_t i=0; i<iterations; ++i) {
        x_index = index;
        index += samples;
        y_index = index;
        index += samples;
        pi_accu += montecarlo_pi(samples, x_index, y_index, key);
    }
    pi_accu /= iterations;              // Approximated value of PI

    return pi_accu;
}

int main(int argc, char** argv)
{
    bp_util_type bp = bp_util_create(argc, argv, 2);// Grab arguments
    if (bp.args.has_error) {
        return 1;
    }
    const int samples = bp.args.sizes[0];
    const int iterations = bp.args.sizes[1];

    bp.timer_start();
    double pi = run_montecarlo_pi(samples, iterations);
    bp.timer_stop();

    bp.print("montecarlo_pi(c99_omp)");
    if (bp.args.verbose) {
        printf("PI-approximation = %f\n", pi);
    }

    return 0;
}
