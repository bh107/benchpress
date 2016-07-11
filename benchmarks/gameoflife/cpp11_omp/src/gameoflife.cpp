#include <iostream>
#include <iomanip>
#include <bp_util.h>

#define HEIGHT 1000
#define WIDTH  1000

static double SURVIVE_LOW  = 2.0;
static double SURVIVE_HIGH = 3.0;
static double SPAWN        = 3.0;

using namespace std;

template <typename T>
void world(T state)
{
    #pragma omp parallel for collapse(2)
    for(int h=0; h<HEIGHT+2; ++h) {
        for(int w=0; w<WIDTH+2; ++w) {
            state[h][w] = (((h<2) and (h>WIDTH-3)) &&
                           ((w<2) and (w>HEIGHT-3)));
        }
    }
}

template <typename T>
void play(T state, int iterations, int version, int visualize)
{
    cout << state << SURVIVE_LOW << SURVIVE_HIGH << SPAWN << endl;
    cout << state << iterations << version << visualize << endl;
    
    T* cells, ul, um, ur, ml, mr, ll, lm, lr;
}

template <typename T>
void bench(bp_util_type& bp, const int I, const int V)
{
    auto state = new T[HEIGHT][WIDTH];              // Construct matrices
    world(state);

    bp.timer_start();                               // Start timer

    play(state, I, V, bp.args.visualize);

    bp.timer_stop();                                // Stop timer

    bp.print("gameoflife(cpp11_omp)");				// Print results..
    if (bp.args.verbose) {                          // ..and value.
        cout << fixed << setprecision(10)
             << "Result = " << endl;
    }
}

int main(int argc, char* argv[])
{
    bp_util_type bp = bp_util_create(argc, argv, 4);// Grab arguments
    if (bp.args.has_error) {
        return 1;
    }
    const int W = bp.args.sizes[0];
    const int H = bp.args.sizes[1];
    const int I = bp.args.sizes[2];
    const int V = bp.args.sizes[3];

    if (HEIGHT != H) {
        cout << "Multidimensional arrays in C11 does not support dynamic size, so it has to be: " << H << "." << endl;
        return 0;
    }
    if (WIDTH != W) {
        cout << "Multidimensional arrays in C11 does not support dynamic size, so it has to be: " << W << "." << endl;
        return 0;
    }

    bench<double>(bp, I, V);

    return 0;
}
