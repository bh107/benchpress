#include <blitz/array.h>
#include <random/uniform.h>
#include <util/argparse.hpp>
#include <util/timing.hpp>

using namespace blitz;
using namespace ranlib;
using namespace argparse;

double monte_carlo_pi(int samples, int iterations)
{
    Array<double, 1> x(samples), y(samples), m(samples);       // Operands
    Array<double, 1> c(1), accu(1);
    accu = 0;

    Uniform<double> rand;
    rand.seed((unsigned int)time(0));

    for(int i=0; i<iterations; ++i) {
        x = rand.random();               // Sample random numbers
        y = rand.random();
        m = cast<double>(sqrt(x*x + y*y)<=1.0); // Model
        c = sum(m);                             // Count
        accu += (c*4.0) / (double)samples;      // Approximate
    }
    accu /= (double)iterations;
    
    return accu(0);
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

    size_t start = sample_time();
    double pi = monte_carlo_pi(samples, iterations);
    size_t end = sample_time();

	bp.print("mcpi(cpp11_blitz)");     
    if (bp.args.verbose) {                             // and values.
        cout << "PI-approximation = " << pi << endl;
    }

    return 0;
}

