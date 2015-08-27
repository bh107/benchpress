from benchpress.default import *
import copy

scripts_gpu = [
    ('Black Scholes',       'black_scholes',  '--size=32000000*50 --dtype=float32'),
    ('Stencil4D',           'ndstencil',      '--size=25*1000*4 --dtype=float32'),
    ('Leibnitz PI',         'leibnitz_pi',    '--size=10000000       --dtype=float32'),
    ('Monte Carlo PI',      'montecarlo_pi',  '--size=10000000*100    --dtype=float32'),
    ('Matrix Mul',          'mxmul',          '--size=500            --dtype=float32'),
    ('Game of Life v1',     'gameoflife',     '--size=2000*2000*100*1 --dtype=float32'),
    ('Game of Life v2',     'gameoflife',     '--size=2000*2000*100*2 --dtype=float32'),
    ('Heat Equation',       'heat_equation',  '--size=2000*2000*100   --dtype=float32'),
]

scripts_gpu_no_optimal = [
    ('Shallow Water',       'shallow_water',  '--size=1000*1000*100 --dtype=float32'),
    #('Gauss Elimination',   'gauss',     '--size=1000 --dtype=float32'),
    #('LU Factorization',    'lu',        '--size=1000 --dtype=float32'),
    #('Stencil1D',           'ndstencil', '--size=25*8000*1 --dtype=float32'),
    #('Stencil2D',           'ndstencil', '--size=25*4000*2 --dtype=float32'),
    #('Stencil3D',           'ndstencil', '--size=25*2000*3 --dtype=float32'),
    #('SOR',           'sor',            '--size=8000*8000*100 --dtype=float32'),
    #('N-body',        'nbody',          '--size=3200*50 --dtype=float32'),
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

stack_gpu = [
    [('default',    'bridge',       None)],
    [('bcexp_gpu',  'bcexp_gpu',    None)],
    [('dimclean',   'dimclean',     None)],
    [
        ('UniqueViews', 'dimclean', {'BH_PRICE_MODEL':'unique_views'}),
        ('TmpElem',     'dimclean', {'BH_PRICE_MODEL':'temp_elemination'}),
    ],
    [
        ('Singleton',  'singleton',   None),
#        ('Naive',      'topological', None),
        ('Greedy',     'greedy',      None),
        ('Optimal',    'optimal',     None),
    ],
    [
        ('filecache',  'node', fuse_cache("true")),
#        ('memcache',  'node', cache_path("", fuse_cache("true"))),
#        ('nocache',  'node', fuse_cache("false")),
    ],
    [('pricer',     'pricer',   None)],
    #[('gpu',        'gpu',      {"BH_FUSE_MODEL" : "NO_XSWEEP_SCALAR_SEPERATE"})],
    [('gpu',        'gpu',      None)],
    [('cpu',        'cpu',      {"BH_CPU_JIT_LEVEL": "3", "OMP_NUM_THREADS":4})],
]

stack_gpu_no_optimal = copy.deepcopy(stack_gpu)
stack_gpu_no_optimal[4].pop(-1) # pop the optimal fuser

suite_gpu = {
    'scripts': scripts_gpu,
    'launchers':  [python_bohrium],
    'bohrium': stack_gpu
}

suite_gpu_no_optimal = {
    'scripts': scripts_gpu_no_optimal,
    'launchers':  [python_bohrium],
    'bohrium': stack_gpu_no_optimal
}

suites = [
    suite_gpu,
    suite_gpu_no_optimal,
]


