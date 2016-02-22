from benchpress.default import *
import copy

def fuse_cache(value):
    envs = ["BH_SINGLETON_FUSE_CACHE", "BH_TOPOLOGICAL_FUSE_CACHE",\
            "BH_GREEDY_FUSE_CACHE", "BH_OPTIMAL_FUSE_CACHE", "BH_GENTLE_FUSE_CACHE"]
    ret = {}
    for env in envs:
        ret[env] = value
    return ret

scripts_cpu_alain = [
    ('Alain Example',  'alain',  '--size=100000000*10'),
]

scripts_cpu_alain_fixed = [
    ('Alain Example Fixed',  'alain',  '--size=100000000*10'),
]

scripts_cpu_calain = [
    ('Alain Counterexample',  'alain_counterexample',  '--size=50000000*10'),
]

def MaxShare_fixed_fusion(Iterations):
    ret = ""
    for i in xrange(Iterations):
        ret += "2:1+2,%(i)d:6+7,%(i)d:8+9,%(i)d:10+11,%(i)d:12+13,%(i)d:5+6,%(i)d:5+8,%(i)d:5+10,"%{'i':i+2}
    return ret[:-1]

def TmpElem_fixed_fusion(Iterations):
    ret = ""
    for i in xrange(Iterations):
        ret += "%(i)d:1+2,%(i)d:1+3,%(i)d:1+4,%(i)d:1+5,%(i)d:6+7,%(i)d:8+9,%(i)d:10+11,%(i)d:12+13,"%{'i':i+2}
    return ret[:-1]

stack_cpu = [
    [('default',    'bridge',       None)],
    [('bccon',      'bccon',        None)],
    [
        ('UniqueViews', 'bcexp', {'BH_PRICE_MODEL':'unique_views'}),
        ('TmpElem',     'bcexp', {'BH_PRICE_MODEL':'temp_elemination'}),
        ('MaxShare',    'bcexp', {'BH_PRICE_MODEL':'max_share'}),
        ('AmosRobinson','bcexp', {'BH_PRICE_MODEL':'amos'}),
    ],
    [
        ('Optimal',    'optimal',     None),
    ],
    [
        ('filecache',  'node', fuse_cache("true")),
    ],
    [('pricer',     'pricer',       None)],
    [('cpu',        'cpu',  {"BH_CPU_JIT_LEVEL": "3", "OMP_NUM_THREADS":"4"})],
]
stack_cpu_alain_fixed = copy.deepcopy(stack_cpu)
stack_cpu_alain_fixed[2] =\
[
    ('UniqueViews', 'bcexp', {'BH_PRICE_MODEL':'unique_views'}),
    ('TmpElem',     'bcexp', {'BH_PRICE_MODEL':'temp_elemination',
                              'BH_FUSER_OPTIMAL_MERGE':TmpElem_fixed_fusion(10)}),
    ('MaxShare',    'bcexp', {'BH_PRICE_MODEL':'max_share',
                              'BH_FUSER_OPTIMAL_MERGE':MaxShare_fixed_fusion(10)}),
    ('AmosRobinson','bcexp', {'BH_PRICE_MODEL':'amos',
                              'BH_FUSER_OPTIMAL_MERGE':MaxShare_fixed_fusion(10)}),
]
stack_cpu_alain_fixed[3][0] = ('Optimal','optimal', {'BH_OPTIMAL_CACHE_PATH':"/tmp/bh_fixed_fuse_cache"})

stack_cpu_calain = copy.deepcopy(stack_cpu)

suite_cpu_alain = {
    'scripts': scripts_cpu_alain,
    'launchers':  [python_bohrium],
    'bohrium': stack_cpu
}
suite_cpu_alain_fixed = {
    'scripts': scripts_cpu_alain_fixed,
    'launchers':  [python_bohrium],
    'bohrium': stack_cpu_alain_fixed
}
suite_cpu_calain = {
    'scripts': scripts_cpu_calain,
    'launchers':  [python_bohrium],
    'bohrium': stack_cpu_calain
}

suites = [
    suite_cpu_alain,
    suite_cpu_alain_fixed,
    suite_cpu_calain,
]

