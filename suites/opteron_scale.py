from default import *

scripts = [
    ('Jacobi Stencil',  'jacobi_stencil',   '--size=8000*8000*10'),
    ('Black Scholes',   'black_scholes',    '--size=4000000*5'),
    ('KNN',             'knn',              '--size=15000000*10*3'),
    ('Monte Carlo PI',  'mc',               '--size=10000000*10'),
    ('NBody',           'nbody',            '--size=4000*5'),
    ('Shallow Water',   'shallow_water',    '--size=1500*1500*5'),
]

managers= [('node', 'node', '', None)]

numpy = {
    'bridges':  [('NumPy/Native', 'python benchmark/python/{script}.py {args} --bohrium=False', None)],
    'scripts':  scripts,
}

bohrium = {
    'bridges':  [('NumPy/Bohrium', 'python benchmark/python/{script}.py {args} --bohrium=True', None)],
    'managers': [('node',  'node', '',  None) ],
    'engines':  [
        ('score',  'score',{'BH_CORE_VCACHE_SIZE': '10', 'BH_VE_CPU_TRAVERSAL': 'naive'}),
        ('omp1',    'cpu', {'BH_CORE_VCACHE_SIZE': '10', 'OMP_NUM_THREADS': '1'}),
        ('omp2',    'cpu', {'BH_CORE_VCACHE_SIZE': '10', 'OMP_NUM_THREADS': '2'}),
        ('omp4',    'cpu', {'BH_CORE_VCACHE_SIZE': '10', 'OMP_NUM_THREADS': '4'}),
        ('omp8',    'cpu', {'BH_CORE_VCACHE_SIZE': '10', 'OMP_NUM_THREADS': '8'}),
        ('omp16',   'cpu', {'BH_CORE_VCACHE_SIZE': '10', 'OMP_NUM_THREADS': '16'}),
        ('omp32',   'cpu', {'BH_CORE_VCACHE_SIZE': '10', 'OMP_NUM_THREADS': '32'}),
    ],
    'scripts':  scripts
}

suites = [
    bohrium,
    numpy
]

