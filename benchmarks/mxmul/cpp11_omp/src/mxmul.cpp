#include <iostream>
#include <iomanip>
#include <bp_util.h>

#define N 2000

using namespace std;

template <typename T>
void matmul(T a, T b, T c, int m, int n, int k)
{
    #pragma omp parallel for collapse(2)
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            double sum = 0;
            for (int t = 0; t < k; t++) {
                sum += a[i][t] * b[t][j];
            }
            c[i][j] = sum;
        }
    }
}

int main(int argc, char* argv[])
{
    bp_util_type bp = bp_util_create(argc, argv, 1);    // Grab arguments
    if (bp.args.has_error) {
        return 1;
    }
    bp.timer_start();

    const int n = bp.args.sizes[0];
    const int nelements = n*n;

    if (n != N) {
        cout << "HEJ " << n << " " << N << endl;
    }
    
    auto a = new double[N][N];  // Data setup
    auto b = new double[N][N];
    auto c = new double[N][N];
    int range = 0;
    for (int i=0; i<n; ++i) {
        for (int j=0; j<n; ++j) {
            a[i][j] = (range++) / (float)nelements;
            b[i][j] = (range) / (float)nelements;
        }
    }

    bp.timer_start();                                       // Start timer
    matmul(a, b, c, n, n, n);
    bp.timer_stop();

    bp.print("mxmul(cpp11_omp)");
    if (bp.args.verbose) {                                  // and values.
        double r = 0.0;
        #pragma omp parallel for collapse(2) reduction(+:r)
        for(int i=0; i<n; ++i) {
            for(int j=0; j<n; ++j) {
                r += c[i][j];
            }
        }
        cout << fixed << setprecision(10)
			 << "Result = " << r << endl;
    }

    delete a; 
    delete b; 
    delete c; 

    return 0;
}
