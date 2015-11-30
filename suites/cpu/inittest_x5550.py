from benchpress.default import *

scripts = [
    ('Synth Init',   'synth_init',    '--size=100000000*10'),
]

stack_parallel = [
    [('default',    'bridge',       None)],
    [('bccon',      'bccon',        None)],
    [('bcexp',      'bcexp',        None)],
    [('topo',       'topological',  None)],
    [('node',       'node',         None)],
    [
        ('omp_af2_pi_pe_t08', 'cpu',  {"OMP_NUM_THREADS": "08", "SYNTH_INIT_MODE": 3, "GOMP_CPU_AFFINITY": "0 4 1 5 2 6 3 7" }),
        ('omp_af2_pi_pe_t06', 'cpu',  {"OMP_NUM_THREADS": "06", "SYNTH_INIT_MODE": 3, "GOMP_CPU_AFFINITY": "0 4 1 5 2 6 3 7" }),
        ('omp_af2_pi_pe_t04', 'cpu',  {"OMP_NUM_THREADS": "04", "SYNTH_INIT_MODE": 3, "GOMP_CPU_AFFINITY": "0 4 1 5 2 6 3 7" }),
        ('omp_af2_pi_pe_t02', 'cpu',  {"OMP_NUM_THREADS": "02", "SYNTH_INIT_MODE": 3, "GOMP_CPU_AFFINITY": "0 4 1 5 2 6 3 7" }),
        ('omp_af2_pi_pe_t01', 'cpu',  {"OMP_NUM_THREADS": "1",  "SYNTH_INIT_MODE": 3, "GOMP_CPU_AFFINITY": "0 4 1 5 2 6 3 7" }),
        
        ('omp_af2_si_pe_t08', 'cpu',  {"OMP_NUM_THREADS": "08", "SYNTH_INIT_MODE": 2, "GOMP_CPU_AFFINITY": "0 4 1 5 2 6 3 7" }),
        ('omp_af2_si_pe_t06', 'cpu',  {"OMP_NUM_THREADS": "06", "SYNTH_INIT_MODE": 2, "GOMP_CPU_AFFINITY": "0 4 1 5 2 6 3 7" }),
        ('omp_af2_si_pe_t04', 'cpu',  {"OMP_NUM_THREADS": "04", "SYNTH_INIT_MODE": 2, "GOMP_CPU_AFFINITY": "0 4 1 5 2 6 3 7" }),
        ('omp_af2_si_pe_t02', 'cpu',  {"OMP_NUM_THREADS": "02", "SYNTH_INIT_MODE": 2, "GOMP_CPU_AFFINITY": "0 4 1 5 2 6 3 7" }),
        ('omp_af2_si_pe_t01', 'cpu',  {"OMP_NUM_THREADS": "1",  "SYNTH_INIT_MODE": 2, "GOMP_CPU_AFFINITY": "0 4 1 5 2 6 3 7 " }),

        ('omp_af_pi_pe_t08', 'cpu',  {"OMP_NUM_THREADS": "08", "SYNTH_INIT_MODE": 3, "GOMP_CPU_AFFINITY": "0-8" }),
        ('omp_af_pi_pe_t06', 'cpu',  {"OMP_NUM_THREADS": "06", "SYNTH_INIT_MODE": 3, "GOMP_CPU_AFFINITY": "0-8" }),
        ('omp_af_pi_pe_t04', 'cpu',  {"OMP_NUM_THREADS": "04", "SYNTH_INIT_MODE": 3, "GOMP_CPU_AFFINITY": "0-8" }),
        ('omp_af_pi_pe_t02', 'cpu',  {"OMP_NUM_THREADS": "02", "SYNTH_INIT_MODE": 3, "GOMP_CPU_AFFINITY": "0-8" }),
        ('omp_af_pi_pe_t01', 'cpu',  {"OMP_NUM_THREADS": "1",  "SYNTH_INIT_MODE": 3, "GOMP_CPU_AFFINITY": "0-8" }),

        ('omp_af_si_pe_t08', 'cpu',  {"OMP_NUM_THREADS": "08", "SYNTH_INIT_MODE": 2, "GOMP_CPU_AFFINITY": "0-8" }),
        ('omp_af_si_pe_t06', 'cpu',  {"OMP_NUM_THREADS": "06", "SYNTH_INIT_MODE": 2, "GOMP_CPU_AFFINITY": "0-8" }),
        ('omp_af_si_pe_t04', 'cpu',  {"OMP_NUM_THREADS": "04", "SYNTH_INIT_MODE": 2, "GOMP_CPU_AFFINITY": "0-8" }),
        ('omp_af_si_pe_t02', 'cpu',  {"OMP_NUM_THREADS": "02", "SYNTH_INIT_MODE": 2, "GOMP_CPU_AFFINITY": "0-8" }),
        ('omp_af_si_pe_t01', 'cpu',  {"OMP_NUM_THREADS": "1",  "SYNTH_INIT_MODE": 2, "GOMP_CPU_AFFINITY": "0-8" }),

        ('omp_pi_pe_t08',    'cpu',  {"OMP_NUM_THREADS": "08", "SYNTH_INIT_MODE": 3}),
        ('omp_pi_pe_t06',    'cpu',  {"OMP_NUM_THREADS": "06", "SYNTH_INIT_MODE": 3}),
        ('omp_pi_pe_t04',    'cpu',  {"OMP_NUM_THREADS": "04", "SYNTH_INIT_MODE": 3}),
        ('omp_pi_pe_t02',    'cpu',  {"OMP_NUM_THREADS": "02", "SYNTH_INIT_MODE": 3}),
        ('omp_pi_pe_t01',    'cpu',  {"OMP_NUM_THREADS": "1",  "SYNTH_INIT_MODE": 3}),

        ('omp_si_pe_t08',    'cpu',  {"OMP_NUM_THREADS": "08", "SYNTH_INIT_MODE": 2}),
        ('omp_si_pe_t06',    'cpu',  {"OMP_NUM_THREADS": "06", "SYNTH_INIT_MODE": 2}),
        ('omp_si_pe_t04',    'cpu',  {"OMP_NUM_THREADS": "04", "SYNTH_INIT_MODE": 2}),
        ('omp_si_pe_t02',    'cpu',  {"OMP_NUM_THREADS": "02", "SYNTH_INIT_MODE": 2}),
        ('omp_si_pe_t01',    'cpu',  {"OMP_NUM_THREADS": "1",  "SYNTH_INIT_MODE": 2}),
    ]
]

serial = {
    'scripts': scripts,
    'launchers': [
        ('C/SEQ', '`bp-info --benchmarks`/{script}/c99_omp/bin/{script} {args}', {"SYNTH_INIT_MODE": 0})
    ],
    'bohrium': bh_stack_none,
    "use_slurm_default": True,
    "use_grapher": "cpu"
}

parallel = {
    'scripts': scripts,
    'launchers': [
        ('C/OMP',     '`bp-info --benchmarks`/{script}/c99_omp/bin/{script} {args}', None)
    ],
    'bohrium': stack_parallel,
    "use_slurm_default": True,
    "use_grapher": "cpu"
}


#
#   As usual, put them into the list of suites to run.
#
suites = [
    serial,
    parallel
]

