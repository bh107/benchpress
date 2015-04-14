from default import *

#
#   Example Bohrium stack configuration
#
bh_stack_cpu_t4 = [
    [('default',    'bridge',             None)],
    [('creduce',    'complete_reduction', None)],
    [('node',       'node',               None)],
    [('topo',       'topological',        None)],
    [
        ('cpu_t04', 'cpu',   {"OMP_NUM_THREADS": "4"}),
        ('cpu_t02', 'cpu',   {"OMP_NUM_THREADS": "2"}),
        ('cpu_t01', 'cpu',   {"OMP_NUM_THREADS": "1"}),
    ]
]

bh_stack_cpu_t32 = [
    [('default',    'bridge',             None)],
    [('creduce',    'complete_reduction', None)],
    [('node',       'node',               None)],
    [('topo',       'topological',        None)],
    [
        ('cpu_t32', 'cpu',   {"OMP_NUM_THREADS": "32"}),
        ('cpu_t16', 'cpu',   {"OMP_NUM_THREADS": "16"}),
        ('cpu_t08', 'cpu',   {"OMP_NUM_THREADS": "8"}),
        ('cpu_t04', 'cpu',   {"OMP_NUM_THREADS": "4"}),
        ('cpu_t02', 'cpu',   {"OMP_NUM_THREADS": "2"}),
        ('cpu_t01', 'cpu',   {"OMP_NUM_THREADS": "1"}),
    ]
]

#
#   Scripts
#
scripts = [
    ('Leibnitz PI',   'leibnitz_pi',  '--size=100000000'),
]
#
#   Default launchers (python_numpy, python_bohrium) are used.
#

#
#   Putting them together in the following example suite definition
#
multicore = {
    'scripts': scripts,
    'launchers': [cpp11_omp, python_bohrium, cpp11_bxx],
    'bohrium': bh_stack_cpu_t4
}

sequential = {
    'scripts': scripts,
    'launchers': [c99_seq, cpp11_seq],
    'bohrium': bh_stack_none
}

numpy = {
    'scripts': scripts,
    'launchers': [python_numpy],
    'bohrium': bh_stack_none
}

#
#   As usual, put them into the list of suites to run.
#
suites = [
    numpy,
    sequential,
    multicore
]
