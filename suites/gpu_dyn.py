# Bridges  with various parameter setups
# (alias, cmd (relative to the root of bohrium), env-vars)
bohrium = [
    ('bohrium', 'python benchmark/Python/{script}.py {args} --bohrium=True', None)
]

# Engines with various parameter setups
# (alias, engine, env-vars)
engines = [
    ('GPU',     'gpu',      None),
]

# Scripts and their arguments
# (alias, script, arguments)
scripts   = [
    ('Gauss', 'gauss',     '--size=8000 --dtype=float64'),
    ('LU',    'lu',        '--size=8000 --dtype=float64'),
    ('1D',    'ndstencil', '--size=24*1000*1 --dtype=float64'),
    ('2D',    'ndstencil', '--size=24*1000*2 --dtype=float64'),
    ('3D',    'ndstencil', '--size=24*1000*3 --dtype=float64'),
    ('4D',    'ndstencil', '--size=24*1000*4 --dtype=float64'),

]

suites = [
    { 'bridges': bohrium
      ,'engines':  engines
      ,'scripts':  scripts},
    ]
