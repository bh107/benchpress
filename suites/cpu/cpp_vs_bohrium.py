from benchpress.default import *
from bp_cpu_shared import *

scripts = [
    ('Heat Equation',   'heat_equation',    '--size=14000*14000*10'),
    ('Game of Life v1', 'gameoflife',       '--size=10000*10000*10*1'),
    ('Game of Life v2', 'gameoflife',       '--size=10000*10000*10*2'),
    ('Leibnitz PI',     'leibnitz_pi',      '--size=200000000'),
    ('Montecarlo PI',   'montecarlo_pi',    '--size=200000000'),
    ('Mxmul',           'mxmul',            '--size=1500'),
    ('Rosenbrock',      'rosenbrock',       '--size=100000000*10'),
    ('Shallow Water',   'shallow_water',    '--size=5000*5000*10'),
]

bohrium = {
    'scripts': scripts,
    'launchers': [python_bohrium, cpp11_bxx],
    'bohrium': bh_stack_cpu_t32_best,
    "use_slurm_default": True,
    "use_grapher": "cpu"
}

cpp = {
    'scripts': scripts,
    'launchers': [cpp11_omp],
    'bohrium': stack_omp_t32,
    "use_slurm_default": True,
    "use_grapher": "cpu"
}

#
#   As usual, put them into the list of suites to run.
#
suites = [
    cpp,
    bohrium
]
