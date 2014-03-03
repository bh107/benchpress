
engines = [('cpu',  'cpu',   None)]

python_script = [\
    		 ('N-body 15k',        'nbody',        '--size=150*10'),
#           	 ('N-body 20k',        'nbody',        '--size=200*10'),
#                 ('Shallow Water 20k', 'shallow_water','--size=200*200*10'),
#                 ('Shallow Water 25k', 'shallow_water','--size=250*250*10'),
#                 ('Black Scholes 10m', 'black_scholes','--size=10000*10'),
#                 ('Black Scholes 100m','black_scholes','--size=10000000*10')
]

python = {
    'bridges': [('numpy', 'dython benchmark/Python/{script}.py {args} --bohrium=True', None)],
    'engines': engines,
    'scripts': python_script
}
python_native = {
    'bridges': [('numpy-native', 'python benchmark/Python/{script}.py {args} --bohrium=False', None)],
    'scripts': python_script
}

suites = [python]#, python]

