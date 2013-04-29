# Bridges  with various parameter setups
# (alias, cmd (relative to the root of bohrium), env-vars)
bohrium = [
    ('bohrium', 'python benchmark/Python/{script}.py {args} --bohrium=True', None)
]
numpy = [
    ('numpy', 'python benchmark/Python/{script}.py {args} --bohrium=False', None)
]

# Engines with various parameter setups
# (alias, engine, env-vars)
engines = [
    ('GPU',     'gpu',      None),
]

# Scripts and their arguments
# (alias, script, arguments)
scripts   = [
    ('Black Scholes f32 128M',    'black_scholes',  '--size=128000000*50 --dtype=float32'),
    ('Black Scholes f32  64M',    'black_scholes',  '--size=64000000*50 --dtype=float32'),
    ('Black Scholes f32  32M',    'black_scholes',  '--size=32000000*50 --dtype=float32'),
    ('Black Scholes f32  16M',    'black_scholes',  '--size=16000000*50 --dtype=float32'),
    ('Black Scholes f32   8M',    'black_scholes',  '--size=8000000*50 --dtype=float32'),

    ('Black Scholes f64  64M',    'black_scholes',  '--size=64000000*50 --dtype=float64'),
    ('Black Scholes f64  32M',    'black_scholes',  '--size=32000000*50 --dtype=float64'),
    ('Black Scholes f64  16M',    'black_scholes',  '--size=16000000*50 --dtype=float64'),
    ('Black Scholes f64   8M',    'black_scholes',  '--size=8000000*50 --dtype=float64'),
    ('Black Scholes f64   4M',    'black_scholes',  '--size=4000000*50 --dtype=float64'),

    ('SOR f32 16k x 16k',         'sor',            '--size=16000*16000*50 --dtype=float32'),
    ('SOR f32  8k x 16k',         'sor',            '--size=8000*16000*50 --dtype=float32'),
    ('SOR f32  8k x  8k',         'sor',            '--size=8000*8000*50 --dtype=float32'),
    ('SOR f32  4k x  8k',         'sor',            '--size=4000*8000*50 --dtype=float32'),
    ('SOR f32  4k x  4k',         'sor',            '--size=4000*4000*50 --dtype=float32'),

    ('SOR f64  8k x 16k',         'sor',            '--size=8000*16000*50 --dtype=float64'),
    ('SOR f64  8k x  8k',         'sor',            '--size=8000*8000*50 --dtype=float64'),
    ('SOR f64  4k x  8k',         'sor',            '--size=4000*8000*50 --dtype=float64'),
    ('SOR f64  4k x  4k',         'sor',            '--size=4000*4000*50 --dtype=float64'),
    ('SOR f64  2k x  4k',         'sor',            '--size=2000*4000*50 --dtype=float64'),

    ('Shallow Water f32 4k x 8k', 'shallow_water',  '--size=4000*8000*50 --dtype=float32'),
    ('Shallow Water f32 4k x 4k', 'shallow_water',  '--size=4000*4000*50 --dtype=float32'),
    ('Shallow Water f32 2k x 4k', 'shallow_water',  '--size=2000*4000*50 --dtype=float32'),
    ('Shallow Water f32 2k x 2k', 'shallow_water',  '--size=2000*2000*50 --dtype=float32'),
    ('Shallow Water f32 1k x 2k', 'shallow_water',  '--size=1000*2000*50 --dtype=float32'),

    ('Shallow Water f64 4k x 4k', 'shallow_water',  '--size=4000*4000*50 --dtype=float64'),
    ('Shallow Water f64 2k x 4k', 'shallow_water',  '--size=2000*4000*50 --dtype=float64'),
    ('Shallow Water f64 2k x 2k', 'shallow_water',  '--size=2000*2000*50 --dtype=float64'),
    ('Shallow Water f64 1k x 2k', 'shallow_water',  '--size=1000*2000*50 --dtype=float64'),
    ('Shallow Water f64 1k x 1k', 'shallow_water',  '--size=1000*1000*50 --dtype=float64'),

    ('N-body f32 6400', 'nbody',  '--size=6400*100 --dtype=float32'),
    ('N-body f32 3200', 'nbody',  '--size=3200*100 --dtype=float32'),
    ('N-body f32 1600', 'nbody',  '--size=1600*100 --dtype=float32'),
    ('N-body f32  800', 'nbody',  '--size=800*100  --dtype=float32'),
    ('N-body f32  400', 'nbody',  '--size=400*100  --dtype=float32'),

    ('N-body f64 3200', 'nbody',  '--size=3200*100 --dtype=float64'),
    ('N-body f64 1600', 'nbody',  '--size=1600*100 --dtype=float64'),
    ('N-body f64  800', 'nbody',  '--size=800*100  --dtype=float64'),
    ('N-body f64  400', 'nbody',  '--size=400*100  --dtype=float64'),
    ('N-body f64  200', 'nbody',  '--size=200*100  --dtype=float64'),

]

suites = [
    { 'bridges': bohrium
      ,'engines':  engines
      ,'scripts':  scripts},
    { 'bridges': numpy
      ,'scripts':  scripts}
    ]
