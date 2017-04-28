#include <iostream>
#include <iomanip>
#include <bp_util.h>

using namespace std;

double leibnitz_pi(int nelements)
{
    double sum = 0.0;
    for(int n=0; n<nelements; ++n) {
        sum += 1.0/(4*n+1) - 1.0/(4*n+3);
    }
    return sum;
}

int main(int argc, char* argv[])
{
    bp_util_type bp = bp_util_create(argc, argv, 1);// Grab arguments
    if (bp.args.has_error) {
        return 1;
    }
    const int nelements = bp.args.sizes[0];

    bp.timer_start();                               // Start timer
    double pi = 4.0*leibnitz_pi(nelements);         // Run benchmark
    bp.timer_stop();                                // Stop timer

    bp.print("leibnitz_pi(cpp11_seq)");				// Print results..
    if (bp.args.verbose) {                          // ..and value.
        cout << fixed << setprecision(11)
			 << "PI-approximation = " << pi << endl;
    }

    return 0;
}
