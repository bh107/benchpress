from default import *

scripts   = [
    ('Jacobi Stencil',        'jacobi_stencil',        '--size=3000*3000*100'),
    ('Shallow Water',         'shallow_water',         '--size=2000*2000*100'),
    ('Heat Equation',         'heat_equation',         '--size=3000*3000*100'),
    ('N-Body',                'nbody',                 '--size=1000*100'),
    ('Wire World',            'wireworld',             '--size=100*100'),
    ('Monte Carlo Pi',        'mc',                    '--size=10000000*100'),
    ('Black Scholes',         'black_scholes',         '--size=1000000*100'),
    ('Lattice Boltzmann D2Q9','lattice_boltzmann_D2Q9','--size=1000*1000*10'),
    ('Gauss Elimination',     'gauss',                 '--size=1000'),
    ('Convolution 3D',        'convolve_3d',           '--size=100'),
    ('Matrix Multiplication', 'mxmul',                 '--size=1000'),
    ('LU Factorization',      'lu',                    '--size=1000'),
]

bohrium = {
    'bridges': [python_bohrium],
    'engines': [('CPU', 'cpu', None),
                ('GPU', 'gpu', None)],
    'scripts': scripts,
}

numpy = {
    'bridges': [python_numpy],
    'engines': [('CPU', 'cpu', None)],
    'scripts': scripts,
}

suites = [numpy, bohrium]

