# Bridges  with various parameter setups
# (alias, cmd (relative to the root of bohrium), env-vars)
bohrium = [
    ('bohrium', 'python benchmark/python/{script}.py {args} --bohrium=True', None)
]
numpy = [
    ('numpy', 'python benchmark/python/{script}.py {args} --bohrium=False', None)
]

# Engines with various parameter setups
# (alias, engine, env-vars)
engines = [
    ('GPU',     'gpu',      None),
]

# Scripts and their arguments
# (alias, script, arguments)
scripts   = [
    ('SOR f32  2k x  8k',         'sor',            '--size=2046*8190*100 --dtype=float32'),
    ('SOR f32  4k x  4k',         'sor',            '--size=4094*4094*100 --dtype=float32'),
    ('SOR f32  8k x  4k',         'sor',            '--size=8190*2046*100 --dtype=float32'),

    ('SOR f64  2k x  8k',         'sor',            '--size=2046*8190*100 --dtype=float64'),
    ('SOR f64  4k x  4k',         'sor',            '--size=4094*4094*100 --dtype=float64'),
    ('SOR f64  8k x  4k',         'sor',            '--size=8190*2046*100 --dtype=float64'),

    ('Jacobi f32  2k x  8k',      'jacobi_stencil', '--size=2046*8190*100 --dtype=float32'),
    ('Jacobi f32  4k x  4k',      'jacobi_stencil', '--size=4094*4094*100 --dtype=float32'),
    ('Jacobi f32  8k x  2k',      'jacobi_stencil', '--size=8190*2046*100 --dtype=float32'),

    ('Jacobi f64  2k x  8k',      'jacobi_stencil', '--size=2046*8190*100 --dtype=float64'),
    ('Jacobi f64  4k x  4k',      'jacobi_stencil', '--size=4094*4094*100 --dtype=float64'),
    ('Jacobi f64  8k x  2k',      'jacobi_stencil', '--size=8190*2046*100 --dtype=float64'),

    ('Shallow Water f32 2k x 8k', 'shallow_water',  '--size=2048*8192*100 --dtype=float32'),
    ('Shallow Water f32 4k x 4k', 'shallow_water',  '--size=4096*4096*100 --dtype=float32'),
    ('Shallow Water f32 8k x 2k', 'shallow_water',  '--size=8192*2048*100 --dtype=float32'),

    ('Shallow Water f64 2k x 8k', 'shallow_water',  '--size=2048*8192*100 --dtype=float64'),
    ('Shallow Water f64 4k x 4k', 'shallow_water',  '--size=4096*4096*100 --dtype=float64'),
    ('Shallow Water f64 8k x 2k', 'shallow_water',  '--size=8192*2048*100 --dtype=float64'),


]

suites = [
    { 'bridges': bohrium
      ,'engines':  engines
      ,'scripts':  scripts}
    ]
