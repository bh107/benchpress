
scripts   = [
    ('Heat 2D',       'heat_equation',  '--size=1000*1000*10'),
    ('Shallow Water', 'shallow_water',  '--size=100*100*10'),
]

PREFIX = 'python benchmark/Python/{script}.py {args} ' 

numpy_org = {
    'bridges': [
	('NumPy Original',   PREFIX + '--bohrium=False', None),
	('npbacked-numpy',   PREFIX + '--bohrium=True', {'BHPY_BACKEND':'numpy'}),
	('npbacked-numexpr', PREFIX + '--bohrium=True', {'BHPY_BACKEND':'numexpr', 'OMP_NUM_THREADS':4}),
	('npbacked-pygpu',   PREFIX + '--bohrium=True', {'BHPY_BACKEND':'pygpu'}),
	       ],
    'scripts':  scripts
}

suites = [numpy_org]
