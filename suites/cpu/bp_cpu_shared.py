#
#   Common / Shared stack configurations for CPU suites.
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

bh_stack_cpu_t4 = [
    [('default',    'bridge',             None)],
    [('creduce',    'complete_reduction', None)],
    [('node',       'node',               None)],
    [('topo',       'topological',        None)],
    [
        ('cpu_fs_t04', 'cpu',   {"BH_VE_CPU_JIT_FUSION": "1", "OMP_NUM_THREADS": "4"}),
        ('cpu_fs_t02', 'cpu',   {"BH_VE_CPU_JIT_FUSION": "1", "OMP_NUM_THREADS": "2"}),
        ('cpu_fs_t01', 'cpu',   {"BH_VE_CPU_JIT_FUSION": "1", "OMP_NUM_THREADS": "1"}),
    
        ('cpu_t04', 'cpu',   {"BH_VE_CPU_JIT_FUSION": "0", "OMP_NUM_THREADS": "4"}),
        ('cpu_t02', 'cpu',   {"BH_VE_CPU_JIT_FUSION": "0", "OMP_NUM_THREADS": "2"}),
        ('cpu_t01', 'cpu',   {"BH_VE_CPU_JIT_FUSION": "0", "OMP_NUM_THREADS": "1"}),
    ]
]

stack_omp_t32 = [
    [('default',    'bridge',             None)],
    [('node',       'node',               None)],
    [
        ('cpu_af_t32', 'cpu',   {"OMP_NUM_THREADS": "32", "GOMP_CPU_AFFINITY": "0-31" }),
        ('cpu_af_t16', 'cpu',   {"OMP_NUM_THREADS": "16", "GOMP_CPU_AFFINITY": "0-31" }),
        ('cpu_af_t08', 'cpu',   {"OMP_NUM_THREADS": "8", "GOMP_CPU_AFFINITY": "0-31" }),
        ('cpu_af_t04', 'cpu',   {"OMP_NUM_THREADS": "4", "GOMP_CPU_AFFINITY": "0-31" }),
        ('cpu_af_t02', 'cpu',   {"OMP_NUM_THREADS": "2", "GOMP_CPU_AFFINITY": "0-31" }),
        ('cpu_af_t01', 'cpu',   {"OMP_NUM_THREADS": "1", "GOMP_CPU_AFFINITY": "0-31" }),

        ('cpu_t32', 'cpu',   {"OMP_NUM_THREADS": "32"}),
        ('cpu_t16', 'cpu',   {"OMP_NUM_THREADS": "16"}),
        ('cpu_t08', 'cpu',   {"OMP_NUM_THREADS": "8"}),
        ('cpu_t04', 'cpu',   {"OMP_NUM_THREADS": "4"}),
        ('cpu_t02', 'cpu',   {"OMP_NUM_THREADS": "2"}),
        ('cpu_t01', 'cpu',   {"OMP_NUM_THREADS": "1"}),
    ]
]

stack_omp_t4 = [
    [('default',    'bridge',             None)],
    [('node',       'node',               None)],
    [
        ('cpu_af_t04', 'cpu',   {"OMP_NUM_THREADS": "4", "GOMP_CPU_AFFINITY": "0-31" }),
        ('cpu_af_t02', 'cpu',   {"OMP_NUM_THREADS": "2", "GOMP_CPU_AFFINITY": "0-31" }),
        ('cpu_af_t01', 'cpu',   {"OMP_NUM_THREADS": "1", "GOMP_CPU_AFFINITY": "0-31" }),

        ('cpu_t04', 'cpu',   {"OMP_NUM_THREADS": "4"}),
        ('cpu_t02', 'cpu',   {"OMP_NUM_THREADS": "2"}),
        ('cpu_t01', 'cpu',   {"OMP_NUM_THREADS": "1"}),
    ]
]


