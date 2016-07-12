from benchpress.default import *
import copy

scripts = [
    ('Black Scholes',           'black_scholes',            '--size=15000000*40'),
    ('Heat Equation',           'heat_equation',            '--size=12000*12000*40'),
    ('Monte Carlo Pi',          'montecarlo_pi',            '--size=100000000*40'),
    ('Leibnitz Pi',             'leibnitz_pi',              '--size=700000000'),
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

stack = [
    [('default',    'bridge',       None)],
    [('bccon',      'bccon',        None)],
    [
        ('UniqueViews', 'bcexp', {'BH_PRICE_MODEL':'unique_views'}),
    ],
    [
        ('Greedy',     'greedy',      None),
    ],
    [
        ('memcache',  'node', cache_path("", fuse_cache("true"))),
    ],
    [
        ('cpu*1',        'cpu',  {"BH_CPU_JIT_LEVEL": "3", "OMP_NUM_THREADS":"1"}),
        ('cpu*4',        'cpu',  {"BH_CPU_JIT_LEVEL": "3", "OMP_NUM_THREADS":"4"}),
    ],
]

suite_bohrium = {
    'scripts': scripts,
    'launchers':  [python_bohrium],
    'bohrium': stack
}

suite_c = {
    'scripts': scripts,
    'launchers':  [c99_seq, python_numpy],
    'bohrium': bh_stack_none
}

suites = [
    suite_bohrium,
    suite_c,
]

