from benchpress.default import *

scripts = [
    ('X-ray',                'xraysim',        		 '--size=43*40*10'),
    ('MC Pi',                'montecarlo_pi',  		 '--size=1000000000*10'),
    ('MFE',                  'magnetic_field_extrapolation', '--size=63*63*10'),
    ('BEAN',                 'galton_bean_machine',      '--size=1000000*10000'),
    ('Black Scholes',        'black_scholes',            '--size=15000000*40'),
    ('Game of Life',         'gameoflife',               '--size=9000*9000*40*2'),
    ('Gauss Elimination',    'gauss',                    '--size=2800'),
    ('LU Factorization',     'lu',                       '--size=2800'),
    ('Leibnitz Pi',          'leibnitz_pi',              '--size=700000000'),
    ('27 Point Stencil',     'point27',                  '--size=350*40'),
    ('Rosenbrock',           'rosenbrock',               '--size=200000000*40'),
    ('Heat Equation',        'heat_equation',            '--size=10000*10000*40'),
    ('Shallow Water',        'shallow_water',            '--size=8000*8000*40'),
    ('N-Body',               'nbody',                    '--size=5000*40'),
    ('Wire World',           'wireworld',                '--size=1000*100'),
    ('Rosenbrock',           'rosenbrock',               '--size=500000000*40'),
]

stack_openmp = [
    [('default',    'bridge',  None)],
    [('bcexp',      'bcexp',   None)],
    [('bccon',      'bccon',   None)],
    [\
      ('CPU1',      'node',   {'OMP_NUM_THREADS': '1'}),
      ('CPU',       'node',    None),
    ],
    [('openmp',     'openmp',  None)],
]

stack_opencl = [
    [('default',    'bridge',  None)],
    [('bcexp',      'bcexp',   None)],
    [('bccon',      'bccon',   None)],
    [('node',       'node',    None)],
    [('opencl',     'opencl',  None)],
    [('openmp',     'openmp',  None)],
]

suite_openmp = {
    'scripts': scripts,
    'launchers':  [python_bohrium],
    'bohrium': stack_openmp
}
suite_opencl = {
    'scripts': scripts,
    'launchers':  [python_bohrium],
    'bohrium': stack_opencl
}
suite_numpy = {
    'scripts': scripts,
    'launchers':  [python_numpy],
    'bohrium': bh_stack_none
}

suites = [
    suite_opencl,
    suite_openmp,
    suite_numpy,
]


