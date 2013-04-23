# Bridges  with various parameter setups
# (alias, cmd (relative to the root of bohrium), env-vars)
bridges = [
    ('numpy', 'python benchmark/Python/{script}.py {args} --bohrium=True', None),
    ('CIL', 'mono benchmark/CIL/Csharp/{script}/bin/Release/{script}.exe {args}', None),
]


# Engines with various parameter setups
# (alias, engine, env-vars)
engines = [
    ('naive',   'naive',    None),
    ('simple',  'simple',   None),
    ('gpu',     'gpu',      None),
]

# Scripts and their arguments
# (alias, script, arguments)
scripts   = [
    ('Black Scholes',        'black_scholes',  '--size=1000000*10'),
    ('Monte Carlo PI',       'mc',             '--size=1000000*100'),
    ('Jacobi Stencil',       'jacobi_stencil', '--size=5000*5000*10'),
    ('Shallow Water',        'shallow_water',  '--size=1000*1000*10'),
    ('Lattice Boltzmann 2D', 'lattice_boltzmann_D2Q9', '--size=100*4000*10'),
]

suite = {
    'bridges':  bridges,
    'engines':  engines,
    'scripts':  scripts
}
