#include <iostream>
#include <sstream>
#include <string>
#include <cmath>
#include <bp_util.h>

using namespace std;

int main(int argc, char* argv[])
{
    if (2>argc) {
        cout << "usage: " << argv[0] << " --size=10000*10000*10 [--verbose]" << endl;
        return 1;
    }

    bp_arguments_type args = parse_args(argc, argv);        // Parse args

    const int width     = args.sizes[0];
    const int height    = args.sizes[1];

    const int ydim = 10000;
    if (ydim != height) {
        cout << "Multidimensional arrays in C11 does not support dynamic size, so it has to be: " << ydim << "." << endl;
        return 0;
    }

    const int xdim = 10000;
    if (xdim != width) {
        cout << "Multidimensional arrays in C11 does not support dynamic size, so it has to be: " << xdim << "." << endl;
        return 0;
    }

    const int max_iterations = args.sizes[2];

    printf(
        "Running heat_equation(cpp11_omp) --size=%d*%d*%i iterations.\n",
        ydim,
        xdim,
        max_iterations
    );

    double epsilon  = 0.005;
    double delta    = epsilon+1.0;

    auto grid = new double[ydim][xdim];
    auto temp = new double[ydim][xdim];

    for(int i=0; i<ydim; i++){      // Initialize the grid
        for(int j=0;j<xdim;j++){
            grid[i][j] = 0;
        }
    }
    for(int i=0; i<ydim; i++){      // And borders
        grid[i][0]      = -273.15;
        grid[i][xdim-1] = -273.15;
    }
    for(int i=0; i<xdim; i++){
        grid[0][i]      = -273.15;
        grid[ydim-1][i] = 40.0;
    }

    size_t start = bp_sample_time();
    auto iterations = 0;            // Compute the heat equation
    while(delta>epsilon) {
        ++iterations;
        delta = 0.0;
        for(int i=1; i<ydim-1; i++){
            #pragma omp parallel for reduction(+:delta)
            for(int j=1;j<xdim-1;j++){
                temp[i][j] = (grid[i-1][j] + grid[i+1][j] + grid[i][j] + grid[i][j-1] + grid[i][j+1])*0.2;
                delta += abs(temp[i][j] - grid[i][j]);
            }
        }

        #pragma omp parallel for collapse(2)
        for(int i=1;i<ydim-1; i++){
            for(int j=1;j<xdim-1;j++){
                grid[i][j] = temp[i][j];
            }
        }
        if (iterations>=max_iterations) {
            break;
        }
    }
    size_t stop = bp_sample_time();
    size_t elapsed = stop - start;

    printf("Ran heat_equation(cpp11_omp) iter: %d size: %d*%d elapsed-time: %lf\n", max_iterations, ydim, xdim, elapsed/(double)1000000.0);
    if (args.verbose) {                             // and values.
        cout << ", \"output\": [";
        for(int i=0; i<10; ++i) {
            for(int j=0; j<10; ++j) {
                cout << grid[i][j] << ", ";
            }
            cout << endl;
        }
        cout << "]";
    }

    return 0;
}
