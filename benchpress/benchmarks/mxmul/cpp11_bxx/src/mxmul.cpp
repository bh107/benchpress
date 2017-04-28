#include <iostream>
#include <iomanip>
#include <bxx/bohrium.hpp>
#include <bp_util.h>

using namespace std;
using namespace bxx;

int main(int argc, char* argv[])
{
    bp_util_type bp = bp_util_create(argc, argv, 1);// Grab arguments
    if (bp.args.has_error) {
        return 1;
    }
    const int n = bp.args.sizes[0];
    const double nelements = n*n;

    multi_array<double> a, b, c;                    // Construct matrices
    a = view_as<double>(range<double>(n*n) / nelements, n, n);
    b = view_as<double>(range<double>(n*n) / nelements, n, n);

    Runtime::instance().flush();
    bp.timer_start();                               // Start timer
    c = matmul(a, b);                               // Run benchmark
    Runtime::instance().flush();
    bp.timer_stop();                                // Stop timer

    bp.print("mxmul(cpp11_bxx)");				    // Print results..
    if (bp.args.verbose) {                          // ..and value.
        cout << fixed << setprecision(10)
			 << "Result = " << scalar<double>(sum(c)) << endl;
    }

    return 0;
}
