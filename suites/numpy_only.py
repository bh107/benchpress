from default import *

suites = [
    {
        'bridges':  [
            ('NumPy', 'taskset -c 0 python `bp_info --benchmarks`/{script}/python_numpy/{script}.py {args}', None)
        ],
        'scripts':  [
            ('Black Scholes',               'black_scholes',    '--size=1000000*10'),
            ('Game of Life',                'gameoflife',       '--size=10000*10000*10'),
            ('Gauss Elimination',           'gauss',            '--size=500'),
            ('Heat Equation',               'heat_equation',    '--size=5000*5000*10'),
            ('Jacobi Solve',                'jacobi_solve',     '--size=5000*5000*10'),
            ('Jacobi Stencil',              'jacobi_stencil',   '--size=5000*5000*10'),
            ('kNN Naive 1',                 'knn_naive1',       '--size=10000000*14*10'),
            ('Lattice Boltzmann 3D',        'lbm_3d',           '--size=50*50*50*10'),
            ('LU Factorization',            'lu',               '--size=1000'),
            ('Monte Carlo PI',              'mc',               '--size=50000000*10'),
            ('Matrix Multiplication',       'mxmul',            '--size=250'),
            ('nbody',                       'nbody',            '--size=2000*10'),
            ('1D Stencil',                  'ndstencil',        '--size=27*10*1'),
            ('2D Stencil',                  'ndstencil',        '--size=27*10*2'),
            ('3D Stencil',                  'ndstencil',        '--size=27*10*3'),
            ('Shallow Water',               'shallow_water',    '--size=5000*5000*10'),
            ('SOR',                         'sor',              '--size=5000*5000*10'),
            ('Synthetic',                   'synth',            '--size=200000000*10'),
            ('Synthetic Inplace',           'synth_inplace',    '--size=200000000*10'),
            ('Synthetic Stream #0 Ones',    'synth_stream',     '--size=50000000*20*0'),
            ('Synthetic Stream #1 Range',   'synth_stream',     '--size=50000000*10*1'),
            ('Synthetic Stream #2 Random',  'synth_stream',     '--size=50000000*10*2'),
        ],
    }
]

