from benchpress.default import *
import copy

scripts_cpu = [
    ('Black Scholes',           'black_scholes',            '--size=15000000*20'),
    ('Game of Life',            'gameoflife',               '--size=10000*10000*20*2'),
    ('Heat Equation',           'heat_equation',            '--size=12000*12000*20'),
    ('Leibnitz PI',             'leibnitz_pi',              '--size=100000000*20'),
    ('Gauss Elimination',       'gauss',                    '--size=2800'),
    ('LU Factorization',        'lu',                       '--size=2800'),
    ('Monte Carlo PI',          'montecarlo_pi',            '--size=100000000*20'),
    ('27 Point Stencil',        'point27',                  '--size=350*20'),
    ('Shallow Water',           'shallow_water',            '--size=3200*3200*20'),
    ('Rosenbrock',              'rosenbrock',               '--size=200000000*20'),
#    ('Game of Life v1',         'gameoflife',               '--size=10000*10000*10*1'),
    #('Matrix Multiplication',   'mxmul',                    '--size=500*5'),
    #('Heat Equation FI',        'heat_equation_fixed',      '--size=14000*14000*10'),
    #('Jacobi',                  'jacobi',                   '--size=14000*10'),
    #('Jacobi FI',               'jacobi_fixed',             '--size=14000*10'),
    #('1D Stencil',              'ndstencil',                '--size=27*10*1'),
    #('2D Stencil',              'ndstencil',                '--size=27*10*2'),
    #('3D Stencil',              'ndstencil',                '--size=27*10*3'),
#    ('Synthetic',               'synth',                    '--size=200000000*10'),
#    ('Synthetic Inplace',       'synth_inplace',            '--size=200000000*10'),
    #('Synthetic Stream #0 Ones',    'synth_stream',  '--size=50000000*20*0'),
    #('Synthetic Stream #1 Range',   'synth_stream',  '--size=50000000*10*1'),
    #('Synthetic Stream #2 Random',  'synth_stream',  '--size=50000000*10*2'),
]

scripts_cpu_no_optimal = [
    ('SOR',                     'sor',                      '--size=12000*12000*20'),
    ('NBody',                   'nbody',                    '--size=6000*20'),
    ('NBody Nice',              'nbody_nice',               '--size=20*2000000*20'),
    ('Lattice Boltzmann',       'lbm_3d',                   '--size=150*150*150*20'),
    ('Water-Ice Simulation',    'wisp',                     '--size=800*800*20'),
]

def fuse_cache(value):
    envs = ["BH_SINGLETON_FUSE_CACHE", "BH_TOPOLOGICAL_FUSE_CACHE",\
            "BH_GREEDY_FUSE_CACHE", "BH_OPTIMAL_FUSE_CACHE", "BH_GENTLE_FUSE_CACHE"]
    ret = {}
    for env in envs:
        ret[env] = value
    return ret

def cache_path(value, out={}):
    envs = ["BH_SINGLETON_CACHE_PATH", "BH_TOPOLOGICAL_CACHE_PATH",\
            "BH_GREEDY_CACHE_PATH", "BH_OPTIMAL_CACHE_PATH", "BH_GENTLE_CACHE_PATH"]
    for env in envs:
        out[env] = value
    return out

stack_cpu = [
    [('default',    'bridge',       None)],
    [('bccon',      'bccon',        None)],
    [
        ('UniqueViews', 'bcexp', {'BH_PRICE_MODEL':'unique_views'}),
        ('TmpElem',     'bcexp', {'BH_PRICE_MODEL':'temp_elemination'}),
        ('MaxShare',    'bcexp', {'BH_PRICE_MODEL':'MAX_SHARE'}),
        ('AmosRobinson','bcexp', {'BH_PRICE_MODEL':'amos'}),
    ],
    [
        ('Singleton',  'singleton',   None),
    #    ('Naive',      'topological', None),
        ('Greedy',     'greedy',      None),
        ('Optimal',    'optimal',     None),
    ],
    [
        ('filecache',  'node', fuse_cache("true")),
        ('memcache',  'node', cache_path("", fuse_cache("true"))),
     #   ('nocache',  'node', fuse_cache("false")),
    ],
    [('pricer',     'pricer',       None)],
    [('cpu',        'cpu',  {"BH_CPU_JIT_LEVEL": "3", "OMP_NUM_THREADS":"4"})],
]

stack_cpu_no_optimal = copy.deepcopy(stack_cpu)
stack_cpu_no_optimal[3].pop(-1) # pop the optimal fuser

suite_cpu = {
    'scripts': scripts_cpu,
    'launchers':  [python_bohrium],
    'bohrium': stack_cpu
}

suite_cpu_no_optimal = {
    'scripts': scripts_cpu_no_optimal,
    'launchers':  [python_bohrium],
    'bohrium': stack_cpu_no_optimal
}

suites = [
    suite_cpu,
   # suite_cpu_no_optimal,
]

