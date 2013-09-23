from default import *

scripts = [
    ('Black Scholes',   'black_scholes',    '--size=4000000*5'),
    ('Jacobi Stencil',  'jacobi_stencil',   '--size=5000*4000*10'),
    ('KNN',             'knn',              '--size=2000000*10*3'),
    ('Monte Carlo PI',  'mc',               '--size=10000000*10'),
    ('NBody',           'nbody',            '--size=4000*5'),
    ('Shallow Water',   'shallow_water',    '--size=1500*1500*5'),
]

scripts = []

managers= [('node', 'node', '', None)]

numpy = {
    'bridges':  [('NumPy/Native', 'python benchmark/Python/{script}.py {args} --bohrium=False', None)],
    'scripts':  scripts,
}

bohrium = {
    'bridges':  [('NumPy/Bohrium', 'python benchmark/Python/{script}.py {args} --bohrium=True', None)],
    'managers': [('node',  'node', '',  None) ],
    'engines':  [
        ('static',  'cpu',      {'BH_CORE_VCACHE_SIZE': '10', 'BH_VE_CPU_TRAVERSAL': 'naive'}),
        ('omp1',    'dynamite', {'BH_CORE_VCACHE_SIZE': '10', 'OMP_NUM_THREADS': '1'}),
        ('omp2',    'dynamite', {'BH_CORE_VCACHE_SIZE': '10', 'OMP_NUM_THREADS': '2'}),
        ('omp4',    'dynamite', {'BH_CORE_VCACHE_SIZE': '10', 'OMP_NUM_THREADS': '4'}),
        ('omp8',    'dynamite', {'BH_CORE_VCACHE_SIZE': '10', 'OMP_NUM_THREADS': '8'}),
        ('omp16',   'dynamite', {'BH_CORE_VCACHE_SIZE': '10', 'OMP_NUM_THREADS': '16'}),
        ('omp32',   'dynamite', {'BH_CORE_VCACHE_SIZE': '10', 'OMP_NUM_THREADS': '32'}),
    ],
    'scripts':  scripts
}

suites = [
    bohrium,
    numpy
]

