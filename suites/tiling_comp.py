from default import scripts, engines

# Run on all default-script with numpy, simple and score
# with default parameters.

suite = {
    'scripts': [
        ('BlackScholes-c',   '../ccode/bscholes',  '2000000 4'),
        ('Black Scholes',   'bscholes.py',  '--size=2000000*4'),
        ('Jacobi-c', '../ccode/jacobi', '7000 4'),
        ('Jacobi Iterative - Reduce', 'jacobi.iterative.reduc.py', '--size=7000*7000*4'),
        
    ],
    'engines': [engines[2]]
}
