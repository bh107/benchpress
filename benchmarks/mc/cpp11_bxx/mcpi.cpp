#include <iostream>
#include "bxx/bohrium.hpp"

using namespace std;
using namespace bxx;
using namespace argparse;

double monte_carlo_pi(int samples, int iterations)
{
    multi_array<double> x, y, m, c, accu(1);    // Operands
    accu = (double)0.0;                         // Acculumate across iterations
    for(int i=0; i<iterations; ++i) {
        x = random<double>(samples);            // Sample random numbers
        y = random<double>(samples);
        m = as<double>(sqrt(x*x + y*y)<=1.0);   // Model
        c = sum(m);                             // Count

        accu += (c*4.0) / (double)samples;      // Approximate
    }
    accu /= (double)iterations;
    
    return scalar(accu);
}

int main(int argc, char* argv[])
{
    bp_util_type bp = bp_util_create(argc, argv, 2);// Grab arguments
    if (bp.args.has_error) {
        return 1;
    }
    const int samples = bp.args.sizes[0];
    const int iterations = bp.args.sizes[1]

    bp.timer_start();
    double pi = monte_carlo_pi(samples, iterations);
    bp.timer_end();
                                                    // Output timing
    bp.print("mc(cpp11_bxx)");
    if (bp.args.verbose) {                             // and values.
        cout << "PI-approximation = " << pi << endl;
    }

    return 0;
}

