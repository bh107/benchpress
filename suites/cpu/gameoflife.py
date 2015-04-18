from benchpress.default import *
from bp_cpu_shared import *

scripts = [
    ('Game of Life v1',   'gameoflife',  '--size=10000*10000*10*1'),
    ('Game of Life v2',   'gameoflife',  '--size=10000*10000*10*2'),
]

multicore = {
    'scripts': scripts,
    'launchers': [python_bohrium],
    'bohrium': bh_stack_cpu_t32
}

numpy = {
    'scripts': scripts,
    'launchers': [python_numpy],
    'bohrium': bh_stack_none
}

suites = [
    numpy,
    multicore
]
