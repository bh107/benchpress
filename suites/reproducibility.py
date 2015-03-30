scripts   = [
    ('SOR',                   'sor',                   '--size=300*300*1000'),
    ('Jacobi Stencil',        'jacobi_stencil',        '--size=300*300*1000'),
    ('Heat Equation',         'heat_equation',         '--size=300*300*1000'),
    ('Shallow Water',         'shallow_water',         '--size=200*200*100'),
    ('N-Body',                'nbody',                 '--size=100*100'),
    ('N-Body Nice',           'nbody_nice',            '--size=500*100*100'),
    ('Black Scholes',         'black_scholes',         '--size=1000*100'),
    ('Matrix Multiplication', 'mxmul',                 '--size=500'),
#    ('Gauss Elimination',     'gauss',                 '--size=500'),
#    ('LU Factorization',      'lu',                    '--size=500'),
]

CPU_FLG = " -O3 -fstrict-aliasing -march=native -fopenmp "
CPU_IEEE_FULL = CPU_FLG + "-frounding-math -fsignaling-nans"
CPU_IEEE_RELAXED = CPU_FLG + "-ffast-math "

bohrium = {
    'bridges': [('Bohrium', 'python benchmark/python/{script}.py {args} --bohrium=True', None)],
    'engines': [\
                ('CPU1_DEFAULT',  'cpu', {'OMP_NUM_THREADS': 1, 'BH_VE_CPU_JIT_FUSION': 1, 'BH_CPU_COMPILER_FLG': CPU_FLG}),
                ('CPU32_DEFAULT', 'cpu', {'OMP_NUM_THREADS': 32,'BH_VE_CPU_JIT_FUSION': 1,'BH_CPU_COMPILER_FLG': CPU_FLG}),
                ('CPU1_RELAXED',  'cpu', {'OMP_NUM_THREADS': 1, 'BH_VE_CPU_JIT_FUSION': 1, 'BH_CPU_COMPILER_FLG': CPU_IEEE_RELAXED}),
                ('CPU32_RELAXED', 'cpu', {'OMP_NUM_THREADS': 32,'BH_VE_CPU_JIT_FUSION': 1,'BH_CPU_COMPILER_FLG': CPU_IEEE_RELAXED}),
                ('CPU1_FULL',     'cpu', {'OMP_NUM_THREADS': 1, 'BH_VE_CPU_JIT_FUSION': 1, 'BH_CPU_COMPILER_FLG': CPU_IEEE_FULL}),
                ('CPU32_FULL',    'cpu', {'OMP_NUM_THREADS': 32,'BH_VE_CPU_JIT_FUSION': 1,'BH_CPU_COMPILER_FLG': CPU_IEEE_FULL}),
                ('GPU',           'gpu', None)
               ],
    'scripts': scripts
}

numpy = {
    'bridges': [('NumPy', 'python benchmark/python/{script}.py {args} --bohrium=False', None)],
    'engines': [('CPU',   'cpu', None)],
    'scripts': scripts
}

suites = [numpy, bohrium]

