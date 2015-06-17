#include <iostream>
#include <iomanip>
#include <bp_util.h>
#include <bxx/bohrium.hpp>

using namespace std;
using namespace bxx;

template <typename T>
void setup(multi_array<T>& out, multi_array<T>& in,
           multi_array<uint64_t>& index, multi_array<uint64_t>& index_z,
            uint64_t nelements)
{
    out = zeros<T>(nelements);
    in  = range<T>(nelements);
    index   = nelements - (range<uint64_t>(nelements) + (uint64_t)1);
    index_z = nelements - (range<uint64_t>(nelements/2) + (uint64_t)1);
}

template <typename T>
void bench_gather(multi_array<T>& out, multi_array<T>& in,
                  multi_array<uint64_t>& index, int iterations)
{
    for(int i=0; i<iterations; i++) {
        gather(out, in, index);
    }
}

template <typename T>
void bench_gatherz(multi_array<T>& out, multi_array<T>& in,
                  multi_array<uint64_t>& index, int iterations)
{
    for(int i=0; i<iterations; i++) {
        gatherz(out, in, index);
    }
}

template <typename T>
void bench_scatter(multi_array<T>& out, multi_array<T>& in,
                   multi_array<uint64_t>& index, int iterations)
{
    for(int i=0; i<iterations; i++) {
        scatter(out, in, index);
    }
}

template <typename T>
void bench_scatterz(multi_array<T>& out, multi_array<T>& in,
                   multi_array<uint64_t>& index, int iterations)
{
    for(int i=0; i<iterations; i++) {
        scatterz(out, in, index);
    }
}

int main(int argc, char* argv[])
{
    bp_util_type bp = bp_util_create(argc, argv, 3);// Grab arguments
    if (bp.args.has_error) {
        return 1;
    }
    const int nelements     = bp.args.sizes[0];
    const int iterations    = bp.args.sizes[1];
    const int operation     = bp.args.sizes[2];

    multi_array<double> out, in;
    multi_array<uint64_t> index, index_z;

    setup(out, in, index, index_z, nelements);
    
    Runtime::instance().flush();
    bp.timer_start();                               // Start timer
    if (0 == operation) {
        bench_gather(out, in, index, iterations);
    } else if (1 == operation) {
        bench_gatherz(out, in, index_z, iterations);
    } else if (2 == operation) {
        bench_scatter(out, in, index, iterations);
    } else if (3 == operation) {
        bench_scatterz(out, in, index_z, iterations);
    } else {
        cout << "Unknown operation, should be 0=gather, 1=gatherz, 2=scatter, 3=scatterz." << endl;
    }
    Runtime::instance().flush();
    bp.timer_stop();                                // Stop timer

    bp.print("synth_index(cpp11_bxx)");
    if (bp.args.verbose) {                          // ..and value.
        cout << fixed << setprecision(11)
			 << "Iterations = " << iterations << endl;
        cout << "Result of" << endl;
        if (0==operation) {
            cout << "gather(" << endl;
        } else if (1==operation) {
            cout << "gatherz(" << endl;
        } else if (2==operation) {
            cout << "scatter(" << endl;
        } else if (3==operation) {
            cout << "scatterz(" << endl;
        }
        cout << "  out=" << out << "," << endl;
        cout << "  in=" << in << "," << endl;
        if ((0==operation) or (2==operation)) {
            cout << "  index=" << index << ");" << endl;
        } else {
            cout << "  index=" << index_z << ");" << endl;
        }
    }

    return 0;
}
