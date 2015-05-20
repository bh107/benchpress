#include <iostream>
#include <sstream>
#include <string>
#include <cmath>
#include <bp_util.h>

#define xdim 14000
#define ydim 14000

using namespace std;

template <typename T>
void solve(T grid, double epsilon, int max_iterations)
{
    T temp = new double[ydim][xdim];

    double delta = epsilon+1.0;
    int iterations = 0;            // Compute the heat equation

    while(delta>epsilon) {
        ++iterations;

        #pragma omp parallel for reduction(+:delta) collapse(2)
        for (int i=1; i<ydim-1; i++) {
            for(int j=1;j<xdim-1;j++) {
                temp[i][j] = (grid[i-1][j] + grid[i+1][j] + grid[i][j] + grid[i][j-1] + grid[i][j+1])*0.2;
                delta += abs(temp[i][j] - grid[i][j]);
            }
        }

        #pragma omp parallel for collapse(2)
        for (int i=1;i<ydim-1; i++) {
            for(int j=1;j<xdim-1;j++) {
                grid[i][j] = temp[i][j];
            }
        }

        if (iterations>=max_iterations) {
            break;
        }
    }
}

int main(int argc, char* argv[])
{
    bp_util_type bp = bp_util_create(argc, argv, 3);// Grab arguments
    if (bp.args.has_error) {
        return 1;
    }
    bp.timer_start();

    const int width     = bp.args.sizes[0];
    const int height    = bp.args.sizes[1];

    if (ydim != height) {
        cout << "Multidimensional arrays in C11 does not support dynamic size, so it has to be: " << ydim << "." << endl;
        return 0;
    }

    if (xdim != width) {
        cout << "Multidimensional arrays in C11 does not support dynamic size, so it has to be: " << xdim << "." << endl;
        return 0;
    }

    const int max_iterations = bp.args.sizes[2];

    double epsilon  = 0.005;

    auto grid = new double[ydim][xdim];
    #pragma omp parallel for collapse(2)
    for (int i=0; i<ydim; i++) {      // Initialize the grid
        for (int j=0;j<xdim;j++) {
            grid[i][j] = 0;
        }
    }
    for (int i=0; i<ydim; i++) {      // And borders
        grid[i][0]      = -273.15;
        grid[i][xdim-1] = -273.15;
    }
    for (int i=0; i<xdim; i++) {
        grid[0][i]      = -273.15;
        grid[ydim-1][i] = 40.0;
    }

    bp.timer_start();                                   // Start timer
    solve(grid, epsilon, max_iterations);
    bp.timer_stop();

    bp.print("heat_equation(cpp11_omp)");
    if (bp.args.verbose) {                             // and values.
        cout << ", \"output\": [";
        for (int i=0; i<10; ++i) {
            for (int j=0; j<10; ++j) {
                cout << grid[i][j] << ", ";
            }
            cout << endl;
        }
        cout << "]";
    }

    return 0;
}
