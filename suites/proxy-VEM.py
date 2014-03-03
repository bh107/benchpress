managers = [('proxy', 'proxy', '{bridge}', None)]

engines = [('cpu',  'cpu',   None)]

python_script = [\
#    		 ('N-body 5k',        'nbody',        '--size=150*10'),
#           	 ('N-body 20k',        'nbody',        '--size=200*10'),
                 ('Shallow Water 10k', 'shallow_water','--size=10000*10000*10'),
#                 ('Shallow Water 25k', 'shallow_water','--size=250*250*10'),
#                 ('Black Scholes 10m', 'black_scholes','--size=10000*10'),
#                 ('Black Scholes 100m','black_scholes','--size=10000000*10')
]

python = {
    'bridges': [('numpy', 'python benchmark/Python/{script}.py {args} --bohrium=True', None)],
    'managers': managers,
    'engines': engines,
    'scripts': python_script
}

suites = [python]

