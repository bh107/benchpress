from default import *

# Bridges  with various parameter setups
# (alias, cmd (relative to the root of bohrium), env-vars)
bridges = [
    ('bohrium-numpy', 'python benchmark/Python/{script}.py {args} --bohrium=True', None),
]

# Managers above the node-vem with various parameter setups.
# NB: the node-vem is hardcoded, the managers here will have the
#     node-vem as child unless it is the node-vem itself
# (alias, manager, cmd (relative to the root of bohrium), env-vars)
managers = [
    ('node',  'node', '',  None),
]

# Scripts and their arguments
# (alias, script, arguments)
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

# Engines with various parameter setups
# (alias, engine, env-vars)
engines = [
    ('naive',       'cpy', {'BH_CORE_VCACHE_SIZE': '0',
                            'BH_VE_CPU_TRAVERSAL': 'naive'}),
    ('naive+vc',    'cpu', {'BH_CORE_VCACHE_SIZE': '10',
                            'BH_VE_CPU_TRAVERSAL': 'naive'}),
    ('fl',          'cpu', {'BH_CORE_VCACHE_SIZE' : '0',
                            'BH_VE_CPUT_TRAVERSAL': 'fruit_loops'}),
    ('fl+vc',       'cpu', {'BH_CORE_VCACHE_SIZE' : '10',
                            'BH_VE_CPUT_TRAVERSAL': 'fruit_loops'}),
]

# A suite example
# Note that 'engines' and 'managers' may be undefined, in which case they are ignored
suite = {
    'bridges':   bridges,
    'managers':  managers,
    'engines':   engines,
    'scripts':   scripts,
}

py_only = {
    'bridges':  [('python-numpy', 'python benchmark/Python/{script}.py {args} --bohrium=False', None)],
    'scripts':  scripts,
}

suites = [py_only, suite]

