# Bridges  with various parameter setups
# (alias, cmd (relative to the root of bohrium), env-vars)
bohrium = [
    ('bohrium', 'python benchmark/python/{script}.py {args} --bohrium=True', None)
]

# Engines with various parameter setups
# (alias, engine, env-vars)
engines = [
    ('GPU',     'gpu',      None),
]

# Scripts and their arguments
# (alias, script, arguments)
scripts   = [
    ('Gauss f64 1i', 'gauss_fi',     '--size=9000*1 --dtype=float64'),
    ('LU f64 1i',    'lu_fi',        '--size=9000*1 --dtype=float64'),
    ('Gauss f32 1i', 'gauss_fi',     '--size=12000*1 --dtype=float32'),
    ('LU f32 1i',    'lu_fi',        '--size=12000*1 --dtype=float32'),
    ('Gauss f64 100i', 'gauss_fi',     '--size=9000*100 --dtype=float64'),
    ('LU f64 100i',    'lu_fi',        '--size=9000*100 --dtype=float64'),
    ('Gauss f32 100i', 'gauss_fi',     '--size=12000*100 --dtype=float32'),
    ('LU f32 100i',    'lu_fi',        '--size=12000*100 --dtype=float32'),

]

suites = [
    { 'bridges': bohrium
      ,'engines':  engines
      ,'scripts':  scripts},
    ]
