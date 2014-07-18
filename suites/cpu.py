from default import *

scripts = [
    #('LMM Swaption',            'LMM_swaption_vec',         '--size=1000*1000'),
    ('Black Scholes',           'black_scholes',            '--size=2000000*5'),
    #('Convolution',             'convolve',                 '--size=10'),
    #('Convolution 2D',          'convolve_2d',              '--size=10'),
    #('Convolution 3D',          'convolve_3d',              '--size=10'),
    ('Convolution Sep',         'convolve_seperate_std',    '--size=11*11'),
    ('Game of Life',            'gameoflife',               '--size=501*500*5'),
    ('Gauss Elimination',       'gauss',                    '--size=100'),
    ('Heat Equation',           'heat_equation',            '--size=100*100*2'),
    #('Jacobi',                  'jacobi',                   '--size=2'),
    ('Jacobi Fixed I',          'jacobi_fixed',             '--size=10*10'),
    ('Jacobi Stencil',          'jacobi_stencil',           '--size=8000*8000*10'),
    #('kNN',                     'k_nearest_neighbor',       '--size=100'),
    ('kNN Naive 1',             'knn.naive',                '--size=100*10*2'),
    #('kNN Naive 2',             'knn',                      '--size=100*10*2'),
    #('Lattice Boltzmann D2Q9',  'lattice_boltzmann_D2Q9',   '--size=100*100*10'),
    ('Lattice Boltzmann 3D',    'lbm.3d',                   '--size=10*10*10*2'),
    ('LU Factorization',        'lu',                       '--size=10'),
    ('Monte Carlo PI',          'mc',                       '--size=10000000*10'),
    ('Matrix Multiplication',   'mxmul',                    '--size=10'),
    #('nbody',                   'nbody',                    '--size=10*10'),
    ('ND Stencil',              'ndstencil',                '--size=10*10*3'),
    ('27 Point Stencil',        'point27',                  '--size=10*10'),
    ('Pricing American',        'pricing',                  '--size=100'),
    ('Shallow Water',           'shallow_water',            '--size=1500*1500*5'),
    ('SOR',                     'sor',                      '--size=10*10*2'),
    ('Synthetic',               'synth',                    '--size=10*10'),
    #('Wireworld',               'wireworld',                '--size=10*10')
]

managers= [('node', 'node', '', None)]

numpy = {
    'bridges':  [('NumPy/Native', 'python benchmark/Python/{script}.py {args} --bohrium=False', None)],
    'scripts':  scripts,
}

bohrium = {
    'bridges':  [('NumPy/Bohrium', 'python benchmark/Python/{script}.py {args} --bohrium=True', None)],
    'managers': [('node',  'node', '',  None) ],
    'engines':  [
        ('omp1',    'cpu', {'BH_VE_CPU_JIT_FUSION': '0', 'OMP_NUM_THREADS': '1'}),
        ('omp2',    'cpu', {'BH_VE_CPU_JIT_FUSION': '0', 'OMP_NUM_THREADS': '2'}),
        ('omp4',    'cpu', {'BH_VE_CPU_JIT_FUSION': '0', 'OMP_NUM_THREADS': '4'}),
        ('omp8',    'cpu', {'BH_VE_CPU_JIT_FUSION': '0', 'OMP_NUM_THREADS': '8'}),
        ('omp16',   'cpu', {'BH_VE_CPU_JIT_FUSION': '0', 'OMP_NUM_THREADS': '16'}),
        ('omp32',   'cpu', {'BH_VE_CPU_JIT_FUSION': '0', 'OMP_NUM_THREADS': '32'}),
    ],
    'scripts':  scripts
}

suites = [
    bohrium,
    numpy
]

