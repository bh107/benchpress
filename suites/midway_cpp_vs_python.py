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
    ('Jacobi Stencil',       'jacobi_stencil', '--size=313*4000*10'),
    ('Jacobi Stencil',       'jacobi_stencil', '--size=625*4000*10'),
    ('Jacobi Stencil',       'jacobi_stencil', '--size=1250*4000*10'),
    ('Jacobi Stencil',       'jacobi_stencil', '--size=2500*4000*10'),
    ('Jacobi Stencil',       'jacobi_stencil', '--size=5000*4000*10'),
    ('Jacobi Stencil',       'jacobi_stencil', '--size=10000*4000*10'),
]

mc = [
    ('Monte Carlo PI', 'mc', '--size=625000*10'),
    ('Monte Carlo PI', 'mc', '--size=1250000*10'),
    ('Monte Carlo PI', 'mc', '--size=2500000*10'),
    ('Monte Carlo PI', 'mc', '--size=5000000*10'),
    ('Monte Carlo PI', 'mc', '--size=10000000*10'),
    ('Monte Carlo PI', 'mc', '--size=20000000*10'),
]

cpp_mc = [
    ('Monte Carlo PI', 'monte_carlo_pi', '--size=625000*10'),
    ('Monte Carlo PI', 'monte_carlo_pi', '--size=1250000*10'),
    ('Monte Carlo PI', 'monte_carlo_pi', '--size=2500000*10'),
    ('Monte Carlo PI', 'monte_carlo_pi', '--size=5000000*10'),
    ('Monte Carlo PI', 'monte_carlo_pi', '--size=10000000*10'),
    ('Monte Carlo PI', 'monte_carlo_pi', '--size=20000000*10'),
]

engines = [
    ('cpu',     'cpu',      {'BH_CORE_VCACHE_SIZE':  '0', 'BH_VE_CPU_TRAVERSAL': 'naive'}),
    ('cpu_vc',  'cpu',      {'BH_CORE_VCACHE_SIZE': '30', 'BH_VE_CPU_TRAVERSAL': 'naive'}),
    ('floop',   'cpu',      {'BH_CORE_VCACHE_SIZE': '30', 'BH_VE_CPU_TRAVERSAL': 'fruit_loops'}),
    ('tiling',  'tiling',   {'BH_CORE_VCACHE_SIZE': '30'}),
    ('dynamite','dynamite', {'BH_CORE_VCACHE_SIZE': '30'}),
    ('mcore',   'mcore',    {'BH_CORE_VCACHE_SIZE': '30'}),
]
managers= [('node', 'node', '', None)]

cpp = {
    'bridges': [('Bh/cpp', './benchmark/cpp/bin/{script} {args}', None)],
    'managers': managers,
    'engines':  engines,
    'scripts':  []+scholes+jacobi+cpp_mc
}

python = {
    'bridges':  [('NumPy/Bohrium', 'python benchmark/python/{script}.py {args} --bohrium=True', None)],
    'managers': managers,
    'engines':  engines,
    'scripts':  []+scholes+jacobi+mc
}

suites = [
    cpp,
    python
]

