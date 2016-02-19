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

MaxShare_fixed_fusion = "2:1+2,2:6+7,2:8+9,2:10+11,2:12+13,2:5+6,2:5+8,2:5+10"
TmpElem_fixed_fusion = "2:1+2,2:6+7,2:8+9,2:10+11,2:12+13"

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
                              'BH_FUSER_OPTIMAL_MERGE':TmpElem_fixed_fusion}),
    ('MaxShare',    'bcexp', {'BH_PRICE_MODEL':'max_share',
                              'BH_FUSER_OPTIMAL_MERGE':MaxShare_fixed_fusion}),
    ('AmosRobinson','bcexp', {'BH_PRICE_MODEL':'amos',
                              'BH_FUSER_OPTIMAL_MERGE':MaxShare_fixed_fusion}),
]

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

