from benchpress.default import *

scripts = [
    ('Heat Equation',   'heat_equation',   '--size=100*100*1' ),
    ('nBody',           'nbody',           '--size=100*1'      ),
    ('nBody-NICE',      'nbody_nice',      '--size=100*100*1'  ),
    ('Shallow Water',   'shallow_water',   '--size=100*100*1' ),
    ('Black Scholes',   'black_scholes',   '--size=1000*1'   ),
    ('Jacobi Fixed',    'jacobi_fixed',    '--size=1000*1'   ),
    ('SOR',             'sor',             '--size=100*100*1'   ),
    ('MonteCarlo',      'montecarlo_pi',   '--size=1000*1'   ),
    ('GameOfLife',      'gameoflife',      '--size=100*100*1*1'   ),
    ('Gauss',           'gauss',           '--size=100*100*1'   ),
    ('LU',              'lu',              '--size=100*100*1'   ),
    ('Synth',           'synth',           '--size=100*1'   ),
    ('point27',         'point27',         '--size=100*1'   ),
    ('rosenbrock',      'rosenbrock',      '--size=100*1'   ),
    ('wisp',            'wisp',            '--size=100*100*1'   ),
#    ('lbm_3d',          'lbm_3d',          '--size=10*10*10*1'   ),
#    ('lbm_2d',          'lbm_2d',          '--size=10*10*1'   ),
#    ('wireworld',       'wireworld',       '--size=10*1'   ),
]

testscripts = [
        #('Heat Equation',   'heat_equation',   '--size=100*100*1' ),
    ('nBody-NICE',      'nbody_nice',      '--size=100*100*1'  ),
    #('Shallow Water',   'shallow_water',   '--size=100*100*1' ),
    ]

bh_stack_cpu_pricer = [
    [('default',    'bridge',       None)],
    [('bccon',      'bccon',        None)],
    [('bcexp',      'bcexp',        None)],
    [
        ('single',     'singleton',   {"BH_SINGLETON_FUSE_CACHE": "true"}),
        ('topo',       'topological', {"BH_TOPOLOGICAL_FUSE_CACHE": "true"}),
        ('greedy',     'greedy',      {"BH_GREEDY_FUSE_CACHE": "true"}),
        ('optimal',    'optimal',     {"BH_OPTIMAL_FUSE_CACHE": "true"}),
    ],
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

