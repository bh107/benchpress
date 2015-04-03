from default import *

# TODO: Adapt this to the benchpress after the "makeover".

scripts = [
    ('Jacobi Stencil',  'jacobi_stencil',   '--size=8000*8000*3'),
    ('Cloth',           'cloth',            '--size=3000*3000*1'),
    ('SOR',             'sor',              '--size=4000*4000*5'),
    ('Shallow Water',   'shallow_water',    '--size=3000*3000*5'),
    ('LU Factor.',      'lu',               '--size=6000*1'),
    ('KNN',             'knn',              '--size=2000000*10*3'),
    ('Monte Carlo PI',  'mc',               '--size=20000000*10'),
    ('NBody',           'nbody',            '--size=3000*1'),
    ('Swaption',        'LMM_swaption_vec', '--size=5000'),
    ('Bolzmann D2Q9',   'lattice_boltzmann_D2Q9', '--size=1400*1400*2'),
    ('Bolzmann 3D',     'lbm.3d',           '--size=120*100*100*5'),
    ('Matrix Mul',      'mxmul',            '--size=800'),
    ('Wire World',      'wireworldnumpy',   '--size=5000*5000*5'),
    ('FFT',             'fftex',            '--size=18'),
    ('Black Scholes',   'black_scholes',    '--size=8000000*5'),
]
numpy = {
    'bridges':  [
        ('NumPy/Native', 'python benchmark/python/{script}.py {args}', {'VCACHE_LINES': "0"}),

        ('NumPy/MMAP_100M', 'python benchmark/python/{script}.py {args}',
            {'VCACHE_LINES': "0", "MALLOC_MMAP_MAX": "0", "MALLOC_TRIM_THRESHOLD_": "104857600"} ),
        ('NumPy/MMAP_512M', 'python benchmark/python/{script}.py {args}',
            {'VCACHE_LINES': "0", "MALLOC_MMAP_MAX": "0", "MALLOC_TRIM_THRESHOLD_": "536870912"} ),
        ('NumPy/MMAP_1G', 'python benchmark/python/{script}.py {args}',
            {'VCACHE_LINES': "0", "MALLOC_MMAP_MAX": "0", "MALLOC_TRIM_THRESHOLD_": "1048576000"} ),

    ],
    'scripts':  scripts,
}

suites = [
    numpy
]

