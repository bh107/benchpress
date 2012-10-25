# Engines with various parameter setups
# (alias, runs, engine, env-vars)

engines = [
    ('numpy',   None,       None),
    ('simple',  'simple',   None),
    ('score',   'score',    None),
    ('mcore',   'mcore',    None),
    ('gpu',     'gpu',    None),
    ('jit',     'jit',    None),
]

# Scripts and their arguments
# (alias, script, parameters)
scripts   = [
    ('Black Scholes',   'bscholes.py',  '--size=2000000*4'),
    ('Cache Synth',     'cache.py',     '--size=10500000*10*1'),

    ('Jacobi Iterative',            'jacobi.iterative.py',          '--size=7000*7000*4'),
    # This one seems to be broken.
    #('Jacobi Iterative - No Views', 'jacobi.iterative.noviews.py',  '--size=7000*7000*4'),
    ('Jacobi Iterative - Reduce',   'jacobi.iterative.reduc.py',    '--size=7000*7000*4'),

    ('kNN',             'knn.py',       '--size=10000*120'),
    # This is fall back to the bridge
    #('kNN - Naive',     'knn.naive.py', '--size=10000*120*10'),

    ('Lattice Boltzmann 2D', 'lbm.2d.py', '--size=15*200000*2'),
    ('Lattice Boltzmann 3D', 'lbm.3d.py', '--size=100*100*100*2'),

    # This one seems to be broken
    #('LU Factorization', 'lu.py', '--size=5000*10'),   

    ('Monte Carlo PI - RIL',    'mc.py',        '--size=10*1000000*10'),
    ('Monte Carlo PI - 2xN',    'mc.2byN.py',   '--size=10*1000000*10'),
    ('Monte Carlo PI - Nx2',    'mc.Nby2.py',   '--size=10*1000000*10'),

    # This one seems to be broken
    #('N-Body',  'nbody.py', '--size=2500*10'),

    ('Stencil - 1D 4way',       'stencil.simplest.py',  '--size=100000000*1'),
    ('Stencil - 2D',            'stencil.2d.py',        '--size=10000*1000*10'),

    ('Shallow Water',           'swater.py',            '--size=2200*1'),

]

suite = {
    'scripts':  scripts,
    'engine':   engines
}
