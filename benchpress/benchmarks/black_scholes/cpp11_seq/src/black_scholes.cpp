#include <iostream>
#include <sstream>
#include <string>
#include <cmath>
#include <Random123/philox.h>
#include <bp_util.h>

using namespace std;

typedef union philox2x32_as_1x64 {
    philox2x32_ctr_t orig;
    uint64_t combined;
} philox2x32_as_1x64_t;

double* model(int64_t samples)
{
    const uint64_t key = 0;
    double* data = (double*)malloc(sizeof(double)*samples);

    for(int64_t count = 0; count<samples; ++count) {
        philox2x32_as_1x64_t counter;
        counter.combined = count;

        philox2x32_as_1x64_t x_philox;

        x_philox.orig = philox2x32(
          counter.orig,
          (philox2x32_key_t){ { key } } 
        );

        double x = x_philox.combined;
        x /= 18446744073709551616.000000;
        x *= 4.0;
        x += 58.0;          // Model between 58-62

        data[count] = x;
    }
    return data;
}

// The cumulative normal distribution function 
double cnd( double x )
{
    double L, K, w;

    double const a1 =  0.31938153,
                 a2 = -0.356563782,
                 a3 =  1.781477937,
                 a4 = -1.821255978,
                 a5 =  1.330274429;

    L = fabs(x);
    K = 1.0 / (1.0 + 0.2316419 * L);
    w = 1.0 - 1.0 / sqrt(2 * M_PI) * exp(-L *L / 2) * (\
        a1 * K         + \
        a2 * pow(K, 2) + \
        a3 * pow(K, 3) + \
        a4 * pow(K, 4) + \
        a5 * pow(K, 5)
    );

    return (x<0) ? 1.0 - w : w;
}

// The Black and Scholes (1973) Stock option formula
void pricing(double* market, double *prices,
             size_t samples, size_t iterations,
             char flag, double x, double d_t, double r, double v)
{
    double t = d_t;

    for(size_t iter=0; iter<iterations; ++iter) {
        double res = 0;
        for(size_t sample=0; sample<samples; ++sample) {
            double d1 = (log(market[sample]/x) + (r+v*v/2)*t) / (v*sqrt(t));
            double d2 = d1-v*sqrt(t);

            if (flag == 'c') {
                res += market[sample] *cnd(d1)-x * exp(-r*t)*cnd(d2);
            } else {
                res += x * exp(-r*t) * cnd(-d2) - market[sample] * cnd(-d1);
            }
        }
        t += d_t;
        prices[iter] = res / samples;
    }
}

int main(int argc, char* argv[])
{
    bp_util_type bp = bp_util_create(argc, argv, 2);
    if (bp.args.has_error) {
        return 0;
    }
    const int samples    = bp.args.sizes[0];
    const int iterations = bp.args.sizes[1];

    double* market = model(samples);        // Generate pseudo-market data
    double* prices = (double*)malloc(sizeof(double)*iterations); // Prices

    bp.timer_start();
    pricing(
        market, prices,
        samples, iterations,
        'c', 65.0, 1.0 / 365.0,
        0.08, 0.3
    );
    bp.timer_stop();
    
    bp.print("black_scholes(cpp11_seq)");
    if (bp.args.verbose) {                 // and values.
        printf("output: [ ");
        for(int i=0; i<iterations; ++i) {
            printf("%f ", prices[i]);
        }
        printf("]\n");
    }

    free(market);
    free(prices);
    return 0;
}
