from benchpress.default import *

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
    #('Water-Ice Simulation',        'wisp',                 '--size=1000*1000*10'),
    #('Rosenbrock',              'rosenbrock',               '--size=100000000*10'),
    #('Pricing American',        'pricing',                  '--size=100'),
    #('Wireworld',               'wireworld',                '--size=10*10')
    #('Lattice Boltzmann D2Q9',  'lattice_boltzmann_D2Q9',   '--size=100*100*10'),
    #('kNN',                     'k_nearest_neighbor',       '--size=100'),
    #('Lattice Boltzmann 3D',    'lbm_3d',                   '--size=150*150*150*10'),
]

def fuse_cache(value):
    return {\
            "BH_SINGLETON_FUSE_CACHE": value,
            "BH_TOPOLOGICAL_FUSE_CACHE": value,
            "BH_GREEDY_FUSE_CACHE": value,
            "BH_OPTIMAL_FUSE_CACHE": value\
            }

bh_stack_cpu_pricer = [
    [('default',    'bridge',       None)],
    [('bccon',      'bccon',        None)],
    [('bcexp',      'bcexp',        None)],
    [
        ('Singleton',  'singleton',   None),
        ('Naive',      'topological', None),
        ('Greedy',     'greedy',      None),
        ('Optimal',    'optimal',     None),
    ],
    [
        ('filecache',  'node', fuse_cache("true")),
        ('memcache',  'node', fuse_cache("")),
        ('nocache',  'node', fuse_cache("false")),
    ],
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

