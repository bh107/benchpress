from benchpress.default import *
from bp_cpu_shared import *

scripts = [
    ('Water-Ice Simulation', 'wisp', '--size=1000*1000*10'),
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
    'bohrium':  bh_stack_cpu_t8,
    "use_slurm_default": True,
    "use_grapher": "cpu"
}

suites = [
    numpy,
    bohrium
]

