from benchpress.default import *

scripts = [
    ('SciFly C1',   'scifly',    '--size=1000*10*1'),
    ('SciFly C2',   'scifly',    '--size=1000*10*2'),
]

bh_stack_laptop = [
    [('default',    'bridge',       None)],
    [('bccon',      'bccon',        None)],
    [('bcexp',      'bcexp',        None)],
    [('topo',       'topological',  None)],
    [('node',       'node',         None)],
    [
        ('cpu_t04', 'cpu',  {"OMP_NUM_THREADS": "4"}),
        ('cpu_t02', 'cpu',  {"OMP_NUM_THREADS": "2"}),
        ('cpu_t01', 'cpu',  {"OMP_NUM_THREADS": "1"}),
    ]
]

bohrium = {
    'scripts': scripts,
    'launchers': [python_bohrium],
    'bohrium': bh_stack_laptop,
    "use_slurm_default": False,
    "use_grapher": "cpu"
}

numpy = {
    'scripts': scripts,
    'launchers': [python_numpy],
    'bohrium': bh_stack_none,
    "use_slurm_default": False,
    "use_grapher": "cpu"
}

#
#   As usual, put them into the list of suites to run.
#
suites = [
    numpy,
    bohrium
]
