from default import *

scripts   = [
    ('Black Scholes',        'black_scholes',  '--size=1000000*10'),
    ('Jacobi Stencil',       'jacobi_stencil', '--size=20000*1000*10'),
    ('KNN',                  'knn',            '--size=2000000*10*3'),
#    ('Lattice Boltzmann 2D', 'lattice_boltzmann_D2Q9',  '--size=1000*1000*10'),
#    ('Lattice Boltzmann 3D', 'lbm.3d',          '--size=100*100*100*10'),
    ('Monte Carlo PI',       'mc',              '--size=1000000*100'),
#    ('MXMUL',                'mxmul',           '--size=1000'),
    ('NBody',                'nbody',           '--size=300*300'),
    ('Shallow Water',        'shallow_water',   '--size=1000*1000*10'),
#    ('SoR',                  'sor',             '--size=5000*5000*10'),
]

python = {
    'bridges':  [('python-numpy', 'python benchmark/Python/{script}.py {args} --bohrium=False', None)],
    'scripts':  scripts,
}

score = {
    'bridges':  [
        ('bohrium-numpy', 'taskset -c 1 python benchmark/Python/{script}.py {args} --bohrium=True', None),
    ],
    'managers': [
        ('node',  'node', '',  None),
    ],
    'engines':   [
        ('naive',    'cpu', {'BH_CORE_VCACHE_SIZE': '0', 'BH_VE_CPU_TRAVERSAL': 'naive'}),
        ('naive+vc', 'cpu', {'BH_CORE_VCACHE_SIZE': '10', 'BH_VE_CPU_TRAVERSAL': 'naive'}),
        ('fl',       'cpu', {'BH_CORE_VCACHE_SIZE' : '0', 'BH_VE_CPUT_TRAVERSAL': 'fruit_loops'}),
        ('fl+vc',    'cpu', {'BH_CORE_VCACHE_SIZE' : '10', 'BH_VE_CPUT_TRAVERSAL': 'fruit_loops'}),
        ('tiling',   'tiling',   {'BH_CORE_VCACHE_SIZE': '0'}),
        ('tiling+vc','tiling',   {'BH_CORE_VCACHE_SIZE': '10'}),   
    ],
    'scripts':   scripts
}

mcore = {
    'bridges':  [('bohrium-numpy-mcore', 'python benchmark/Python/{script}.py {args} --bohrium=True', None)],
    'managers': [
        ('node',  'node', '',  None),
    ],
    'engines': [
        ('mcore',       'mcore',    {'BH_CORE_VCACHE_SIZE': '0'}),
        ('mcore+vc',    'mcore',    {'BH_CORE_VCACHE_SIZE': '10'})
    ],
    'scripts':  scripts
}

suites = [
    python,
    mcore,
    score
]

