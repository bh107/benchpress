from benchpress.default import *

scripts = [
    ('Heat Equation',   'heat_equation',   '--size=100*100*1' ),
    ('nBody',           'nbody',           '--size=100*1'      ),
    ('nBody-NICE',      'nbody_nice',      '--size=100*100*1'  ),
    ('Shallow Water',   'shallow_water',   '--size=100*100*1' ),
    ('Black Scholes',   'black_scholes',   '--size=1000*1'   ),
    ('Jacobi Fixed',    'jacobi_fixed',    '--size=1000*1'   ),
    ('SOR',             'sor',             '--size=100*100*1'   ),
    ('MonteCarlo',      'montecarlo_pi',   '--size=1000*1'   ),
    ('GameOfLife',      'gameoflife',      '--size=100*100*1*1'   ),
    ('Gauss',           'gauss',           '--size=100*100*1'   ),
    ('LU',              'lu',              '--size=100*100*1'   ),
    ('Synth',           'synth',           '--size=100*1'   ),
    ('point27',         'point27',         '--size=100*1'   ),
    ('rosenbrock',      'rosenbrock',      '--size=100*1'   ),
    ('wisp',            'wisp',            '--size=100*100*1'   ),
#    ('lbm_3d',          'lbm_3d',          '--size=10*10*10*1'   ),
#    ('lbm_2d',          'lbm_2d',          '--size=10*10*1'   ),
#    ('wireworld',       'wireworld',       '--size=10*1'   ),
]

scripts = [
    ('Black Scholes',           'black_scholes',            '--size=5000000*10'),
    ('Game of Life v1',         'gameoflife',               '--size=10000*10000*10*1'),
    ('Game of Life v2',         'gameoflife',               '--size=10000*10000*10*2'),
    ('Gauss Elimination',       'gauss',                    '--size=2000'),
    ('Heat Equation',           'heat_equation',            '--size=14000*14000*10'),
    ('Heat Equation FI',        'heat_equation_fixed',      '--size=14000*14000*10'),
    ('Jacobi',                  'jacobi',                   '--size=14000*10'),
    ('Jacobi FI',               'jacobi_fixed',             '--size=14000*10'),
    ('kNN Naive 1',             'knn_naive',                '--size=20000000*64*10'),
    ('Leibnitz PI',             'leibnitz_pi',              '--size=100000000'),
    ('LU Factorization',        'lu',                       '--size=2000'),
    ('Monte Carlo PI',          'montecarlo_pi',            '--size=50000000*10'),
    ('Matrix Multiplication',   'mxmul',                    '--size=1000'),
    ('NBody',                   'nbody',                    '--size=2000*10'),
    ('NBody Nice',              'nbody_nice',               '--size=10*2000000*10'),
    ('1D Stencil',              'ndstencil',                '--size=27*10*1'),
    ('2D Stencil',              'ndstencil',                '--size=27*10*2'),
    ('3D Stencil',              'ndstencil',                '--size=27*10*3'),
    ('27 Point Stencil',        'point27',                  '--size=150*150'),
    ('Shallow Water',           'shallow_water',            '--size=5000*5000*10'),
    ('SOR',                     'sor',                      '--size=5000*5000*10'),
    ('Synthetic',               'synth',                    '--size=200000000*10'),
    ('Synthetic Inplace',       'synth_inplace',            '--size=200000000*10'),
    ('Synthetic Stream #0 Ones',    'synth_stream',  '--size=50000000*20*0'),
    ('Synthetic Stream #1 Range',   'synth_stream',  '--size=50000000*10*1'),
    ('Synthetic Stream #2 Random',  'synth_stream',  '--size=50000000*10*2'),
    ('Water-Ice Simulation',        'wisp',                 '--size=1000*1000*10'),
    #('Rosenbrock',              'rosenbrock',               '--size=100000000*10'),
    #('Pricing American',        'pricing',                  '--size=100'),
    #('Wireworld',               'wireworld',                '--size=10*10')
    #('Lattice Boltzmann D2Q9',  'lattice_boltzmann_D2Q9',   '--size=100*100*10'),
    #('kNN',                     'k_nearest_neighbor',       '--size=100'),
    #('Lattice Boltzmann 3D',    'lbm_3d',                   '--size=150*150*150*10'),
]

bh_stack_cpu_pricer = [
    [('default',    'bridge',       None)],
    [('bccon',      'bccon',        None)],
    [('bcexp',      'bcexp',        None)],
    [
        ('single',     'singleton',   {"BH_SINGLETON_FUSE_CACHE": "true"}),
        ('topo',       'topological', {"BH_TOPOLOGICAL_FUSE_CACHE": "true"}),
        ('greedy',     'greedy',      {"BH_GREEDY_FUSE_CACHE": "true"}),
        ('optimal',    'optimal',     {"BH_OPTIMAL_FUSE_CACHE": "true"}),
    ],
    [('node',       'node',         None)],
    [('pricer',     'pricer',       None)],
    [('cpu',        'cpu',  {"BH_CPU_JIT_LEVEL": "3", "OMP_NUM_THREADS":4})],

]

bh_cpu_pricer_suite = {
    'scripts': scripts,
    'launchers':  [python_bohrium],
    'bohrium': bh_stack_cpu_pricer
}

suites = [
    bh_cpu_pricer_suite,
]

