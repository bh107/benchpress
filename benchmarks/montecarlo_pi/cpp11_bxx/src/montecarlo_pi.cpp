#include <iostream>
#include "bxx/bohrium.hpp"
#include <bp_util.h>

using namespace std;
using namespace bxx;

template <typename T>
multi_array<T>& monte_carlo_pi(int samples)
{
    multi_array<T> x, y, m;             // Operands

    x = randu<T>(samples);              // Sample random numbers
    y = randu<T>(samples);
    m = as<T>(sqrt(x*x + y*y) <= 1.0);  // Model

    return sum(m) * 4.0 / (T)samples;   // Count
}

template <typename T>
T solve(int samples, int iterations)
{
    multi_array<T> acc;                 // Acculumate across iterations
    acc = zeros<T>(1);
    for(int i=0; i<iterations; ++i) {
        acc += monte_carlo_pi<T>(samples);        
    }
    acc /= (T)iterations;
    return scalar(acc);
}

int main(int argc, char* argv[])
{
    bp_util_type bp = bp_util_create(argc, argv, 2);// Grab arguments
    if (bp.args.has_error) {
        return 1;
    }
    const int samples = bp.args.sizes[0];
    const int iterations = bp.args.sizes[1];

    Runtime::instance().flush();
    bp.timer_start();
    double pi = solve<double>(samples, iterations);
    Runtime::instance().flush();
    bp.timer_stop();
                                                    // Output timing
    bp.print("montecarlo_pi(cpp11_bxx)");
    if (bp.args.verbose) {                          // and values.
        cout << "PI-approximation = " << pi << endl;
    }

    return 0;
}

