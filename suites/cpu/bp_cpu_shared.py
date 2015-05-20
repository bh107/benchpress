#
#   Common / Shared stack configurations for CPU suites.
#
bh_stack_cpu_t32_best = [
    [('default',                'bridge',                   None)],
    [('composite_expansion',    'composite_expansion',      None)],
    [('composite_contraction',  'composite_contraction',    None)],
    [('topo',                   'topological',              None)],
    [
        ('cpu_vc_fs_ct_t32', 'cpu',   {"BH_CPU_JIT_LEVEL": "3", "OMP_NUM_THREADS": "32", "COMPOSITE_EXPANSION_EXPAND_SIGN": "0"}),
        ('cpu_vc_fs_ct_t16', 'cpu',   {"BH_CPU_JIT_LEVEL": "3", "OMP_NUM_THREADS": "16", "COMPOSITE_EXPANSION_EXPAND_SIGN": "0"}),
        ('cpu_vc_fs_ct_t08', 'cpu',   {"BH_CPU_JIT_LEVEL": "3", "OMP_NUM_THREADS": "8" , "COMPOSITE_EXPANSION_EXPAND_SIGN": "0"}),
        ('cpu_vc_fs_ct_t04', 'cpu',   {"BH_CPU_JIT_LEVEL": "3", "OMP_NUM_THREADS": "4" , "COMPOSITE_EXPANSION_EXPAND_SIGN": "0"}),
        ('cpu_vc_fs_ct_t02', 'cpu',   {"BH_CPU_JIT_LEVEL": "3", "OMP_NUM_THREADS": "2" , "COMPOSITE_EXPANSION_EXPAND_SIGN": "0"}),
        ('cpu_vc_fs_ct_t01', 'cpu',   {"BH_CPU_JIT_LEVEL": "3", "OMP_NUM_THREADS": "1" , "COMPOSITE_EXPANSION_EXPAND_SIGN": "0"}),
    ]
]

bh_stack_cpu_t32 = [
    [('default',                'bridge',                   None)],
    [('composite_expansion',    'composite_expansion',      None)],
    [('composite_contraction',  'composite_contraction',    None)],
    [('topo',                   'topological',              None)],
    [
        ('cpu_vc_fs_ct_t32', 'cpu',   {"BH_CPU_JIT_LEVEL": "3", "OMP_NUM_THREADS": "32", "COMPOSITE_EXPANSION_EXPAND_SIGN": "0"}),
        ('cpu_vc_fs_ct_t16', 'cpu',   {"BH_CPU_JIT_LEVEL": "3", "OMP_NUM_THREADS": "16", "COMPOSITE_EXPANSION_EXPAND_SIGN": "0"}),
        ('cpu_vc_fs_ct_t08', 'cpu',   {"BH_CPU_JIT_LEVEL": "3", "OMP_NUM_THREADS": "8" , "COMPOSITE_EXPANSION_EXPAND_SIGN": "0"}),
        ('cpu_vc_fs_ct_t04', 'cpu',   {"BH_CPU_JIT_LEVEL": "3", "OMP_NUM_THREADS": "4" , "COMPOSITE_EXPANSION_EXPAND_SIGN": "0"}),
        ('cpu_vc_fs_ct_t02', 'cpu',   {"BH_CPU_JIT_LEVEL": "3", "OMP_NUM_THREADS": "2" , "COMPOSITE_EXPANSION_EXPAND_SIGN": "0"}),
        ('cpu_vc_fs_ct_t01', 'cpu',   {"BH_CPU_JIT_LEVEL": "3", "OMP_NUM_THREADS": "1" , "COMPOSITE_EXPANSION_EXPAND_SIGN": "0"}),
    
        ('cpu_vc_t32', 'cpu',   {"BH_CPU_JIT_LEVEL": "1", "OMP_NUM_THREADS": "32", "COMPOSITE_EXPANSION_EXPAND_SIGN": "0"}),
        ('cpu_vc_t16', 'cpu',   {"BH_CPU_JIT_LEVEL": "1", "OMP_NUM_THREADS": "16", "COMPOSITE_EXPANSION_EXPAND_SIGN": "0"}),
        ('cpu_vc_t08', 'cpu',   {"BH_CPU_JIT_LEVEL": "1", "OMP_NUM_THREADS": "8" , "COMPOSITE_EXPANSION_EXPAND_SIGN": "0"}),
        ('cpu_vc_t04', 'cpu',   {"BH_CPU_JIT_LEVEL": "1", "OMP_NUM_THREADS": "4" , "COMPOSITE_EXPANSION_EXPAND_SIGN": "0"}),
        ('cpu_vc_t02', 'cpu',   {"BH_CPU_JIT_LEVEL": "1", "OMP_NUM_THREADS": "2" , "COMPOSITE_EXPANSION_EXPAND_SIGN": "0"}),
        ('cpu_vc_t01', 'cpu',   {"BH_CPU_JIT_LEVEL": "1", "OMP_NUM_THREADS": "1" , "COMPOSITE_EXPANSION_EXPAND_SIGN": "0"}),
    ]
]

