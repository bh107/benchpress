from default import *

scripts = [
    #('LMM Swaption',            'LMM_swaption_vec',         '--size=1000*1000'),
    ('Black Scholes',           'black_scholes',            '--size=5000000*10'),
    #('Convolution',             'convolve',                 '--size=10'),
    #('Convolution 2D',          'convolve_2d',              '--size=10'),
    #('Convolution 3D',          'convolve_3d',              '--size=10'),
    #('Convolution Sep',         'convolve_seperate_std',    '--size=11*11'),
    ('Game of Life',            'gameoflife',               '--size=10000*10000*10'),
    ('Gauss Elimination',       'gauss',                    '--size=2000'),
    ('Heat Equation',           'heat_equation',            '--size=10000*10000*10'),
    #('Jacobi',                  'jacobi',                   '--size=2'),
    ('Jacobi Fixed I',          'jacobi_fixed',             '--size=10000*10'),
    ('Jacobi Stencil',          'jacobi_stencil',           '--size=10000*10000*10'),
    #('kNN',                     'k_nearest_neighbor',       '--size=100'),
    ('kNN Naive 1',             'knn_naive1',               '--size=20000000*20*10'),
    ('kNN Naive 2',             'knn_naive2',               '--size=2000000*20*10'),
    #('Lattice Boltzmann D2Q9',  'lattice_boltzmann_D2Q9',   '--size=100*100*10'),
    ('Lattice Boltzmann 3D',    'lbm_3d',                   '--size=150*150*150*10'),
    ('LU Factorization',        'lu',                       '--size=2000'),
    ('Monte Carlo PI',          'mc',                       '--size=50000000*10'),
    ('Matrix Multiplication',   'mxmul',                    '--size=2000'),
    ('nbody',                   'nbody',                    '--size=2000*10'),
    ('1D Stencil',              'ndstencil',                '--size=27*10*1'),
    ('2D Stencil',              'ndstencil',                '--size=27*10*2'),
    ('3D Stencil',              'ndstencil',                '--size=27*10*3'),
    ('27 Point Stencil',        'point27',                  '--size=150*150'),
    #('Pricing American',        'pricing',                  '--size=100'),
    ('Shallow Water',           'shallow_water',            '--size=5000*5000*10'),
    ('SOR',                     'sor',                      '--size=5000*5000*10'),
    ('Synthetic',               'synth',                    '--size=200000000*10'),
    ('Synthetic Inplace',       'synth_inplace',            '--size=200000000*10'),
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
        ('fusion_01',   'cpu', {'BH_VE_CPU_JIT_FUSION': '1', 'OMP_NUM_THREADS': '1' , 'GOMP_CPU_AFFINITY': "0"   }),
        ('fusion_02',   'cpu', {'BH_VE_CPU_JIT_FUSION': '1', 'OMP_NUM_THREADS': '2' , 'GOMP_CPU_AFFINITY': "0-1" }),
        ('fusion_04',   'cpu', {'BH_VE_CPU_JIT_FUSION': '1', 'OMP_NUM_THREADS': '4' , 'GOMP_CPU_AFFINITY': "0-3" }),
        ('fusion_08',   'cpu', {'BH_VE_CPU_JIT_FUSION': '1', 'OMP_NUM_THREADS': '8' , 'GOMP_CPU_AFFINITY': "0-7" }),
        ('fusion_16',   'cpu', {'BH_VE_CPU_JIT_FUSION': '1', 'OMP_NUM_THREADS': '16', 'GOMP_CPU_AFFINITY': "0-15"}),
        ('fusion_32',   'cpu', {'BH_VE_CPU_JIT_FUSION': '1', 'OMP_NUM_THREADS': '32', 'GOMP_CPU_AFFINITY': "0-31"}),

        ('omp_01',  'cpu', {'BH_VE_CPU_JIT_FUSION': '0', 'OMP_NUM_THREADS': '1'     , 'GOMP_CPU_AFFINITY': "0"   }),
        ('omp_02',  'cpu', {'BH_VE_CPU_JIT_FUSION': '0', 'OMP_NUM_THREADS': '2'     , 'GOMP_CPU_AFFINITY': "0-1" }),
        ('omp_04',  'cpu', {'BH_VE_CPU_JIT_FUSION': '0', 'OMP_NUM_THREADS': '4'     , 'GOMP_CPU_AFFINITY': "0-3" }),
        ('omp_08',  'cpu', {'BH_VE_CPU_JIT_FUSION': '0', 'OMP_NUM_THREADS': '8'     , 'GOMP_CPU_AFFINITY': "0-7" }),
        ('omp_16',  'cpu', {'BH_VE_CPU_JIT_FUSION': '0', 'OMP_NUM_THREADS': '16'    , 'GOMP_CPU_AFFINITY': "0-15"}),
        ('omp_32',  'cpu', {'BH_VE_CPU_JIT_FUSION': '0', 'OMP_NUM_THREADS': '32'    , 'GOMP_CPU_AFFINITY': "0-31"}),
    ],
    'scripts':  scripts
}

suites = [
    numpy,
    bohrium
]

