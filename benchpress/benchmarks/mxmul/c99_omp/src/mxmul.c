#include <stdlib.h>
#include <stdio.h>
#include <bp_util.h>

void matmul(double* a, double* b, double* c, int m, int n, int k)
{
    #pragma omp parallel for collapse(2)
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            double sum = 0;
            for (int t = 0; t < k; t++) {
                sum += a[i*m +t] * b[t*n + j];
            }
            c[i*n+j] = sum;
        }
    }
}

int main(int argc, char* argv[])
{
    bp_util_type bp = bp_util_create(argc, argv, 1);        // Grab arguments
    if (bp.args.has_error) {
        return 1;
    }
    bp.timer_start();

    const int n = bp.args.sizes[0];
    const int nelements = n*n;
    
    double* a = (double*)malloc(sizeof(double)*nelements);  // Data setup
    double* b = (double*)malloc(sizeof(double)*nelements);
    double* c = (double*)malloc(sizeof(double)*nelements);
    for (int i=0; i<nelements; ++i) {
        a[i] = i / (float)nelements;
        b[i] = i / (float)nelements;
    }

    bp.timer_start();                                       // Start timer
    matmul(a, b, c, n, n, n);
    bp.timer_stop();

    bp.print("mxmul(c99_omp)");
    if (bp.args.verbose) {                                  // and values.
        double r = 0.0;
        #pragma omp parallel for reduction(+:r)
        for(int i=0; i<nelements; ++i) {
            r += c[i];
        }
        printf("Result = %.10f\n", r);
    }
    free(a);
    free(b);
    free(c);

    return 0;
}
