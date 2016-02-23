from benchpress.default import *
import copy

scripts_cpu = [
    ('Game of Life',            'gameoflife',               '--size=10000*10000*40*2'),
    ('Jacobi Solver',           'jacobi',                   '--size=14000*40'),
    ('Black Scholes',           'black_scholes',            '--size=15000000*40'),
    ('Heat Equation',           'heat_equation',            '--size=12000*12000*40'),
    ('Gauss Elimination',       'gauss',                    '--size=2800'),
    ('LU Factorization',        'lu',                       '--size=2800'),
    ('Monte Carlo Pi',          'montecarlo_pi',            '--size=100000000*40'),
    ('Leibnitz Pi',             'leibnitz_pi',              '--size=100000000*40'),
    ('27 Point Stencil',        'point27',                  '--size=350*40'),
    ('Rosenbrock',              'rosenbrock',               '--size=200000000*40'),
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
    ],
    [
        ('Singleton',  'singleton',   None),
        ('Greedy',     'greedy',      None),
        ('Optimal',    'optimal',     None),
    ],
    [
        ('memcache',  'node', cache_path("", fuse_cache("true"))),
    ],
    [('pricer',     'pricer',       None)],
    [('cpu',        'cpu',  {"BH_CPU_JIT_LEVEL": "3", "OMP_NUM_THREADS":"4"})],
]

suite_cpu = {
    'scripts': scripts_cpu,
    'launchers':  [python_bohrium],
    'bohrium': stack_cpu
}

suites = [
    suite_cpu,
]

