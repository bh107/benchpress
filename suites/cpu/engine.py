from benchpress.default import *
from bp_cpu_shared import *

scripts = [
    ('Heat Equation',   'heat_equation',    '--size=14000*14000*10'),
    ('Leibnitz PI',     'leibnitz_pi',      '--size=200000000'),
    ('Rosenbrock',      'rosenbrock',       '--size=100000000*10'),
]

bohrium = {
    'scripts': scripts,
    'launchers': [python_bohrium],
    'bohrium': bh_stack_cpu_t32_all
}

omp = {
    'scripts': scripts,
    'launchers': [cpp11_omp],
    'bohrium': stack_omp_t32
}

cseq = {
    'scripts': scripts,
    'launchers': [c99_seq],
    'bohrium': bh_stack_none
}

np = {
    'scripts': scripts,
    'launchers': [python_numpy],
    'bohrium': bh_stack_none
}

#
#   As usual, put them into the list of suites to run.
#
suites = [
    cseq,
    omp,
    bohrium,
    np
]
