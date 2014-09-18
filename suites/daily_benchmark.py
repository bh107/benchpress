from default import *

scripts   = [
    ('Jacobi Stencil', 'jacobi_stencil', '--size=100*100*10'),
    ('Shallow Water',  'shallow_water',  '--size=100*100*10'),
    ('N-Body',         'nbody',          '--size=100*10'),
]

bohrium = {
    'bridges': [('Bohrium', 'python benchmark/Python/{script}.py {args} --bohrium=True', None)],
    'engines': [('CPU', 'cpu', None),
                ('GPU', 'gpu', None)],
    'scripts': scripts,
}

numpy = {
    'bridges': [('Bohrium', 'python benchmark/Python/{script}.py {args} --bohrium=True', None)],
    'engines': [('CPU', 'cpu', None)],
    'scripts': scripts,
}

suites = [numpy, python]

