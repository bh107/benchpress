from benchpress.default import *

scripts_cpu = [
    ('Game of Life',            'gameoflife',               '--size=9000*9000*40*2'),
    ('Jacobi Solver',           'jacobi',                   '--size=10000*40'),
    ('Black Scholes',           'black_scholes',            '--size=15000000*40'),
    ('Heat Equation',           'heat_equation',            '--size=12000*12000*40'),
    ('Gauss Elimination',       'gauss',                    '--size=2800'),
    ('LU Factorization',        'lu',                       '--size=2800'),
    ('Monte Carlo Pi',          'montecarlo_pi',            '--size=100000000*40'),
    ('Leibnitz Pi',             'leibnitz_pi',              '--size=700000000'),
    ('27 Point Stencil',        'point27',                  '--size=350*40'),
    ('Rosenbrock',              'rosenbrock',               '--size=200000000*40'),
]

stack_cpu = [
    [('default',    'bridge',       None)],
    [('bcexp',      'bcexp',        None)],
    [('bccon',      'bccon',        None)],
    [('topological','topological',  None)],
    [('node',       'node',         None)],
    [('cpu',        'cpu',  {"BH_CPU_JIT_LEVEL": "3", "OMP_NUM_THREADS":"1"})],
]

stack_uni = [
    [('default',    'bridge',       None)],
    [('bcexp',      'bcexp',        None)],
    [('bccon',      'bccon',        None)],
    [('node',       'node',         None)],
    [('uni',        'uni',          None)],
]

suite_cpu = {
    'scripts': scripts_cpu,
    'launchers':  [python_bohrium],
    'bohrium': stack_cpu
}
suite_uni = {
    'scripts': scripts_cpu,
    'launchers':  [python_bohrium],
    'bohrium': stack_uni
}
suites = [
    suite_cpu,
    suite_uni,
]

