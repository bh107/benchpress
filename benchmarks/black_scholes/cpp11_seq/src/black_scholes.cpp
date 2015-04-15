#include <iostream>
#include <sstream>
#include <string>
#include <cmath>
#include <bp_util.h>

using namespace std;

int main(int argc, char* argv[])
{
    bp_util_type bp = bp_util_create(argc, argv, 2);
    if (bp.args.has_error) {
        return 1;
    }
    const int ydim = 1000;
    const int xdim = 1000;

    auto grid = new double[ydim][xdim];

    bp.timer_start();

    cout << "Whatever" << argc << " " << argv[0] << endl;

    cout << "Address " << &(grid[0][0]) << endl;
    cout << "Address " << &(grid[0]) << endl;;
    cout << "Address " << &(*grid) << endl;;

    bp.timer_stop();
    bp.print("black_scholes(cpp11_seq)");
        
    return 0;
}
