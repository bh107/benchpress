from benchpress.default import *

scripts = [
    ('Leibnitz PI',             'leibnitz_pi',              '--size=100000000'),
]

numpy = {
    'scripts':  scripts,
    'launchers':  [python_numpy],
    'bohrium': bh_stack_none,
    "use_slurm_default": True,
    "use_grapher": "cpu"
}

bohrium = {
    'scripts':  scripts,
    'launchers':  [python_bohrium],
    'bohrium':  [
        [('default',    'bridge',             None)],
        [('creduce',    'complete_reduction', None)],
        [('node',       'node',               None)],
        [('topo',       'topological',        None)],
 
        [
            ('cpu_fs_t01',      'cpu', {'BH_VE_CPU_JIT_FUSION': '1',    'OMP_NUM_THREADS': '1'                           }),
            ('cpu_fs_t02',      'cpu', {'BH_VE_CPU_JIT_FUSION': '1',    'OMP_NUM_THREADS': '2'                           }),
            ('cpu_fs_t04',      'cpu', {'BH_VE_CPU_JIT_FUSION': '1',    'OMP_NUM_THREADS': '4'                           }),
            ('cpu_fs_t08',      'cpu', {'BH_VE_CPU_JIT_FUSION': '1',    'OMP_NUM_THREADS': '8'                           }),
            ('cpu_fs_t16',      'cpu', {'BH_VE_CPU_JIT_FUSION': '1',    'OMP_NUM_THREADS': '16'                          }),
            ('cpu_fs_t32',      'cpu', {'BH_VE_CPU_JIT_FUSION': '1',    'OMP_NUM_THREADS': '32'                          }),

            ('cpu_t01',         'cpu', {'BH_VE_CPU_JIT_FUSION': '0',    'OMP_NUM_THREADS': '1'                           }),
            ('cpu_t02',         'cpu', {'BH_VE_CPU_JIT_FUSION': '0',    'OMP_NUM_THREADS': '2'                           }),
            ('cpu_t04',         'cpu', {'BH_VE_CPU_JIT_FUSION': '0',    'OMP_NUM_THREADS': '4'                           }),
            ('cpu_t08',         'cpu', {'BH_VE_CPU_JIT_FUSION': '0',    'OMP_NUM_THREADS': '8'                           }),
            ('cpu_t16',         'cpu', {'BH_VE_CPU_JIT_FUSION': '0',    'OMP_NUM_THREADS': '16'                          }),
            ('cpu_t32',         'cpu', {'BH_VE_CPU_JIT_FUSION': '0',    'OMP_NUM_THREADS': '32'                          }),
        ]
    ],
    "use_slurm_default": True,
    "use_grapher": "cpu"
}

suites = [
    numpy,
    bohrium
]

