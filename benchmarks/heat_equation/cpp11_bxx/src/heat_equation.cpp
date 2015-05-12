#include <iostream>
#include <iomanip>
#include <bp_util.h>
#include <bxx/bohrium.hpp>

using namespace std;
using namespace bxx;

template <typename T>
void init_grid(multi_array<T>& grid, int height, int width)
{
    grid = zeros<T>(height+2, width+2);
    grid[_(0,-1)][0]    = (T)(-273.15);
    grid[_(0,-1)][-1]   = (T)(-273.15);
    grid[-1][_(0,-1)]   = (T)(-273.15);
    grid[0][_(0,-1)]    = (T)(40);
}

template <typename T>
uint32_t jacobi(multi_array<T>& grid, T epsilon, uint32_t max_iterations, bool visualize)
{
    multi_array<T> center, north, east, west, south;
    center  = grid[_(1,-2)][_(1,-2)];
    north   = grid[_(0,-3)][_(1,-2)];
    east    = grid[_(1,-2)][_(2,-1)];
    west    = grid[_(1,-2)][_(0,-3)];
    south   = grid[_(2,-1)][_(1,-2)];

    T delta = epsilon + 1.0;
    uint32_t iteration = 0;
    while(delta>epsilon) {
        ++iteration;
        multi_array<T> work;
        work = ((T)0.2)*(center+north+east+west+south);
        delta = scalar<T>(sum(abs(work-center)));
        center(work);

        if ((max_iterations > 0) && (iteration >= max_iterations)) {
            break;
        }
        if (visualize) {
            plot_surface(grid, 0, 0, 200, -200);
        }
    }
    return iteration;
}

int main(int argc, char* argv[])
{
    bp_util_type bp = bp_util_create(argc, argv, 3);// Grab arguments
    if (bp.args.has_error) {
        return 1;
    }
    const int height = bp.args.sizes[0];
    const int width = bp.args.sizes[1];
    const int max_iterations = bp.args.sizes[2];
    int iterations = 0;

    multi_array<double> grid;
    init_grid(grid, width, height);
    
    bp.timer_start();                               // Start timer
    iterations = jacobi(                            // Run benchmark
        grid,
        0.005,
        max_iterations,
        bp.args.visualize
    );
    bp.timer_stop();                                // Stop timer
    bp.print("heat_equation(cpp11_bxx)");
    if (bp.args.verbose) {                          // ..and value.
        cout << fixed << setprecision(11)
			 << "Iterations = " << iterations << endl;
    }

    return 0;
}
