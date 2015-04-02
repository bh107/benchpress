from default import *

scholes = [
    ('Black Scholes',        'black_scholes',   '--size=125000*10'),
    ('Black Scholes',        'black_scholes',   '--size=250000*10'),
    ('Black Scholes',        'black_scholes',   '--size=500000*10'),
    ('Black Scholes',        'black_scholes',   '--size=1000000*10'),
    ('Black Scholes',        'black_scholes',   '--size=2000000*10'),
    ('Black Scholes',        'black_scholes',   '--size=4000000*10'),
]

jacobi = [
    ('Jacobi Stencil',       'jacobi_stencil', '--size=250*1000*10'),
    ('Jacobi Stencil',       'jacobi_stencil', '--size=500*1000*10'),
    ('Jacobi Stencil',       'jacobi_stencil', '--size=1000*1000*10'),
    ('Jacobi Stencil',       'jacobi_stencil', '--size=2000*1000*10'),
    ('Jacobi Stencil',       'jacobi_stencil', '--size=4000*1000*10'),
    ('Jacobi Stencil',       'jacobi_stencil', '--size=8000*1000*10'),
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
    ('Monte Carlo PI', 'mc', '--size=62500*10'),
    ('Monte Carlo PI', 'mc', '--size=125000*10'),
    ('Monte Carlo PI', 'mc', '--size=2500000*10'),
    ('Monte Carlo PI', 'mc', '--size=5000000*10'),
    ('Monte Carlo PI', 'mc', '--size=10000000*10'),
    ('Monte Carlo PI', 'mc', '--size=20000000*10'),
]

nbody = [
    ('NBody', 'nbody', '--size=50*10'),
    ('NBody', 'nbody', '--size=100*10'),
    ('NBody', 'nbody', '--size=200*10'),
    ('NBody', 'nbody', '--size=400*10'),
    ('NBody', 'nbody', '--size=800*10'),
    ('NBody', 'nbody', '--size=1600*10')
]

shallow = [
    ('Shallow Water',        'shallow_water',   '--size=50*50*10'),
    ('Shallow Water',        'shallow_water',   '--size=100*100*10'),
    ('Shallow Water',        'shallow_water',   '--size=200*200*10'),
    ('Shallow Water',        'shallow_water',   '--size=400*400*10'),
    ('Shallow Water',        'shallow_water',   '--size=800*800*10'),
    ('Shallow Water',        'shallow_water',   '--size=1600*1600*10'),
]

scripts = []
scripts += shallow

scripts = scholes + jacobi + knn + mc + nbody + shallow

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
        ('cpu_vc',  'cpu',      {'BH_CORE_VCACHE_SIZE':  '10', 'BH_VE_CPU_TRAVERSAL': 'naive'}),
        ('tiling',  'tiling',   {'BH_CORE_VCACHE_SIZE':  '10', 'BH_VE_CPU_TRAVERSAL': 'naive'}),
        ('mcore',   'mcore',    {'BH_CORE_VCACHE_SIZE':  '10', 'BH_VE_CPU_TRAVERSAL': 'naive'}),
    ],
    'scripts':  scripts
}

suites = [
    numpy,
    bohrium
]

