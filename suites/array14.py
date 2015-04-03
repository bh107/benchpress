from default import *

scripts = [
    ('Convolve 2D', 'convolve_2d',  '--size=25'),
    ('Convolve 3D', 'convolve_3d',  '--size=5'),
    ('Wireworld',   'wireworld',    '--size=1000*10'),
    ('27-Point',    'point27',      '--size=400*10'),
    ('Jacobi',      'jacobi',       '--size=1250'),
    ('Jacobi Fixed','jacobi_fixed', '--size=1250*600')
]

managers= [('node', 'node', '', None)]

numpy = {
    'bridges':  [python_numpy],
    'scripts':  scripts,
}

bohrium = {
    'bridges':  [python_bohrium],
    'managers': [('node', 'node', '', None)],
    'engines':  [
        #('cpu_fused',   'cpu',  {"BH_VE_CPU_JIT_DUMPSRC": "1", "BH_VE_CPU_JIT_FUSION": "1"}),
        ('cpu_sij', 'cpu', {"BH_VE_CPU_JIT_DUMPSRC": "1", "BH_VE_CPU_JIT_FUSION": "0"}),
    ],
    'scripts':  scripts
}

suites = [
    bohrium,
    numpy
]

