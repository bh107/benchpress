from default import *

scripts = [
    ('Black Scholes',   'black_scholes',    '--size=8000000*5'),
    ('Jacobi Stencil',  'jacobi_stencil',   '--size=8000*8000*3'),
    ('KNN',             'knn',              '--size=2000000*10*3'),
    ('Monte Carlo PI',  'mc',               '--size=20000000*10'),
    ('NBody',           'nbody',            '--size=3000*1'),
    ('Shallow Water',   'shallow_water',    '--size=3000*3000*5'),
    ('Swaption',        'LMM_swaption_vec', '--size=5000'),
    ('Bolzmann D2Q9',   'lattice_boltzmann_D2Q9', '--size=1400*1400*2'),
    ('Bolzmann 3D',     'lbm.3d',           '--size=120*100*100*5'),
    ('Matrix Mul',      'mxmul',            '--size=800'),
    ('SOR',             'sor',              '--size=4000*4000*5'),
    ('Wire World',      'wireworldnumpy',   '--size=5000*5000*5'),
    ('FFT',             'fftex',            '--size=18'),
    ('LU Factor.',      'lu',               '--size=6000*1'),
    ('Cloth',           'cloth',            '--size=3000*3000*1')
]

numpy = {
    'bridges':  [
        ('NumPy/Native', 'python benchmark/python/{script}.py {args}',
            {'VCACHE_LINES': "0", 'VCACHE_BYTES': "0"}),
        ('NumPy/Exact', 'python benchmark/python/{script}.py {args}',
            {'VCACHE_LINES': "10",
             'VCACHE_BYTES': "1048576000",
             "VCACHE_FIT_STRATEGY": 'EXACT'}),
        ('NumPy/First', 'python benchmark/python/{script}.py {args}',
            {'VCACHE_LINES': "10",
             'VCACHE_BYTES': "1048576000",
             "VCACHE_FIT_STRATEGY": 'FIRST'}),
        ('NumPy/Best',  'python benchmark/python/{script}.py {args}',
            {'VCACHE_LINES': "10",
             'VCACHE_BYTES': "1048576000",
             "VCACHE_FIT_STRATEGY": 'BEST'}),
    ],
    'scripts':  scripts,
}

suites = [
    numpy
]

