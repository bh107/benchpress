/*
This file is part of Bohrium and Copyright (c) 2012 the Bohrium team:
http://bohrium.bitbucket.org

Bohrium is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation, either version 3
of the License, or (at your option) any later version.

Bohrium is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the
GNU Lesser General Public License along with bohrium.

If not, see <http://www.gnu.org/licenses/>.
*/
#include <iostream>
#include <bxx/bohrium.hpp>
#include <bp_util.h>

using namespace std;
using namespace bxx;

template <typename T>
multi_array<T>& cnd(multi_array<T>& x)
{
    multi_array<T> l, k, w;
    multi_array<bool> mask;
    T a1 = 0.31938153,
      a2 =-0.356563782,
      a3 = 1.781477937,
      a4 =-1.821255978,
      a5 = 1.330274429,
      pp = 2.5066282746310002; // sqrt(2.0*PI)

    l = abs(x);
    k = 1.0 / (1.0 + 0.2316419 * l);
    w = 1.0 - 1.0 / pp * exp(-1.0*l*l/2.0) * \
        (a1*k + \
         a2*(add(k,(T)2)) + \
         a3*(add(k,(T)3)) + \
         a4*(add(k,(T)4)) + \
         a5*(add(k,(T)5)));

    mask = x < 0.0;
    return w * as<T>(!mask) + (1.0-w)* as<T>(mask);
}

//FLOP count: 2*s+i*(s*8+2*s*26) where s is samples and i is iterations
template <typename T>
T* pricing(size_t samples, size_t iterations, char flag, T x, T d_t, T r, T v)
{
    multi_array<T> d1, d2, res, s;
    T* p    = (T*)malloc(sizeof(T)*iterations);    // Intermediate results
    T t     = d_t;                              // Initial delta

    s = random<T>((int64_t)samples)*4.0 +58.0;           // Model between 58-62

    for(size_t i=0; i<iterations; i++) {
        d1 = (log(s/x) + (r+v*v/2.0)*t) / (v*sqrt(t));
        d2 = d1-v*sqrt(t);

        if (flag == 'c') {
            res = s * cnd(d1) - x * exp(-r * t) * cnd(d2);
        } else {
            res = x * exp(-r*t) * cnd(-1.0*d2) - s*cnd(-1.0*d1);
        }

        t += d_t;                               // Increment delta
        p[i] = scalar(sum(res)) / (T)samples;   // Result from timestep
    }

    return p;
}

int main(int argc, char* argv[])
{
    bp_util_type bp = bp_util_create(argc, argv, 2);
    if (bp.args.has_error) {
        return 0;
    }
    const size_t samples    = bp.args.sizes[0];
    const size_t iterations = bp.args.sizes[1];

    bp.timer_start();
    double* prices = pricing(
        samples, iterations,
        'c', 65.0, 1.0 / 365.0,
        0.08, 0.3
    );
    bp.timer_stop();
    
    bp.print("black_scholes(cpp11_bxx)");
    if (bp.args.verbose) {                 // and values.
        cout << ", \"output\": [";
        for(size_t i=0; i<iterations; i++) {
            cout << prices[i];
            if (iterations-1!=i) {
                cout << ", ";
            }
        }
        cout << "]" << endl;
    }

    free(prices);                           // Cleanup
    return 0;
}

