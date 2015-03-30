
scripts   = [
    ('Heat 2D',                      'heat_equation',      '--size=3000*3000*100'),
    ('Shallow Water',                'shallow_water',      '--size=2000*2000*100'),
    ('snakes_and_ladders',           'snakes_and_ladders', '--size=1000*10'),
    ('snakes_and_ladders_no_matmul', 'snakes_and_ladders', '--size=1000*10 --no-extmethods'),
]

PREFIX = 'python benchmark/python/{script}.py {args} '

backends = {
    'bridges': [
	('NumPy Original', PREFIX+'--bohrium=False', None),
	('npbacked-numpy (vcache=0)', PREFIX+'--bohrium=True',{'BHPY_BACKEND':'numpy','VCACHE_SIZE':0}),
	('npbacked-numpy (vcache=10)',PREFIX+'--bohrium=True',{'BHPY_BACKEND':'numpy','VCACHE_SIZE':10}),
	('npbacked-numexpr (vcache=0)', PREFIX+'--bohrium=True',\
			{'OMP_NUM_THREADS':8, 'BHPY_BACKEND':'numexpr','VCACHE_SIZE':0}),
	('npbacked-numexpr (vcache=10)',PREFIX+'--bohrium=True',\
			{'OMP_NUM_THREADS':8,'BHPY_BACKEND':'numexpr','VCACHE_SIZE':10}),
	('npbacked-pygpu (vcache=0)', PREFIX+'--bohrium=True',{'BHPY_BACKEND':'pygpu','VCACHE_SIZE':0}),
	('npbacked-pygpu (vcache=10)',PREFIX+'--bohrium=True',{'BHPY_BACKEND':'pygpu','VCACHE_SIZE':10}),
	       ],
    'scripts':  scripts
}

bohriums = {
    'bridges': [('Bohrium', PREFIX+'--bohrium=True', None)],
    'engines': [('GPU', 'gpu', {'OMP_NUM_THREADS':8}), ('CPU', 'cpu', {'OMP_NUM_THREADS':8})],
    'scripts': scripts
}

suites = [backends, bohriums]
