from default import *

engines = [('GPU',  'gpu',   None)]

python_script = [('Shallow Water 4k x 4k','shallow_water','--size=4000*4000*100 --dtype=float64'),
                 ]
python = {
    'bridges': [python_bohrium],
    'engines': engines,
    'scripts': python_script
}
python_native = {
    'bridges': [python_numpy],
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
    'bridges': [cpp11_bxx],
    'engines': engines,
    'scripts': cpp_script
}
blitz = {
    'bridges': [cpp11_blitz],
    'scripts': cpp_script
}

suites = [python_native, python, cil_native, cil, cpp, blitz]

