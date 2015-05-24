#include <iostream>
#include <iomanip>
#include <bxx/bohrium.hpp>
#include <bp_util.h>

static double SURVIVE_LOW  = 2.0;
static double SURVIVE_HIGH = 3.0;
static double SPAWN        = 3.0;

using namespace std;
using namespace bxx;

template <typename T>
void world(int height, int width, multi_array<T>& state)
{
    state = ones<T>(height+2, width+2);
    state[_(2,-3)][_(2,-3)] = (T)0;
}

template <typename T>
void play(multi_array<T>& state, int iterations, int version, int visualize)
{
    multi_array<T> cells, ul, um, ur, ml, mr, ll, lm, lr;
    cells   = state[_(1,-2)][_(1,-2)];
    ul      = state[_(0,-3)][_(0,-3)];
    um      = state[_(0,-3)][_(1,-2)];
    ur      = state[_(0,-3)][_(2,-1)];
    ml      = state[_(1,-2)][_(0,-3)];
    mr      = state[_(1,-2)][_(2,-1)];
    ll      = state[_(2,-1)][_(0,-3)];
    lm      = state[_(2,-1)][_(1,-2)];
    lr      = state[_(2,-1)][_(2,-1)];

    multi_array<T> neighbors;
    if (1 == version) {             //  This is the first implementation of the game rules.
        multi_array<T> live, dead;
        multi_array<bool> stay, spawn;
        for (int i=0; i<iterations; ++i) {
            neighbors   = ul + um + ur + ml + mr + ll + lm + lr;// Count neighbors
            live        = neighbors * cells;                    // Extract live cells neighbors
                                                                // Find cells that stay alive
            stay        = (SURVIVE_LOW <= live) && 
                          (live <= SURVIVE_HIGH);  
            dead        = neighbors * as<T>(cells == (T)0);     // Extract dead cell neighbors
            spawn       = dead == SPAWN;                        // Find spawning cells
            
            cells(as<T>(stay || spawn));                        // Update state

            if (visualize) {
                plot_surface(state, 1, 16, 1, 0);
            }
        }
    } else if (2 == version) {      // This is an optimized version of the game rules
        multi_array<T> c1, c2;
        for (int i=0; i<iterations; ++i) {
            neighbors = ul + um + ur + ml + mr + ll + lm + lr;  // Count neighbors

            c1 = as<T>(neighbors == SURVIVE_LOW);               // Life conditions
            c2 = as<T>(neighbors == SPAWN);

            cells(cells * c1 + c2);                             // Update

            if (visualize) {
                plot_surface(state, 1, 16, 1, 0);
            }
        }
    } else {
        throw std::runtime_error("Unsupported version.");
    }
}

template <typename T>
void bench(bp_util_type& bp, const int W, const int H, const int I, const int V)
{
    multi_array<T> state;                           // Construct matrices
    world(H, W, state);

    Runtime::instance().flush();
    bp.timer_start();                               // Start timer

    play(state, I, V, bp.args.visualize);

    Runtime::instance().flush();
    bp.timer_stop();                                // Stop timer

    bp.print("gameoflife(cpp11_bxx)");				// Print results..
    if (bp.args.verbose) {                          // ..and value.
        cout << fixed << setprecision(10)
             << "Result = " << scalar(sum(state)) << endl;
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

    bench<double>(bp, W, H, I, V);

    return 0;
}
