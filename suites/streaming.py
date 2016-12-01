from benchpress.default import *

scripts = [
    ('X-ray 50^3 020^2',  'xraysim',    '--size=50*20*5'),
    ('MC Pi 0.1G',   'montecarlo_pi',    '--size=100000000*5'),
    ('MFE 040^2',    'idl_init_explode', '--size=40*40*5'),

    ('X-ray 50^3 063^2',  'xraysim',    '--size=50*63*5'),
    ('X-ray 50^3 200^2',  'xraysim',    '--size=50*200*5'),
    ('X-ray 50^3 633^2',  'xraysim',    '--size=50*633*5'),

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

