from benchpress.default import *
from bp_cpu_shared import *

bh_stack = [
    [('default',    'bridge',       None)],
    [('bccon',      'bccon',        None)],
    [('bcexp',      'bcexp',        None)],
    [('topo',       'topological',  None)],
    [('node',       'node',         None)],
    [
        ('cpu_vfc_t32',          'cpu',  {"BH_CPU_JIT_LEVEL": "3", "OMP_NUM_THREADS": "32", "BH_BCEXP_SIGN": "0"}),
        ('cpu_vfc_t16',          'cpu',  {"BH_CPU_JIT_LEVEL": "3", "OMP_NUM_THREADS": "16", "BH_BCEXP_SIGN": "0"}),
        ('cpu_vfc_t08',          'cpu',  {"BH_CPU_JIT_LEVEL": "3", "OMP_NUM_THREADS": "8" , "BH_BCEXP_SIGN": "0"}),
        ('cpu_vfc_t04',          'cpu',  {"BH_CPU_JIT_LEVEL": "3", "OMP_NUM_THREADS": "4" , "BH_BCEXP_SIGN": "0"}),
        ('cpu_vfc_t02',          'cpu',  {"BH_CPU_JIT_LEVEL": "3", "OMP_NUM_THREADS": "2" , "BH_BCEXP_SIGN": "0"}),
        ('cpu_vfc_t01',          'cpu',  {"BH_CPU_JIT_LEVEL": "3", "OMP_NUM_THREADS": "1" , "BH_BCEXP_SIGN": "0"}),

        ('cpu_v_t32',          'cpu',  {"BH_CPU_JIT_LEVEL": "1", "OMP_NUM_THREADS": "32", "BH_BCEXP_SIGN": "0"}),
        ('cpu_v_t16',          'cpu',  {"BH_CPU_JIT_LEVEL": "1", "OMP_NUM_THREADS": "16", "BH_BCEXP_SIGN": "0"}),
        ('cpu_v_t08',          'cpu',  {"BH_CPU_JIT_LEVEL": "1", "OMP_NUM_THREADS": "8" , "BH_BCEXP_SIGN": "0"}),
        ('cpu_v_t04',          'cpu',  {"BH_CPU_JIT_LEVEL": "1", "OMP_NUM_THREADS": "4" , "BH_BCEXP_SIGN": "0"}),
        ('cpu_v_t02',          'cpu',  {"BH_CPU_JIT_LEVEL": "1", "OMP_NUM_THREADS": "2" , "BH_BCEXP_SIGN": "0"}),
        ('cpu_v_t01',          'cpu',  {"BH_CPU_JIT_LEVEL": "1", "OMP_NUM_THREADS": "1" , "BH_BCEXP_SIGN": "0"}),
    ]
]

scripts = [
    ('Lulesh', 'lulesh', '--size=5'),
    ('Lulesh', 'lulesh', '--size=10'),
    ('Lulesh', 'lulesh', '--size=45'),
    ('Lulesh', 'lulesh', '--size=50'),
    ('Lulesh', 'lulesh', '--size=70'),
    ('Lulesh', 'lulesh', '--size=90'),
]

sequential = {
    'scripts': scripts,
    'launchers': [cpp11_seq],
    'bohrium': bh_stack_none,
    "use_slurm_default": True,
    "use_grapher": "cpu"
}

multicore = {
    'scripts': scripts,
    'launchers': [cpp11_omp],
    'bohrium': stack_omp_t32,
    "use_slurm_default": True,
    "use_grapher": "cpu"
}

bohrium = {
    'scripts': scripts,
    'launchers': [cpp11_bxx],
    'bohrium': bh_stack,
    "use_slurm_default": True,
    "use_grapher": "cpu"
}

suites = [
    sequential,
    multicore,
    bohrium
]
