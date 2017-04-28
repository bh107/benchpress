#include <iostream>
#include <iomanip>
#include <bp_util.h>
#include <bxx/bohrium.hpp>

using namespace std;
using namespace bxx;

int main(int argc, char* argv[])
{
    bp_util_type bp = bp_util_create(argc, argv, 2);// Grab arguments
    if (bp.args.has_error) {
        return 1;
    }
    const int nelements     = bp.args.sizes[0];
    const int iterations    = bp.args.sizes[1];

    multi_array<double> foo;
    foo = range<double>(nelements);
    
    Runtime::instance().flush();
    bp.timer_start();                               // Start timer
    double* data = foo.data_export();
    for(int i=0; i<nelements; ++i) {
        data[i] = data[i] + 2;
    }
    Runtime::instance().flush();
    bp.timer_stop();                                // Stop timer
    foo.data_import(data);

    bp.print("synth_index(cpp11_bxx)");
    if (bp.args.verbose) {                          // ..and value.
        cout << fixed << setprecision(11)
			 << "Iterations = " << iterations << endl;
        cout << "Result = " << foo << endl;
    }

    return 0;
}
