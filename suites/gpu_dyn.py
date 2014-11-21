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
    ('1D',    'ndstencil', '--size=24*8000*1 --dtype=float64'),
    ('2D',    'ndstencil', '--size=24*4000*2 --dtype=float64'),
    ('3D',    'ndstencil', '--size=24*2000*3 --dtype=float64'),
    ('4D',    'ndstencil', '--size=24*1000*4 --dtype=float64'),
    ('Gauss', 'gauss',     '--size=9000 --dtype=float64'),
    ('LU',    'lu',        '--size=9000 --dtype=float64'),
    ('1D',    'ndstencil', '--size=25*8000*1 --dtype=float32'),
    ('2D',    'ndstencil', '--size=25*4000*2 --dtype=float32'),
    ('3D',    'ndstencil', '--size=25*2000*3 --dtype=float32'),
    ('4D',    'ndstencil', '--size=25*1000*4 --dtype=float32'),
    ('Gauss', 'gauss',     '--size=12000 --dtype=float32'),
    ('LU',    'lu',        '--size=12000 --dtype=float32'),

]

suites = [
    { 'bridges': bohrium
      ,'engines':  engines
      ,'scripts':  scripts},
    ]
