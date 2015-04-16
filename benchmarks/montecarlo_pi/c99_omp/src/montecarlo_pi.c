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

double montecarlo_pi_fused(int64_t samples, uint64_t xr_count, uint64_t yr_count, uint64_t key)
{
    uint64_t darts = 0;

    double* x = (double*) malloc(samples*sizeof(double));
    double* y = (double*) malloc(samples*sizeof(double));
    
    #pragma omp parallel for reduction(+:darts)
    for (int64_t eidx=0; eidx<samples; ++eidx) {

        uint64_t x_raw = ((philox2x32_as_1x64_t)philox2x32(
          ((philox2x32_as_1x64_t)( xr_count+eidx )).orig,
          (philox2x32_key_t){ { key } }
        )).combined;
        x[eidx] = x_raw;
        x[eidx] /= 18446744073709551616.000000;

        uint64_t y_raw = ((philox2x32_as_1x64_t)philox2x32(
          ((philox2x32_as_1x64_t)( yr_count+eidx )).orig,
          (philox2x32_key_t){ { key } }
        )).combined;

        y[eidx] = y_raw;
        y[eidx] /= 18446744073709551616.000000;

        darts += (x[eidx]*x[eidx] + y[eidx]*y[eidx]) <= 1;
    }
    return (double)darts/samples*4;
}

double montecarlo_pi(int64_t samples, uint64_t xr_count, uint64_t yr_count, uint64_t key)
{
    uint64_t darts = 0;
    
    #pragma omp parallel for reduction(+:darts)
    for (int64_t eidx=0; eidx<samples; ++eidx) {

        uint64_t x_raw = ((philox2x32_as_1x64_t)philox2x32(
          ((philox2x32_as_1x64_t)( xr_count+eidx )).orig,
          (philox2x32_key_t){ { key } }
        )).combined;
        double x = x_raw;
        x /= 18446744073709551616.000000;

        uint64_t y_raw = ((philox2x32_as_1x64_t)philox2x32(
          ((philox2x32_as_1x64_t)( yr_count+eidx )).orig,
          (philox2x32_key_t){ { key } }
        )).combined;
        double y = y_raw;
        y /= 18446744073709551616.000000;

        darts += (x*x + y*y) <= 1;
    }
    return (double)darts/samples*4;
}

double run_montecarlo_pi(int64_t samples, int64_t iterations)
{
    const uint64_t key = 1597416434;    // Philox key
    uint64_t random_count = 0;          // Calls to philox
    uint64_t xr_count = 0;              // x-count offset to philox
    uint64_t yr_count = 0;              // y-count offset to philox

    double pi_accu = 0.0;               // Accumulation over PI-approximations.
    for(int64_t i=0; i<iterations; ++i) {
        xr_count = random_count++;
        yr_count = random_count++;
        //pi_accu += montecarlo_pi_fused(samples, xr_count, yr_count, key);
        pi_accu += montecarlo_pi(samples, xr_count, yr_count, key);
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
