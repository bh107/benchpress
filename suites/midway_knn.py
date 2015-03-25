from default import *

scholes = [
    ('Black Scholes',        'black_scholes',   '--size=2500000*5'),
    ('Black Scholes',        'black_scholes',   '--size=5000000*5'),
    ('Black Scholes',        'black_scholes',   '--size=1000000*5'),
    ('Black Scholes',        'black_scholes',   '--size=2000000*5'),
    ('Black Scholes',        'black_scholes',   '--size=4000000*5'),
    ('Black Scholes',        'black_scholes',   '--size=8000000*5'),
]

jacobi = [
    ('Jacobi Stencil',       'jacobi_stencil', '--size=313*4000*10'),
    ('Jacobi Stencil',       'jacobi_stencil', '--size=625*4000*10'),
    ('Jacobi Stencil',       'jacobi_stencil', '--size=1250*4000*10'),
    ('Jacobi Stencil',       'jacobi_stencil', '--size=2500*4000*10'),
    ('Jacobi Stencil',       'jacobi_stencil', '--size=5000*4000*10'),
    ('Jacobi Stencil',       'jacobi_stencil', '--size=10000*4000*10'),
]

knn = [
    ('KNN', 'knn', '--size=62500*10*3'),
    ('KNN', 'knn', '--size=125000*10*3'),
    ('KNN', 'knn', '--size=250000*10*3'),
    ('KNN', 'knn', '--size=500000*10*3'),
    ('KNN', 'knn', '--size=1000000*10*3'),
    ('KNN', 'knn', '--size=2000000*10*3'),
]

mc = [
    ('Monte Carlo PI', 'mc', '--size=625000*10'),
    ('Monte Carlo PI', 'mc', '--size=1250000*10'),
    ('Monte Carlo PI', 'mc', '--size=2500000*10'),
    ('Monte Carlo PI', 'mc', '--size=5000000*10'),
    ('Monte Carlo PI', 'mc', '--size=10000000*10'),
    ('Monte Carlo PI', 'mc', '--size=20000000*10'),
]

nbody = [
    ('NBody', 'nbody', '--size=125*10'),
    ('NBody', 'nbody', '--size=250*10'),
    ('NBody', 'nbody', '--size=500*10'),
    ('NBody', 'nbody', '--size=1000*10'),
    ('NBody', 'nbody', '--size=2000*10'),
    ('NBody', 'nbody', '--size=4000*5')
]

shallow = [
    ('Shallow Water',        'shallow_water',   '--size=94*94*5'),
    ('Shallow Water',        'shallow_water',   '--size=188*188*5'),
    ('Shallow Water',        'shallow_water',   '--size=375*375*5'),
    ('Shallow Water',        'shallow_water',   '--size=750*750*5'),
    ('Shallow Water',        'shallow_water',   '--size=1500*1500*5'),
    ('Shallow Water',        'shallow_water',   '--size=3000*3000*5'),
]

scripts = []
scripts += knn

managers= [('node', 'node', '', None)]

numpy = {
    'bridges':  [('NumPy/Native', 'python benchmark/python/{script}.py {args} --bohrium=False', None)],
    'scripts':  scripts,
}

bohrium = {
    'bridges':  [('NumPy/Bohrium', 'python benchmark/python/{script}.py {args} --bohrium=True', None)],
    'managers': [('node',  'node', '',  None) ],
    'engines':  [
        ('cpu',     'cpu',      {'BH_CORE_VCACHE_SIZE':  '0', 'BH_VE_CPU_TRAVERSAL': 'naive'}),
        ('cpu_vc',  'cpu',      {'BH_CORE_VCACHE_SIZE':  '30', 'BH_VE_CPU_TRAVERSAL': 'naive'}),
        ('tiling',  'tiling',   {'BH_CORE_VCACHE_SIZE':  '30', 'BH_VE_CPU_TRAVERSAL': 'naive'}),
        ('mcore',   'mcore',    {'BH_CORE_VCACHE_SIZE':  '30', 'BH_VE_CPU_TRAVERSAL': 'naive'}),
    ],
    'scripts':  scripts
}

suites = [
    numpy,
    bohrium
]

