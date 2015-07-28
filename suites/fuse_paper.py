from benchpress.default import *

scripts = [
    ('Heat Equation',   'heat_equation',   '--size=100*100*1' ),
    ('nBody',           'nbody',           '--size=100*1'      ),
    ('Shallow Water',   'shallow_water',   '--size=100*100*1' ),
    ('Black Scholes',   'black_scholes',   '--size=1000*1'   ),
]

bh_stack_cpu_pricer = [
    [('default',    'bridge',       None)],
    [('bccon',      'bccon',        None)],
    [('bcexp',      'bcexp',        None)],
    [('topo',       'topological',  None)],
    [('node',       'node',         None)],
    [('pricer',     'pricer',       None)],
    [('cpu',        'cpu',  {"BH_CPU_JIT_LEVEL": "3"})],

]

bh_cpu_pricer_suite = {
    'scripts': scripts,
    'launchers':  [python_bohrium],
    'bohrium': bh_stack_cpu_pricer
}

suites = [
    bh_cpu_pricer_suite,
]

