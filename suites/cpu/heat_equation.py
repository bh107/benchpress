from benchpress.default import *
from bp_cpu_shared import *

scripts = [
    ('Heat Equation', 'heat_equation', '--size=14000*14000*10'),
]

sequential = {
    'scripts': scripts,
    'launchers': [c99_seq],
    'bohrium': bh_stack_none,
    "use_slurm_default": True,
    "use_grapher": "cpu"
}

multicore = {
    'scripts': scripts,
    'launchers': [c99_omp, cpp11_omp],
    'bohrium': stack_omp_t32,
    "use_slurm_default": True,
    "use_grapher": "cpu"
}

bohrium = {
    'scripts': scripts,
    'launchers': [python_bohrium, cpp11_bxx],
    'bohrium': bh_stack_cpu_t32_best,
    "use_slurm_default": True,
    "use_grapher": "cpu"
}

suites = [
    sequential,
    multicore,
    bohrium
]
