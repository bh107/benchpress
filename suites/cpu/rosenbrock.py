from benchpress.default import *
from bp_cpu_shared import *

scripts = [
    ('Rosenbrock',   'rosenbrock',  '--size=100000000*10'),
]

multicore = {
    'scripts': scripts,
    'launchers': [cpp11_omp, python_bohrium],
    'bohrium': bh_stack_cpu_t32,
    "use_slurm_default": True,
}

sequential = {
    'scripts': scripts,
    'launchers': [c99_seq, cpp11_seq],
    'bohrium': bh_stack_none,
    "use_slurm_default": True,
}

numpy = {
    'scripts': scripts,
    'launchers': [python_numpy],
    'bohrium': bh_stack_none,
    "use_slurm_default": True,
}

suites = [
    numpy,
    sequential,
    multicore
]