bh_stack_cpu_t32_all = [
    [('default',                'bridge',                   None)],
    [('composite_expansion',    'composite_expansion',      None)],
    [('composite_contraction',  'composite_contraction',    None)],
    [('topo',                   'topological',              None)],
    [
        ('cpu_vc_fs_ct_t32', 'cpu', {"BH_CPU_JIT_LEVEL": "3", "OMP_NUM_THREADS": "32", "COMPOSITE_EXPANSION_EXPAND_SIGN": "0"}),
        ('cpu_vc_fs_ct_t16', 'cpu', {"BH_CPU_JIT_LEVEL": "3", "OMP_NUM_THREADS": "16", "COMPOSITE_EXPANSION_EXPAND_SIGN": "0"}),
        ('cpu_vc_fs_ct_t08', 'cpu', {"BH_CPU_JIT_LEVEL": "3", "OMP_NUM_THREADS": "8" , "COMPOSITE_EXPANSION_EXPAND_SIGN": "0"}),
        ('cpu_vc_fs_ct_t04', 'cpu', {"BH_CPU_JIT_LEVEL": "3", "OMP_NUM_THREADS": "4" , "COMPOSITE_EXPANSION_EXPAND_SIGN": "0"}),
        ('cpu_vc_fs_ct_t02', 'cpu', {"BH_CPU_JIT_LEVEL": "3", "OMP_NUM_THREADS": "2" , "COMPOSITE_EXPANSION_EXPAND_SIGN": "0"}),
        ('cpu_vc_fs_ct_t01', 'cpu', {"BH_CPU_JIT_LEVEL": "3", "OMP_NUM_THREADS": "1" , "COMPOSITE_EXPANSION_EXPAND_SIGN": "0"}),

        ('cpu_vc_fs_t32', 'cpu',    {"BH_CPU_JIT_LEVEL": "2", "OMP_NUM_THREADS": "32", "COMPOSITE_EXPANSION_EXPAND_SIGN": "0"}),
        ('cpu_vc_fs_t16', 'cpu',    {"BH_CPU_JIT_LEVEL": "2", "OMP_NUM_THREADS": "16", "COMPOSITE_EXPANSION_EXPAND_SIGN": "0"}),
        ('cpu_vc_fs_t08', 'cpu',    {"BH_CPU_JIT_LEVEL": "2", "OMP_NUM_THREADS": "8" , "COMPOSITE_EXPANSION_EXPAND_SIGN": "0"}),
        ('cpu_vc_fs_t04', 'cpu',    {"BH_CPU_JIT_LEVEL": "2", "OMP_NUM_THREADS": "4" , "COMPOSITE_EXPANSION_EXPAND_SIGN": "0"}),
        ('cpu_vc_fs_t02', 'cpu',    {"BH_CPU_JIT_LEVEL": "2", "OMP_NUM_THREADS": "2" , "COMPOSITE_EXPANSION_EXPAND_SIGN": "0"}),
        ('cpu_vc_fs_t01', 'cpu',    {"BH_CPU_JIT_LEVEL": "2", "OMP_NUM_THREADS": "1" , "COMPOSITE_EXPANSION_EXPAND_SIGN": "0"}),
    
        ('cpu_vc_t32', 'cpu',       {"BH_CPU_JIT_LEVEL": "1", "OMP_NUM_THREADS": "32", "COMPOSITE_EXPANSION_EXPAND_SIGN": "0"}),
        ('cpu_vc_t16', 'cpu',       {"BH_CPU_JIT_LEVEL": "1", "OMP_NUM_THREADS": "16", "COMPOSITE_EXPANSION_EXPAND_SIGN": "0"}),
        ('cpu_vc_t08', 'cpu',       {"BH_CPU_JIT_LEVEL": "1", "OMP_NUM_THREADS": "8" , "COMPOSITE_EXPANSION_EXPAND_SIGN": "0"}),
        ('cpu_vc_t04', 'cpu',       {"BH_CPU_JIT_LEVEL": "1", "OMP_NUM_THREADS": "4" , "COMPOSITE_EXPANSION_EXPAND_SIGN": "0"}),
        ('cpu_vc_t02', 'cpu',       {"BH_CPU_JIT_LEVEL": "1", "OMP_NUM_THREADS": "2" , "COMPOSITE_EXPANSION_EXPAND_SIGN": "0"}),
        ('cpu_vc_t01', 'cpu',       {"BH_CPU_JIT_LEVEL": "1", "OMP_NUM_THREADS": "1" , "COMPOSITE_EXPANSION_EXPAND_SIGN": "0"}),

        ('cpu_t32', 'cpu',          {"BH_CPU_JIT_LEVEL": "1", "OMP_NUM_THREADS": "32", "BH_CPU_VCACHE_SIZE": "0", "COMPOSITE_EXPANSION_EXPAND_SIGN": "0"}),
        ('cpu_t16', 'cpu',          {"BH_CPU_JIT_LEVEL": "1", "OMP_NUM_THREADS": "16", "BH_CPU_VCACHE_SIZE": "0", "COMPOSITE_EXPANSION_EXPAND_SIGN": "0"}),
        ('cpu_t08', 'cpu',          {"BH_CPU_JIT_LEVEL": "1", "OMP_NUM_THREADS": "8",  "BH_CPU_VCACHE_SIZE": "0", "COMPOSITE_EXPANSION_EXPAND_SIGN": "0"}),
        ('cpu_t04', 'cpu',          {"BH_CPU_JIT_LEVEL": "1", "OMP_NUM_THREADS": "4",  "BH_CPU_VCACHE_SIZE": "0", "COMPOSITE_EXPANSION_EXPAND_SIGN": "0"}),
        ('cpu_t02', 'cpu',          {"BH_CPU_JIT_LEVEL": "1", "OMP_NUM_THREADS": "2",  "BH_CPU_VCACHE_SIZE": "0", "COMPOSITE_EXPANSION_EXPAND_SIGN": "0"}),
        ('cpu_t01', 'cpu',          {"BH_CPU_JIT_LEVEL": "1", "OMP_NUM_THREADS": "1",  "BH_CPU_VCACHE_SIZE": "0", "COMPOSITE_EXPANSION_EXPAND_SIGN": "0"}),

    ]
]

