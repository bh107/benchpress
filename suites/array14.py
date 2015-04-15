from default import *

scripts = [
    ('Convolve 2D', 'convolve_2d',  '--size=25'),
    ('Convolve 3D', 'convolve_3d',  '--size=5'),
    ('Wireworld',   'wireworld',    '--size=1000*10'),
    ('27-Point',    'point27',      '--size=400*10'),
    ('Jacobi',      'jacobi',       '--size=1250'),
    ('Jacobi Fixed','jacobi_fixed', '--size=1250*600')
]

numpy = {
    'scripts': scripts,
    'launchers': [python_numpy],
    'bohrium': bh_stack_none
}

bohrium = {
    'scripts': scripts,
    'launchers': [python_bohrium],
    'bohrium': [
        [('default',    'bridge',             None)],
        [('node',       'node',               None)],
        [('topo',       'topological',        None)],
        [
            ('cpu_fused',   'cpu',  {"BH_VE_CPU_JIT_DUMPSRC": "1", "BH_VE_CPU_JIT_FUSION": "1"}),
            ('cpu_sij',     'cpu',  {"BH_VE_CPU_JIT_DUMPSRC": "1", "BH_VE_CPU_JIT_FUSION": "0"}),
        ]
    ],
}

suites = [
    bohrium,
    numpy
]

