from benchpress.default import *
from bp_cpu_shared import *

scripts = [
    ('Leibnitz PI', 'leibnitz_pi', '--size=100000000'),
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
    'bohrium':  bp_stack_cpu_t4,
    "use_slurm_default": True,
    "use_grapher": "cpu"
}

suites = [
    numpy,
    bohrium
]

