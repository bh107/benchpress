engines = [('GPU',  'gpu',   None)]

python_script = [('Shallow Water 4k x 4k','shallow_water','--size=4000*4000*100 --dtype=float64'),
                 ]
python = {
    'bridges': [('numpy', 'python benchmark/python/{script}.py {args} --bohrium=True', None)],
    'engines': engines,
    'scripts': python_script
}
python_native = {
    'bridges': [('numpy-native', 'python benchmark/python/{script}.py {args} --bohrium=False', None)],
    'scripts': python_script
}

cil_script = [('N-body 3200','nbody','--size=3200*50 --no-temp-arrays=True --dtype=double'),
              ]
cil = {
    'bridges': [('CIL', 'mono benchmark/CIL/Csharp/{script}/bin/Release/{script}.exe {args} --bohrium=True', None)],
    'engines': engines,
    'scripts': cil_script
}
cil_native = {
    'bridges': [('CIL-native', 'mono benchmark/CIL/Csharp/{script}/bin/Release/{script}.exe {args} --bohrium=False', None)],
    'scripts': cil_script
}

cpp_script = [('Black Scholes 64M','black_scholes','--size=32000000*50'),
              ]
cpp = {
    'bridges': [('CPP', 'benchmark/cpp/bin/{script} {args}', None)],
    'engines': engines,
    'scripts': cpp_script
}
blitz = {
    'bridges': [('blitz++', 'benchmark/blitz/bin/{script} {args}', None)],
    'scripts': cpp_script
}

suites = [python_native, python, cil_native, cil, cpp, blitz]

