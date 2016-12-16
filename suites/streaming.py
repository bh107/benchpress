from benchpress.default import *

scripts = [
    ('X-ray 1e10',   'xraysim',             '--size=20*40*10'),
    ('MC Pi 1.2e10', 'montecarlo_pi',       '--size=100000000*10'),
    ('MFE 2.3e10',   'idl_init_explode',    '--size=40*40*10'),
    ('BEAN 5e9',     'galton_bean_machine', '--size=100000*10000'),   

    ('X-ray 1e11', 'xraysim',  '--size=43*40*10'),
    ('X-ray 1e12', 'xraysim',  '--size=93*40*10'),
    ('X-ray 1e13', 'xraysim',  '--size=200*40*10'),

    ('MC Pi 1.2e11', 'montecarlo_pi',  '--size=1000000000*10'),
    ('MC Pi 1.2e12', 'montecarlo_pi',  '--size=10000000000*10'),
    ('MC Pi 1.2e13', 'montecarlo_pi',  '--size=100000000000*10'),

    ('MFE 2.3e11', 'idl_init_explode', '--size=63*63*10'),
    ('MFE 2.3e12', 'idl_init_explode', '--size=100*100*10'),
    ('MFE 2.3e13', 'idl_init_explode', '--size=159*159*10'),

    ('BEAN 5e10', 'galton_bean_machine', '--size=1000000*10000'),   
    ('BEAN 5e11', 'galton_bean_machine', '--size=10000000*10000'), 
    ('BEAN 5e12', 'galton_bean_machine', '--size=100000000*10000'),
]

stack_openmp = [
    [('default',    'bridge',  None)],
    [('bcexp',      'bcexp',   None)],
    [('bccon',      'bccon',   None)],
    [('node',       'node',    None)],
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
    'scripts': scripts[:4], # NumPy can only do the three smallest tests
    'launchers':  [python_numpy],
    'bohrium': bh_stack_none
}

suites = [
    suite_openmp,
    suite_opencl,
    suite_numpy
]

