from default import scripts, engines

engines = [
    ('numpy',   None,       None),
    ('naive',   'naive',    None),
    ('score',   'score',    None),
    ('simple',  'simple',   None),
    ('tile',    'tile',     None),
    ('mcore',   'mcore',    None),
    ('jitbatchcacheon',  'jit',      {"CPHVB_JIT_DIRECTEXECUTE":"False","CPHVB_JIT_CACHE_ENABLED":"True"}),
    ('jitbatchcacheoff', 'jit',      {"CPHVB_JIT_DIRECTEXECUTE":"False","CPHVB_JIT_CACHE_ENABLED":"False"}),
    ('jitexprcacheon',   'jit',      {"CPHVB_JIT_DIRECTEXECUTE":"True","CPHVB_JIT_CACHE_ENABLED":"True"}),
    ('jitexprcacheoff',  'jit',      {"CPHVB_JIT_DIRECTEXECUTE":"True","CPHVB_JIT_CACHE_ENABLED":"False"}),    
    ('gpu',     'gpu',      None),
]

# Scripts and their arguments
# (alias, script, parameters)
scripts   = [
    #('Cache Synth',     'cache.py',     '--size=10500000*10*1'),
    #('Lattice Boltzmann 2D', 'lbm.2d.py', '--size=15*200000*2'),
    #('Lattice Boltzmann 3D', 'lbm.3d.py', '--size=100*100*100*2'),
    # This one seems to be broken
    #('LU Factorization', 'lu.py', '--size=5000*10'),


    #~ # tests
    #~ ('Black Scholes',   'bscholes.py',  '--size=2000000*4'),
    #~ ('Jacobi Iterative',            'jacobi.iterative.py',          '--size=7000*7000*4'),
    #~ ('Jacobi Iterative - PS',       'jacobi.iterative.ps.py',       '--size=7000*7000*4'), 
    #~ ('Jacobi Iterative - No Views', 'jacobi.iterative.noviews.py',  '--size=7000*7000*4'),
    #~ ('Jacobi Iterative - Reduce',   'jacobi.iterative.reduc.py',    '--size=7000*7000*4'),
    #~ ('Jacobi Iterative - Reduce Naive',   'jacobi.iterative.reduce.oneline.py',    '--size=7000*7000*4'),
    #~ ('kNN',             'knn.py',       '--size=10000*120'),    
    #~ ('kNN - Naive',     'knn.naive.py', '--size=10000*120*10'),
    #~ ('Monte Carlo PI - RIL',    'mc.py',        '--size=10*1000000*10'),
    #~ ('Monte Carlo PI - 2xN',    'mc.2byN.py',   '--size=10*1000000*10'),
    #~ ('Monte Carlo PI - Nx2',    'mc.Nby2.py',   '--size=10*1000000*10'),
    #~ ('N-Body',  'nbody.py', '--size=2500*10'),
    #~ ('Stencil - 1D 4way',       'stencil.simplest.py',  '--size=100000000*1'),
    #~ ('Stencil - 2D',            'stencil.2d.py',        '--size=10000*1000*10'),
    #~ ('Shallow Water',           'swater.py',            '--size=2200*1'),
    #~ 
    #~ #fun
    #~ ('Monte Carlo PI - RIL',    'mc.py',        '--size=10*1000000*10'),
    #~ ('kNN',             'knn.py',       '--size=10000*120'),    
    #~ ('N-Body',  'nbody.py', '--size=2500*10'),
    #~ ('Shallow Water',           'swater.py',            '--size=2200*1'),
    #~ ('Black Scholes',   'bscholes.py',  '--size=2000000*4'),
    #~ ('Jacobi Iterative - Reduce',   'jacobi.iterative.reduc.py',    '--size=7000*7000*4'),
    #~ ('Jacobi Iterative - Reduce Naive',   'jacobi.iterative.reduce.oneline.py',    '--size=7000*7000*4'),

    #test
    ('Black Scholes',   'bscholes.py',  '--size=100*4'),
    ('Jacobi Iterative',            'jacobi.iterative.py',          '--size=100*100*4'),
    ('Jacobi Iterative - PS',       'jacobi.iterative.ps.py',       '--size=100*100*4'), 
    ('Jacobi Iterative - No Views', 'jacobi.iterative.noviews.py',  '--size=100*100*4'),
    ('Jacobi Iterative - Reduce',   'jacobi.iterative.reduc.py',    '--size=100*100*4'),
    ('Jacobi Iterative - Reduce Naive',   'jacobi.iterative.reduce.oneline.py',    '--size=100*100*4'),
    ('kNN',             'knn.py',       '--size=100*120'),    
    ('kNN - Naive',     'knn.naive.py', '--size=100*120*10'),
    ('Monte Carlo PI - RIL',    'mc.py',        '--size=10*100*10'),
    ('Monte Carlo PI - 2xN',    'mc.2byN.py',   '--size=10*100*10'),
    ('Monte Carlo PI - Nx2',    'mc.Nby2.py',   '--size=10*100*10'),
    ('N-Body',  'nbody.py', '--size=2500*10'),
    ('Stencil - 1D 4way',       'stencil.simplest.py',  '--size=100*1'),
    ('Stencil - 2D',            'stencil.2d.py',        '--size=100*100*10'),
    ('Shallow Water',           'swater.py',            '--size=100*1')
    ('Shallow Water with flush()',           'swater.flushing.py',            '--size=100*1')

]

suite = {
    'scripts':  scripts,
    'engines':  [engines[6]] + [engines[8]]
    #'engines':  engines[0:4] + engines[6:10]
}
