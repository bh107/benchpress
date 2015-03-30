from default import *

scripts   = [
    ('Black Scholes',        'black_scholes',  '--size=1000000*10'),
    ('Jacobi Stencil',       'jacobi_stencil', '--size=20000*1000*10'),
    ('KNN',                  'knn',            '--size=2000000*10*3'),
    ('Monte Carlo PI',       'mc',              '--size=1000000*100'),
    ('NBody',                'nbody',           '--size=300*300'),
    ('Shallow Water',        'shallow_water',   '--size=1000*1000*10'),
]

python = {
    'bridges':  [('python-numpy', 'python benchmark/python/{script}.py {args} --bohrium=False', None)],
    'scripts':  scripts,
}

bohrium_taskset = {
    'bridges':  [
        ('bh-numpy', 'python benchmark/python/{script}.py {args} --bohrium=True', None),
    ],
    'managers': [
        ('node',  'node', '',  None),
    ],
    'engines':   [
        ('naive',    'cpu',     {'BH_CORE_VCACHE_SIZE': '0', 'BH_VE_CPU_TRAVERSAL': 'naive'}),
        ('naive+vc', 'cpu',     {'BH_CORE_VCACHE_SIZE': '10', 'BH_VE_CPU_TRAVERSAL': 'naive'}),
        ('tiling',   'tiling',  {'BH_CORE_VCACHE_SIZE': '0'}),
        ('tiling+vc','tiling',  {'BH_CORE_VCACHE_SIZE': '10'}),
        ('fl',       'cpu',     {'BH_CORE_VCACHE_SIZE' : '0', 'BH_VE_CPU_TRAVERSAL': 'fruit_loops'}),
        ('fl+vc',    'cpu',     {'BH_CORE_VCACHE_SIZE' : '10', 'BH_VE_CPU_TRAVERSAL': 'fruit_loops'}),
    ],
    'scripts':   scripts
}

bohrium = {
    'bridges':  [('bh-numpy-notaskset', 'python benchmark/python/{script}.py {args} --bohrium=True', None)],
    'managers': [
        ('node',  'node', '',  None),
    ],
    'engines': [
        ('mcore',       'mcore',    {'BH_CORE_VCACHE_SIZE': '0'}),
        ('mcore+vc',    'mcore',    {'BH_CORE_VCACHE_SIZE': '10'}),
        ('dynamite',    'dynamite', {'BH_CORE_VCACHE_SIZE': '0'}),
        ('dynamite+vc', 'dynamite', {'BH_CORE_VCACHE_SIZE': '10'}),
    ],
    'scripts':  scripts
}

suites = [
    python,
    bohrium,
    bohrium_taskset
]

