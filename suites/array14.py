from default import *

scripts = [
    ('Convolve',    'convolve',     '--size=25'),
    ('Wireworld',   'wireworld',    '--size=1000*10'),
    ('27-Point',    'point27',      '--size=400*10'),
]

managers= [('node', 'node', '', None)]

numpy = {
    'bridges':  [('NumPy', 'python benchmark/Python/{script}.py {args} --bohrium=False', None)],
    'scripts':  scripts,
}

bohrium = {
    'bridges':  [('Bohrium',    'python benchmark/Python/{script}.py {args} --bohrium=True', None)],
    'managers': [('node',       'node', '',  None)],
    'engines':  [
        ('cpu_fused',   'cpu',  {"BH_VE_CPU_JIT_DUMPSRC": "1", "BH_VE_CPU_JIT_FUSION": "1"}),
        ('cpu_sij',     'cpu',  {"BH_VE_CPU_JIT_DUMPSRC": "1", "BH_VE_CPU_JIT_FUSION": "0"}),
    ],
    'scripts':  scripts
}

suites = [
    bohrium,
    numpy
]

