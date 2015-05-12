from benchpress.default import *

bh_stack_cpu_t32 = [
    [('default',    'bridge',             None)],
    [('node',       'node',               None)],
    [('fuser',      'singleton',          None)],
    [
        ('cpu_t32', 'cpu',   {"OMP_NUM_THREADS": "32"}),
        ('cpu_t16', 'cpu',   {"OMP_NUM_THREADS": "16"}),
        ('cpu_t08', 'cpu',   {"OMP_NUM_THREADS": "8"}),
        ('cpu_t04', 'cpu',   {"OMP_NUM_THREADS": "4"}),
        ('cpu_t02', 'cpu',   {"OMP_NUM_THREADS": "2"}),
        ('cpu_t01', 'cpu',   {"OMP_NUM_THREADS": "1"}),
    ]
]

scripts = [
    ('Heat Equation',   'heat_equation_fixed',   '--size=5000*5000*10' ),
    ('nBody',           'nbody',                 '--size=5000*10'      ),
    ('Shallow Water',   'shallow_water',         '--size=5000*5000*10' ),
    ('Black Scholes',   'black_scholes',         '--size=3200000*36'   ),
    ('nBody Nice',      'nbody_nice',            '--size=15*1000000*10')
]


bh_cpu_t32_suite = {
    'scripts': scripts,
    'launchers': [cil_bohrium],
    'bohrium': bh_stack_cpu_t32
}

reference_suite = {
    'scripts': scripts,
    'launchers': [python_numpy, cil_managed, cil_unsafe]
}

np_bh_ref_suite = {
    'scripts': scripts,
    'launchers': [python_bohrium],
    'bohrium': bh_stack_cpu_t32    
}


suites = [
    bh_cpu_t32_suite,
    reference_suite,
    np_bh_ref_suite
]

