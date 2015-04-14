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
    return 4.0*sum;
}

int main(int argc, char* argv[])
{
    bp_util_type bp = bp_util_create(argc, argv, 1);
    const int nelements = bp.args.sizes[0];

    bp.timer_start();
    double pi = leibnitz_pi(nelements);
    bp.timer_stop();

    bp.print("leibnitz_pi(cpp11_seq)");
    if (bp.args.verbose) {                             // and values.
        cout << fixed << setprecision(11) << "PI = " << pi << endl;
    }

    return 0;
}
