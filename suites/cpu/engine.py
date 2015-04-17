from benchpress.default import *

#
#   Example Bohrium stack configuration
#
bh_stack_cpu_t32 = [
    [('default',    'bridge',             None)],
    [('creduce',    'complete_reduction', None)],
    [('node',       'node',               None)],
    [('topo',       'topological',        None)],
    [
        ('cpu_fs_t32', 'cpu',   {"BH_VE_CPU_JIT_FUSION": "1", "OMP_NUM_THREADS": "32"}),
        ('cpu_fs_t16', 'cpu',   {"BH_VE_CPU_JIT_FUSION": "1", "OMP_NUM_THREADS": "16"}),
        ('cpu_fs_t08', 'cpu',   {"BH_VE_CPU_JIT_FUSION": "1", "OMP_NUM_THREADS": "8"}),
        ('cpu_fs_t04', 'cpu',   {"BH_VE_CPU_JIT_FUSION": "1", "OMP_NUM_THREADS": "4"}),
        ('cpu_fs_t02', 'cpu',   {"BH_VE_CPU_JIT_FUSION": "1", "OMP_NUM_THREADS": "2"}),
        ('cpu_fs_t01', 'cpu',   {"BH_VE_CPU_JIT_FUSION": "1", "OMP_NUM_THREADS": "1"}),
    
        ('cpu_t32', 'cpu',   {"BH_VE_CPU_JIT_FUSION": "0", "OMP_NUM_THREADS": "32"}),
        ('cpu_t16', 'cpu',   {"BH_VE_CPU_JIT_FUSION": "0", "OMP_NUM_THREADS": "16"}),
        ('cpu_t08', 'cpu',   {"BH_VE_CPU_JIT_FUSION": "0", "OMP_NUM_THREADS": "8"}),
        ('cpu_t04', 'cpu',   {"BH_VE_CPU_JIT_FUSION": "0", "OMP_NUM_THREADS": "4"}),
        ('cpu_t02', 'cpu',   {"BH_VE_CPU_JIT_FUSION": "0", "OMP_NUM_THREADS": "2"}),
        ('cpu_t01', 'cpu',   {"BH_VE_CPU_JIT_FUSION": "0", "OMP_NUM_THREADS": "1"}),

    ]
]

stack_omp_t32 = [
    [('default',    'bridge',             None)],
    [('node',       'node',               None)],
    [
        ('cpu_t32', 'cpu',   {"OMP_NUM_THREADS": "32"}),
        ('cpu_t16', 'cpu',   {"OMP_NUM_THREADS": "16"}),
        ('cpu_t08', 'cpu',   {"OMP_NUM_THREADS": "8"}),
        ('cpu_t04', 'cpu',   {"OMP_NUM_THREADS": "4"}),
        ('cpu_t02', 'cpu',   {"OMP_NUM_THREADS": "2"}),
        ('cpu_t01', 'cpu',   {"OMP_NUM_THREADS": "1"}),

        ('cpu_af_t32', 'cpu',   {"OMP_NUM_THREADS": "32", "GOMP_CPU_AFFINITY": "0-31" }),
        ('cpu_af_t16', 'cpu',   {"OMP_NUM_THREADS": "16", "GOMP_CPU_AFFINITY": "0-31" }),
        ('cpu_af_t08', 'cpu',   {"OMP_NUM_THREADS": "8", "GOMP_CPU_AFFINITY": "0-31" }),
        ('cpu_af_t04', 'cpu',   {"OMP_NUM_THREADS": "4", "GOMP_CPU_AFFINITY": "0-31" }),
        ('cpu_af_t02', 'cpu',   {"OMP_NUM_THREADS": "2", "GOMP_CPU_AFFINITY": "0-31" }),
        ('cpu_af_t01', 'cpu',   {"OMP_NUM_THREADS": "1", "GOMP_CPU_AFFINITY": "0-31" }),
    ]
]

#
#   Scripts
#
scripts = [
    ('Heat Equation',   'heat_equation',    '--size=14000*14000*10'),
    ('Leibnitz PI',     'leibnitz_pi',      '--size=200000000'),
    ('Rosenbrock',      'rosenbrock',       '--size=100000000*10'),
]
#
#   Default launchers (python_numpy, python_bohrium) are used.
#

#
#   Putting them together in the following example suite definition
#
bohrium = {
    'scripts': scripts,
    'launchers': [python_bohrium],
    'bohrium': bh_stack_cpu_t32
}

omp = {
    'scripts': scripts,
    'launchers': [cpp11_omp],
    'bohrium': stack_omp_t32
}

cseq = {
    'scripts': scripts,
    'launchers': [c99_seq],
    'bohrium': bh_stack_none
}

np = {
    'scripts': scripts,
    'launchers': [python_numpy],
    'bohrium': bh_stack_none
}

#
#   As usual, put them into the list of suites to run.
#
suites = [
    cseq,
    omp,
    bohrium,
    np
]
