from benchpress.default import *

scripts = [
    ('X-ray 020^3 40^2',  'xraysim',    '--size=20*40*5'),
    ('MC Pi 0.1G',   'montecarlo_pi',    '--size=100000000*5'),
    ('MFE 040^2',    'idl_init_explode', '--size=40*40*5'),

    ('X-ray 043^3 040^2',  'xraysim',    '--size=43*40*5'),
    ('X-ray 093^3 040^2',  'xraysim',    '--size=93*40*5'),
    ('X-ray 200^3 040^2',  'xraysim',    '--size=200*40*5'),

    ('MC Pi 1G',    'montecarlo_pi',    '--size=1000000000*5'),
    ('MC Pi 10G',    'montecarlo_pi',    '--size=10000000000*5'),
    ('MC Pi 100G',   'montecarlo_pi',    '--size=100000000000*5'),

    ('MFE 063^2',    'idl_init_explode', '--size=63*63*5'),
    ('MFE 100^2',    'idl_init_explode', '--size=100*100*5'),
    ('MFE 159^2',    'idl_init_explode', '--size=159*159*5'),
]

stack_openmp = [
    [('default',    'bridge',       None)],
    [('bcexp',      'bcexp_openmp', None)],
    [('bccon',      'bccon_openmp', None)],
    [('node',       'node',         None)],
    [('openmp',     'openmp',       None)],
]

stack_opencl = [
    [('default',    'bridge',       None)],
    [('bcexp',      'bcexp_openmp', None)],
    [('bccon',      'bccon_openmp', None)],
    [('node',       'node',         None)],
    [('opencl',     'opencl',       None)],
    [('openmp',     'openmp',       None)],
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
    'scripts': scripts[:3], # NumPy can only do the three smallest tests
    'launchers':  [python_numpy],
    'bohrium': bh_stack_none
}

suites = [
    suite_openmp,
    suite_opencl,
    suite_numpy,
]

