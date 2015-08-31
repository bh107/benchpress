from benchpress.default import *

scripts = [
    ('Synth Init',   'synth_init',    '--size=500000000*10'),
]

stack_omp_t32 = [
    [('default',    'bridge',       None)],
    [('bccon',      'bccon',        None)],
    [('bcexp',      'bcexp',        None)],
    [('topo',       'topological',  None)],
    [('node',       'node',         None)],
    [
        ('omp_af_t32_pi_pe', 'cpu',  {"OMP_NUM_THREADS": "32", "SYNTH_INIT_MODE": 3, "GOMP_CPU_AFFINITY": "0-31" }),
        ('omp_af_t16_pi_pe', 'cpu',  {"OMP_NUM_THREADS": "16", "SYNTH_INIT_MODE": 3, "GOMP_CPU_AFFINITY": "0-31" }),
        ('omp_af_t08_pi_pe', 'cpu',  {"OMP_NUM_THREADS": "8",  "SYNTH_INIT_MODE": 3, "GOMP_CPU_AFFINITY": "0-31" }),
        ('omp_af_t04_pi_pe', 'cpu',  {"OMP_NUM_THREADS": "4",  "SYNTH_INIT_MODE": 3, "GOMP_CPU_AFFINITY": "0-31" }),
        ('omp_af_t02_pi_pe', 'cpu',  {"OMP_NUM_THREADS": "2",  "SYNTH_INIT_MODE": 3, "GOMP_CPU_AFFINITY": "0-31" }),
        ('omp_af_t01_pi_pe', 'cpu',  {"OMP_NUM_THREADS": "1",  "SYNTH_INIT_MODE": 3, "GOMP_CPU_AFFINITY": "0-31" }),

        ('omp_af_t32_si_pe', 'cpu',  {"OMP_NUM_THREADS": "32", "SYNTH_INIT_MODE": 2, "GOMP_CPU_AFFINITY": "0-31" }),
        ('omp_af_t16_si_pe', 'cpu',  {"OMP_NUM_THREADS": "16", "SYNTH_INIT_MODE": 2, "GOMP_CPU_AFFINITY": "0-31" }),
        ('omp_af_t08_si_pe', 'cpu',  {"OMP_NUM_THREADS": "8",  "SYNTH_INIT_MODE": 2, "GOMP_CPU_AFFINITY": "0-31" }),
        ('omp_af_t04_si_pe', 'cpu',  {"OMP_NUM_THREADS": "4",  "SYNTH_INIT_MODE": 2, "GOMP_CPU_AFFINITY": "0-31" }),
        ('omp_af_t02_si_pe', 'cpu',  {"OMP_NUM_THREADS": "2",  "SYNTH_INIT_MODE": 2, "GOMP_CPU_AFFINITY": "0-31" }),
        ('omp_af_t01_si_pe', 'cpu',  {"OMP_NUM_THREADS": "1",  "SYNTH_INIT_MODE": 2, "GOMP_CPU_AFFINITY": "0-31" }),

        ('omp_t32_pi_pe',    'cpu',  {"OMP_NUM_THREADS": "32", "SYNTH_INIT_MODE": 3}),
        ('omp_t16_pi_pe',    'cpu',  {"OMP_NUM_THREADS": "16", "SYNTH_INIT_MODE": 3}),
        ('omp_t08_pi_pe',    'cpu',  {"OMP_NUM_THREADS": "8",  "SYNTH_INIT_MODE": 3}),
        ('omp_t04_pi_pe',    'cpu',  {"OMP_NUM_THREADS": "4",  "SYNTH_INIT_MODE": 3}),
        ('omp_t02_pi_pe',    'cpu',  {"OMP_NUM_THREADS": "2",  "SYNTH_INIT_MODE": 3}),
        ('omp_t01_pi_pe',    'cpu',  {"OMP_NUM_THREADS": "1",  "SYNTH_INIT_MODE": 3}),

        ('omp_t32_si_pe',    'cpu',  {"OMP_NUM_THREADS": "32", "SYNTH_INIT_MODE": 2}),
        ('omp_t16_si_pe',    'cpu',  {"OMP_NUM_THREADS": "16", "SYNTH_INIT_MODE": 2}),
        ('omp_t08_si_pe',    'cpu',  {"OMP_NUM_THREADS": "8",  "SYNTH_INIT_MODE": 2}),
        ('omp_t04_si_pe',    'cpu',  {"OMP_NUM_THREADS": "4",  "SYNTH_INIT_MODE": 2}),
        ('omp_t02_si_pe',    'cpu',  {"OMP_NUM_THREADS": "2",  "SYNTH_INIT_MODE": 2}),
        ('omp_t01_si_pe',    'cpu',  {"OMP_NUM_THREADS": "1",  "SYNTH_INIT_MODE": 2}),
    ]
]

omp = {
    'scripts': scripts,
    'launchers': [c99_omp],
    'bohrium': stack_omp_t32,
    "use_slurm_default": True,
    "use_grapher": "cpu"
}

#
#   As usual, put them into the list of suites to run.
#
suites = [
    omp
]

