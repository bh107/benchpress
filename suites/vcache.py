from default import *

scripts = [
    ('LU Factor.',      'lu',               '--size=500*499'),
    ('Jacobi Stencil',  'jacobi_stencil',   '--size=10000*4000*10'),
    ('Shallow Water',   'shallow_water',    '--size=3000*3000*5'),
    ('Cloth',           'cloth',            '--size=3000*3000*1'),
    ('SOR',             'sor',              '--size=4000*4000*5'),
    ('Black Scholes',   'black_scholes',    '--size=8000000*5'),
    ('KNN',             'knn',              '--size=2000000*10*3'),
    ('Monte Carlo PI',  'mc',               '--size=20000000*10'),
    ('NBody',           'nbody',            '--size=3000*1'),
    ('Swaption',        'LMM_swaption_vec', '--size=1000'),
    ('Bolzmann D2Q9',   'lattice_boltzmann_D2Q9', '--size=800*800*5'),
    ('Bolzmann 3D',     'lbm.3d',           '--size=120*100*100*5'),
    ('Matrix Mul',      'mxmul',            '--size=800'),
    ('Wire World',      'wireworldnumpy',   '--size=5000*5000*5'),
    ('FFT',             'fftex',            '--size=18'),
]

numpy = {
    'bridges':  [
        ('NumPy/Native', 'python benchmark/python/{script}.py {args}',
            {'VCACHE_LINES': "0", 'VCACHE_BYTES': "0"}),
        ('NumPy/VCache_100M', 'python benchmark/python/{script}.py {args}',
            {'VCACHE_LINES': "10",'VCACHE_BYTES': "104857600"} ),
        ('NumPy/VCache_512M', 'python benchmark/python/{script}.py {args}',
            {'VCACHE_LINES': "10",'VCACHE_BYTES': "536870912"} ),
        ('NumPy/VCache_1G', 'python benchmark/python/{script}.py {args}',
            {'VCACHE_LINES': "10",'VCACHE_BYTES': "1048576000"} ),

    ],
    'scripts':  scripts,
}

suites = [
    numpy
]

