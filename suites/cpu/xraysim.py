from benchpress.default import *
from bp_cpu_shared import *

scripts = [
    #('X-Ray Simulation (60*10*10)', 'xraysim', '--size=60*10*10'),
    ('X-Ray Simulation (50*20*5)', 'xraysim', '--size=50*20*5'),
    ('X-Ray Simulation (50*63*5)', 'xraysim', '--size=50*63*5'),
    ('X-Ray Simulation (50*200*5)', 'xraysim', '--size=50*200*5'),
#    ('X-Ray Simulation (50*633*5)', 'xraysim', '--size=50*633*5'),
]

bh_stack_cpu_t32 = [
    [('default',    'bridge',       None)],
    [('bccon',      'bccon',        None)],
    [('bcexp',      'bcexp',        None)],
    [('topo',       'topological',  None), ('greedy', 'greedy', None)],
    [('node',       'node',         None)],
    [
        ('cpu_vc_fs_ct_t32', 'cpu',  {"BH_CPU_JIT_LEVEL": "3", "OMP_NUM_THREADS": "32", "BH_BCEXP_SIGN": "0"}),
    ]
]

numpy = {
    'scripts':  [scripts[0]],
    'launchers':  [python_numpy],
    'bohrium': bh_stack_none,
    "use_slurm_default": True,
    "use_grapher": "cpu"
}

bohrium = {
    'scripts':  scripts,
    'launchers':  [python_bohrium],
    'bohrium':  bh_stack_cpu_t32,
    "use_slurm_default": True,
    "use_grapher": "cpu"
}

suites = [
    bohrium
]

