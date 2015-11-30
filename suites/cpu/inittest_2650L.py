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
        ('omp_af2_pi_pe_t24', 'cpu',  {"OMP_NUM_THREADS": "24", "SYNTH_INIT_MODE": 3, "GOMP_CPU_AFFINITY": "0 12 1 13 2 14 3 15 4 16 5 17 6 18 7 19 8 20 9 21 10 22 11 23" }),
        ('omp_af2_pi_pe_t20', 'cpu',  {"OMP_NUM_THREADS": "20", "SYNTH_INIT_MODE": 3, "GOMP_CPU_AFFINITY": "0 12 1 13 2 14 3 15 4 16 5 17 6 18 7 19 8 20 9 21 10 22 11 23" }),
        ('omp_af2_pi_pe_t16', 'cpu',  {"OMP_NUM_THREADS": "16", "SYNTH_INIT_MODE": 3, "GOMP_CPU_AFFINITY": "0 12 1 13 2 14 3 15 4 16 5 17 6 18 7 19 8 20 9 21 10 22 11 23" }),
        ('omp_af2_pi_pe_t12', 'cpu',  {"OMP_NUM_THREADS": "12", "SYNTH_INIT_MODE": 3, "GOMP_CPU_AFFINITY": "0 12 1 13 2 14 3 15 4 16 5 17 6 18 7 19 8 20 9 21 10 22 11 23" }),
        ('omp_af2_pi_pe_t08', 'cpu',  {"OMP_NUM_THREADS": "08", "SYNTH_INIT_MODE": 3, "GOMP_CPU_AFFINITY": "0 12 1 13 2 14 3 15 4 16 5 17 6 18 7 19 8 20 9 21 10 22 11 23" }),
        ('omp_af2_pi_pe_t04', 'cpu',  {"OMP_NUM_THREADS": "04", "SYNTH_INIT_MODE": 3, "GOMP_CPU_AFFINITY": "0 12 1 13 2 14 3 15 4 16 5 17 6 18 7 19 8 20 9 21 10 22 11 23" }),
        ('omp_af2_pi_pe_t01', 'cpu',  {"OMP_NUM_THREADS": "1",  "SYNTH_INIT_MODE": 3, "GOMP_CPU_AFFINITY": "0 12 1 13 2 14 3 15 4 16 5 17 6 18 7 19 8 20 9 21 10 22 11 23" }),
        
        ('omp_af2_si_pe_t24', 'cpu',  {"OMP_NUM_THREADS": "24", "SYNTH_INIT_MODE": 2, "GOMP_CPU_AFFINITY": "0 12 1 13 2 14 3 15 4 16 5 17 6 18 7 19 8 20 9 21 10 22 11 23" }),
        ('omp_af2_si_pe_t20', 'cpu',  {"OMP_NUM_THREADS": "20", "SYNTH_INIT_MODE": 2, "GOMP_CPU_AFFINITY": "0 12 1 13 2 14 3 15 4 16 5 17 6 18 7 19 8 20 9 21 10 22 11 23" }),
        ('omp_af2_si_pe_t16', 'cpu',  {"OMP_NUM_THREADS": "16", "SYNTH_INIT_MODE": 2, "GOMP_CPU_AFFINITY": "0 12 1 13 2 14 3 15 4 16 5 17 6 18 7 19 8 20 9 21 10 22 11 23" }),
        ('omp_af2_si_pe_t12', 'cpu',  {"OMP_NUM_THREADS": "12", "SYNTH_INIT_MODE": 2, "GOMP_CPU_AFFINITY": "0 12 1 13 2 14 3 15 4 16 5 17 6 18 7 19 8 20 9 21 10 22 11 23" }),
        ('omp_af2_si_pe_t08', 'cpu',  {"OMP_NUM_THREADS": "08", "SYNTH_INIT_MODE": 2, "GOMP_CPU_AFFINITY": "0 12 1 13 2 14 3 15 4 16 5 17 6 18 7 19 8 20 9 21 10 22 11 23" }),
        ('omp_af2_si_pe_t04', 'cpu',  {"OMP_NUM_THREADS": "04", "SYNTH_INIT_MODE": 2, "GOMP_CPU_AFFINITY": "0 12 1 13 2 14 3 15 4 16 5 17 6 18 7 19 8 20 9 21 10 22 11 23" }),
        ('omp_af2_si_pe_t01', 'cpu',  {"OMP_NUM_THREADS": "1",  "SYNTH_INIT_MODE": 2, "GOMP_CPU_AFFINITY": "0 12 1 13 2 14 3 15 4 16 5 17 6 18 7 19 8 20 9 21 10 22 11 23" }),

        ('omp_af_pi_pe_t24', 'cpu',  {"OMP_NUM_THREADS": "24", "SYNTH_INIT_MODE": 3, "GOMP_CPU_AFFINITY": "0-24" }),
        ('omp_af_pi_pe_t20', 'cpu',  {"OMP_NUM_THREADS": "20", "SYNTH_INIT_MODE": 3, "GOMP_CPU_AFFINITY": "0-24" }),
        ('omp_af_pi_pe_t16', 'cpu',  {"OMP_NUM_THREADS": "16", "SYNTH_INIT_MODE": 3, "GOMP_CPU_AFFINITY": "0-24" }),
        ('omp_af_pi_pe_t12', 'cpu',  {"OMP_NUM_THREADS": "12", "SYNTH_INIT_MODE": 3, "GOMP_CPU_AFFINITY": "0-24" }),
        ('omp_af_pi_pe_t08', 'cpu',  {"OMP_NUM_THREADS": "08", "SYNTH_INIT_MODE": 3, "GOMP_CPU_AFFINITY": "0-24" }),
        ('omp_af_pi_pe_t04', 'cpu',  {"OMP_NUM_THREADS": "04", "SYNTH_INIT_MODE": 3, "GOMP_CPU_AFFINITY": "0-24" }),
        ('omp_af_pi_pe_t01', 'cpu',  {"OMP_NUM_THREADS": "1",  "SYNTH_INIT_MODE": 3, "GOMP_CPU_AFFINITY": "0-24" }),

        ('omp_af_si_pe_t24', 'cpu',  {"OMP_NUM_THREADS": "24", "SYNTH_INIT_MODE": 2, "GOMP_CPU_AFFINITY": "0-24" }),
        ('omp_af_si_pe_t20', 'cpu',  {"OMP_NUM_THREADS": "20", "SYNTH_INIT_MODE": 2, "GOMP_CPU_AFFINITY": "0-24" }),
        ('omp_af_si_pe_t16', 'cpu',  {"OMP_NUM_THREADS": "16", "SYNTH_INIT_MODE": 2, "GOMP_CPU_AFFINITY": "0-24" }),
        ('omp_af_si_pe_t12', 'cpu',  {"OMP_NUM_THREADS": "12", "SYNTH_INIT_MODE": 2, "GOMP_CPU_AFFINITY": "0-24" }),
        ('omp_af_si_pe_t08', 'cpu',  {"OMP_NUM_THREADS": "08", "SYNTH_INIT_MODE": 2, "GOMP_CPU_AFFINITY": "0-24" }),
        ('omp_af_si_pe_t04', 'cpu',  {"OMP_NUM_THREADS": "04", "SYNTH_INIT_MODE": 2, "GOMP_CPU_AFFINITY": "0-24" }),
        ('omp_af_si_pe_t01', 'cpu',  {"OMP_NUM_THREADS": "1",  "SYNTH_INIT_MODE": 2, "GOMP_CPU_AFFINITY": "0-24" }),

        ('omp_pi_pe_t24',    'cpu',  {"OMP_NUM_THREADS": "24", "SYNTH_INIT_MODE": 3}),
        ('omp_pi_pe_t20',    'cpu',  {"OMP_NUM_THREADS": "20", "SYNTH_INIT_MODE": 3}),
        ('omp_pi_pe_t16',    'cpu',  {"OMP_NUM_THREADS": "16", "SYNTH_INIT_MODE": 3}),
        ('omp_pi_pe_t12',    'cpu',  {"OMP_NUM_THREADS": "12", "SYNTH_INIT_MODE": 3}),
        ('omp_pi_pe_t08',    'cpu',  {"OMP_NUM_THREADS": "08", "SYNTH_INIT_MODE": 3}),
        ('omp_pi_pe_t04',    'cpu',  {"OMP_NUM_THREADS": "04", "SYNTH_INIT_MODE": 3}),
        ('omp_pi_pe_t01',    'cpu',  {"OMP_NUM_THREADS": "1",  "SYNTH_INIT_MODE": 3}),

        ('omp_si_pe_t24',    'cpu',  {"OMP_NUM_THREADS": "24", "SYNTH_INIT_MODE": 2}),
        ('omp_si_pe_t20',    'cpu',  {"OMP_NUM_THREADS": "20", "SYNTH_INIT_MODE": 2}),
        ('omp_si_pe_t16',    'cpu',  {"OMP_NUM_THREADS": "16", "SYNTH_INIT_MODE": 2}),
        ('omp_si_pe_t12',    'cpu',  {"OMP_NUM_THREADS": "12", "SYNTH_INIT_MODE": 2}),
        ('omp_si_pe_t08',    'cpu',  {"OMP_NUM_THREADS": "08", "SYNTH_INIT_MODE": 2}),
        ('omp_si_pe_t04',    'cpu',  {"OMP_NUM_THREADS": "04", "SYNTH_INIT_MODE": 2}),
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

