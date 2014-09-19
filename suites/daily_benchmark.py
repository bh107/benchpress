from default import *

scripts   = [
    ('Jacobi Stencil',        'jacobi_stencil',        '--size=100*100*10'),
    ('Shallow Water',         'shallow_water',         '--size=100*100*10'),
    ('Heat Equation',         'heat_equation',         '--size=100*100*10'),
    ('N-Body',                'nbody',                 '--size=100*10'),
    ('Snakes and Ladders',    'snakes_and_ladders',    '--size=100*10'),
    ('Wire World',            'wireworld',             '--size=10*10'),
    ('Monte Carlo Pi',        'mc',                    '--size=100*10'),
    ('Lattice Boltzmann D2Q9','lattice_boltzmann_D2Q9','--size=100*100*10'),
    ('Gauss Elimination',     'gauss',                 '--size=100'),
    ('Convolution 2D',        'convolve_2d',           '--size=5'),
    ('Convolution 3D',        'convolve_3d',           '--size=5'),
    ('Matrix Multiplication', 'mxmul',                 '--size=100'),
    ('LU Factorization',      'lu',                    '--size=100'),
]

bohrium = {
    'bridges': [('Bohrium', 'python benchmark/Python/{script}.py {args} --bohrium=True', None)],
    'engines': [('CPU', 'cpu', None),
                ('GPU', 'gpu', None)],
    'scripts': scripts,
}

numpy = {
    'bridges': [('NumPy', 'python benchmark/Python/{script}.py {args} --bohrium=False', None)],
    'engines': [('CPU', 'cpu', None)],
    'scripts': scripts,
}

suites = [numpy, bohrium]