bh_stack_cpu_t4 = [
    [('default',                'bridge',                   None)],
    [('composite_expansion',    'composite_expansion',      None)],
    [('composite_contraction',  'composite_contraction',    None)],
    [('topo',                   'topological',              None)],
    [
        ('cpu_fs_t04', 'cpu',   {"BH_CPU_JIT_LEVEL": "3", "OMP_NUM_THREADS": "4", "COMPOSITE_EXPANSION_EXPAND_SIGN": "0"}),
        ('cpu_fs_t02', 'cpu',   {"BH_CPU_JIT_LEVEL": "3", "OMP_NUM_THREADS": "2", "COMPOSITE_EXPANSION_EXPAND_SIGN": "0"}),
        ('cpu_fs_t01', 'cpu',   {"BH_CPU_JIT_LEVEL": "3", "OMP_NUM_THREADS": "1", "COMPOSITE_EXPANSION_EXPAND_SIGN": "0"}),
    
        ('cpu_t04', 'cpu',   {"BH_CPU_JIT_LEVEL": "1", "OMP_NUM_THREADS": "4", "COMPOSITE_EXPANSION_EXPAND_SIGN": "0" }),
        ('cpu_t02', 'cpu',   {"BH_CPU_JIT_LEVEL": "1", "OMP_NUM_THREADS": "2", "COMPOSITE_EXPANSION_EXPAND_SIGN": "0" }),
        ('cpu_t01', 'cpu',   {"BH_CPU_JIT_LEVEL": "1", "OMP_NUM_THREADS": "1", "COMPOSITE_EXPANSION_EXPAND_SIGN": "0" }),
    ]
]

stack_omp_t32 = [
    [('default',                'bridge',                   None)],
    [('composite_expansion',    'composite_expansion',      None)],
    [('composite_contraction',  'composite_contraction',    None)],
    [('topo',                   'topological',              None)],
    [
        ('omp_af_t32', 'cpu',   {"OMP_NUM_THREADS": "32", "GOMP_CPU_AFFINITY": "0-31" }),
        ('omp_af_t16', 'cpu',   {"OMP_NUM_THREADS": "16", "GOMP_CPU_AFFINITY": "0-31" }),
        ('omp_af_t08', 'cpu',   {"OMP_NUM_THREADS": "8",  "GOMP_CPU_AFFINITY": "0-31" }),
        ('omp_af_t04', 'cpu',   {"OMP_NUM_THREADS": "4",  "GOMP_CPU_AFFINITY": "0-31" }),
        ('omp_af_t02', 'cpu',   {"OMP_NUM_THREADS": "2",  "GOMP_CPU_AFFINITY": "0-31" }),
        ('omp_af_t01', 'cpu',   {"OMP_NUM_THREADS": "1",  "GOMP_CPU_AFFINITY": "0-31" }),

        ('omp_t32', 'cpu',   {"OMP_NUM_THREADS": "32"}),
        ('omp_t16', 'cpu',   {"OMP_NUM_THREADS": "16"}),
        ('omp_t08', 'cpu',   {"OMP_NUM_THREADS": "8"}),
        ('omp_t04', 'cpu',   {"OMP_NUM_THREADS": "4"}),
        ('omp_t02', 'cpu',   {"OMP_NUM_THREADS": "2"}),
        ('omp_t01', 'cpu',   {"OMP_NUM_THREADS": "1"}),
    ]
]

