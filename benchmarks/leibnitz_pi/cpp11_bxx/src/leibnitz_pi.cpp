#include <iostream>
#include <iomanip>
#include <bxx/bohrium.hpp>
#include <bp_util.h>

using namespace std;
using namespace bxx;

double leibnitz_pi(int nelements)
{
    multi_array<double> n;
    n = range<double>(nelements);

    return scalar(4.0*sum(1.0/(4.0*n+1.0) - 1.0/(4.0*n+3.0)));
}

int main(int argc, char* argv[])
{
    bp_util_type bp = bp_util_create(argc, argv, 1);// Grab arguments
    if (bp.args.has_error) {
        return 1;
    }
    const int nelements = bp.args.sizes[0];

    Runtime::instance().flush();
    bp.timer_start();                               // Start timer
    double pi = leibnitz_pi(nelements);             // Run benchmark
    Runtime::instance().flush();
    bp.timer_stop();                                // Stop timer

    bp.print("leibnitz_pi(cpp11_bxx)");				// Print results..
    if (bp.args.verbose) {                          // ..and value.
        cout << fixed << setprecision(11)
			 << "PI-approximation = " << pi << endl;
    }

    return 0;
}
