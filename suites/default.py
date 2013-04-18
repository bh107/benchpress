# Engines with various parameter setups
# (alias, engine, env-vars)

engines = [
    ('numpy',   None,       None),
    ('naive',   'naive',    None),
    ('simple',  'simple',   None),
    ('gpu',     'gpu',      None),
]

# Scripts and their arguments
# (alias, script, parameters)
scripts   = [
    ('Black Scholes',        'black_scholes.py',  '--size=1000000*10'),
    ('Monte Carlo PI',       'mc.py',             '--size=1000000*100'),
    ('Jacobi Stencil',       'jacobi_stencil.py', '--size=5000*5000*10'),
    ('Shallow Water',        'shallow_water.py',  '--size=1000*1000*10'),
    ('Lattice Boltzmann 2D', 'lattice_boltzmann_D2Q9.py', '--size=100*4000*10'),
]

suite = {
    'scripts':  scripts,
    'engines':  engines
}
