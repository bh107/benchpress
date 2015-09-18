from benchpress.default import *
from bp_cpu_shared import *

scripts = [
    ('Black Scholes',   'black_scholes',    '--size=5000000*10'),
]


cpp11_bxx           = ('BXX/+OPT',    '`bp-info --benchmarks`/{script}/cpp11_bxx/bin/{script} {args}', {"BCEXP_CPU_POWK": "1"})
cpp11_bxx_powk_off  = ('BXX/-OPT',    '`bp-info --benchmarks`/{script}/cpp11_bxx/bin/{script} {args}', {"BCEXP_CPU_POWK": "0"})

bohrium = {
    'scripts': scripts,
    'launchers': [cpp11_bxx, cpp11_bxx_powk_off],
    'bohrium': bh_stack_cpu_t32_best,
    "use_slurm_default": True,
    "use_grapher": "cpu"
}

omp = {
    'scripts': scripts,
    'launchers': [cpp11_omp, cpp11_blitz, cpp11_arma],
    'bohrium': stack_omp_t32,
    "use_slurm_default": True,
    "use_grapher": "cpu"
}

#
#   As usual, put them into the list of suites to run.
#
suites = [
    bohrium,
    omp
]
