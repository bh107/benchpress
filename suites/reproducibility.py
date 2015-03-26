scripts   = [
    ('SOR',                   'sor',                   '--size=300*300*10'),
    ('Jacobi Stencil',        'jacobi_stencil',        '--size=300*300*10'),
    ('Shallow Water',         'shallow_water',         '--size=200*200*10'),
    ('Heat Equation',         'heat_equation',         '--size=300*300*100'),
    ('N-Body',                'nbody',                 '--size=100*100'),
    ('N-Body Nice',           'nbody_nice',            '--size=500*100*10'),
    ('Black Scholes',         'black_scholes',         '--size=10000*100'),
    ('Gauss Elimination',     'gauss',                 '--size=500'),
    ('Matrix Multiplication', 'mxmul',                 '--size=500'),
    ('LU Factorization',      'lu',                    '--size=500'),
]

bohrium = {
    'bridges': [('Bohrium', 'python benchmark/python/{script}.py {args} --bohrium=True', None)],
    'engines': [\
                ('CPU_OMP1',  'cpu', {'OMP_NUM_THREADS': 1}),
                ('CPU_OMP32', 'cpu', {'OMP_NUM_THREADS': 32}),
                ('GPU', 'gpu', None)
               ],
    'scripts': scripts
}

numpy = {
    'bridges': [('NumPy', 'python benchmark/python/{script}.py {args} --bohrium=False', None)],
    'engines': [('CPU',   'cpu', None)],
    'scripts': scripts
}

suites = [numpy, bohrium]

