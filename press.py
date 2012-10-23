#!/usr/bin/env python
from ConfigParser import SafeConfigParser
from subprocess import Popen, PIPE, STDOUT
from datetime import datetime
import tempfile
import argparse
import json
import os
import re

# Engines with various parameter setups
# (alias, runs, engine, env-vars)
engines = [
    ('numpy',   None,       None),
    ('simple',  'simple',   None),
    ('score',   'score',    None),
    ('mcore',   'mcore',    None),

    ('score_1',         'score',    {"CPHVB_VE_SCORE_BLOCKSIZE":"1"}),
    ('score_2',         'score',    {"CPHVB_VE_SCORE_BLOCKSIZE":"2"}),
    ('score_4',         'score',    {"CPHVB_VE_SCORE_BLOCKSIZE":"4"}),
    ('score_16',        'score',    {"CPHVB_VE_SCORE_BLOCKSIZE":"16"}),
    ('score_32',        'score',    {"CPHVB_VE_SCORE_BLOCKSIZE":"32"}),
    ('score_64',        'score',    {"CPHVB_VE_SCORE_BLOCKSIZE":"64"}),
    ('score_512',       'score',    {"CPHVB_VE_SCORE_BLOCKSIZE":"512"}),
    ('score_1024',      'score',    {"CPHVB_VE_SCORE_BLOCKSIZE":"1024"}),
    ('score_2048',      'score',    {"CPHVB_VE_SCORE_BLOCKSIZE":"2048"}),
    ('score_4096',      'score',    {"CPHVB_VE_SCORE_BLOCKSIZE":"4096"}),
    ('score_8192',      'score',    {"CPHVB_VE_SCORE_BLOCKSIZE":"8192"}),
    ('score_16384',     'score',    {"CPHVB_VE_SCORE_BLOCKSIZE":"16384"}),
    ('score_32768',     'score',    {"CPHVB_VE_SCORE_BLOCKSIZE":"32768"}),
    ('score_65536',     'score',    {"CPHVB_VE_SCORE_BLOCKSIZE":"65536"}),
    ('score_131072',    'score',    {"CPHVB_VE_SCORE_BLOCKSIZE":"131072"}),
    ('score_262144',    'score',    {"CPHVB_VE_SCORE_BLOCKSIZE":"262144"}),
    ('score_524288',    'score',    {"CPHVB_VE_SCORE_BLOCKSIZE":"524288"}),
    ('score_1048576',   'score',    {"CPHVB_VE_SCORE_BLOCKSIZE":"1048576"}),
    ('score_2097152',   'score',    {"CPHVB_VE_SCORE_BLOCKSIZE":"2097152"}),
    ('score_4194304',   'score',    {"CPHVB_VE_SCORE_BLOCKSIZE":"4194304"}),

    ('score_bins1',    'score',    {"CPHVB_VE_SCORE_BINMAX":"1"}),
    ('score_bins2',    'score',    {"CPHVB_VE_SCORE_BINMAX":"2"}),
    ('score_bins4',    'score',    {"CPHVB_VE_SCORE_BINMAX":"4"}),
    ('score_bins5 ',   'score',    {"CPHVB_VE_SCORE_BINMAX":"5"}),
    ('score_bins6',    'score',    {"CPHVB_VE_SCORE_BINMAX":"6"}),
    ('score_bins8',    'score',    {"CPHVB_VE_SCORE_BINMAX":"8"}),
    ('score_bins10',    'score',    {"CPHVB_VE_SCORE_BINMAX":"10"}),
    ('score_bins12',    'score',    {"CPHVB_VE_SCORE_BINMAX":"12"}),

]
#[('score_blks%d_binm%d' % ((2**i-(2**(i-2)/2)), j), 'score', {"CPHVB_VE_SCORE_BLOCKSIZE": str((2**i-(2**(i-2)/2))), "CPHVB_VE_SCORE_BINMAX": str(j)})  for j in xrange(2,24) for i in xrange(7,21)]

block_sizes = [str((2**i-(2**(i-2)/2))) for i in xrange(7,21) ]
base_maxes  = [str(j) for j in xrange(1,10)]

engines += [
    ('score_blksize%s_basemax%s' % (blksize, basemax),
    'score',
    {
        "CPHVB_VE_SCORE_BLOCKSIZE": blksize,
        "CPHVB_VE_SCORE_BINMAX":    str(20),
        "CPHVB_VE_SCORE_BASEMAX":   basemax,
    }) for basemax in base_maxes for blksize in block_sizes
]

# Scripts and their arguments
# (alias, script, parameters)
scripts   = [
    ('Black Scholes',   'bscholes.py',  '--size=2000000*4'),
    ('Cache Synth',     'cache.py',     '--size=10500000*10*1'),

    ('Jacobi Iterative',            'jacobi.iterative.py',          '--size=7000*7000*4'),
    # This one seems to be broken.
    #('Jacobi Iterative - No Views', 'jacobi.iterative.noviews.py',  '--size=7000*7000*4'),
    ('Jacobi Iterative - Reduce',   'jacobi.iterative.reduc.py',    '--size=7000*7000*4'),

    ('kNN',             'knn.py',       '--size=10000*120'),
    # This is fall back to the bridge
    #('kNN - Naive',     'knn.naive.py', '--size=10000*120*10'),

    ('Lattice Boltzmann 2D', 'lbm.2d.py', '--size=15*200000*2'),
    ('Lattice Boltzmann 3D', 'lbm.3d.py', '--size=100*100*100*2'),

    # This one seems to be broken
    #('LU Factorization', 'lu.py', '--size=5000*10'),   

    ('Monte Carlo PI - RIL',    'mc.py',        '--size=10*1000000*10'),
    ('Monte Carlo PI - 2xN',    'mc.2byN.py',   '--size=10*1000000*10'),
    ('Monte Carlo PI - Nx2',    'mc.Nby2.py',   '--size=10*1000000*10'),

    # This one seems to be broken
    #('N-Body',  'nbody.py', '--size=2500*10'),

    ('Stencil - 1D 4way',       'stencil.simplest.py',  '--size=100000000*1'),
    ('Stencil - 2D',            'stencil.2d.py',        '--size=10000*1000*10'),

    ('Shallow Water',           'swater.py',            '--size=2200*1'),

]
                                # DEFAULT BENCHMARK
default = {                     # Define a benchmark "suite" which runs:
    'scripts': [0,1,2,3,4,5],   # these scripts
    'engines': [0,1,2]        # using these engines
    #'engines': [0,1,2,3]        # using these engines
} 

waters = {
    'scripts':  [2],
    'engines':  [0, 1,2]
}

swaters = {
    'scripts':  [2],
    'engines':  [0,1]+[c for c, x in enumerate(engines) if 'score_b' in x[0]] 
}

cache_tiling = {
    'scripts': [0,1,2],
    'engines': [0,1]+[c for c, x in enumerate(engines) if 'score_blks' in x[0]]
}

test = {
    'scripts': [0],
    'engines': [0,1]
}

test_all = {
    'scripts': [i for i in range(0, len(scripts))],
    'engines': [0,1,2]
}

score_test = {
    'scripts': [i for i in range(0, len(scripts))],
    'engines': [0,1,2]
}

montecarlo = {
    'scripts': [1,9,10],
    'engines':  [0,1,2,3]
}

most = {
    'scripts': range(0,len(scripts)),
    'engines': [0,1,2,3]
}

suites = {
    'default':      default,
    'test':         test,
    'test_all':     test_all,
    'score_test':     score_test,
    'cache_tiling': cache_tiling,
    'most':         most,
    'monte':        montecarlo,
    'waters':       waters,
    'swaters':      swaters,
}

def meta(src_dir, suite):

    p = Popen(              # Try grabbing the repos-revision
        ["git", "log", "--pretty=format:%H", "-n", "1"],
        stdin   = PIPE,
        stdout  = PIPE,
        cwd     = src_dir
    )
    rev, err = p.communicate()

    p = Popen(              # Try grabbing hw-info
        ["lshw", "-quiet", "-numeric"],
        stdin   = PIPE,
        stdout  = PIPE,
    )
    hw, err = p.communicate()

    p = Popen(              # Try grabbing hw-info
        ["hostname"],
        stdin   = PIPE,
        stdout  = PIPE,
    )
    hostname, err = p.communicate()

    p = Popen(              # Try grabbing python version
        ["python", "-V"],
        stdin   = PIPE,
        stdout  = PIPE,
        stderr  = PIPE
    )
    python_ver, err = p.communicate()
    python_ver  += err

    p = Popen(              # Try grabbing python version
        ["gcc", "-v"],
        stdin   = PIPE,
        stdout  = PIPE,
        stderr  = PIPE
    )
    gcc_ver, err = p.communicate()
    gcc_ver += err

    info = {
        'suite':    suite,
        'rev':      rev if rev else 'Unknown',
        'hostname': hostname if hostname else 'Unknown',
        'started':  str(datetime.now()),
        'ended':    None,
        'hw':       {
            'cpu':  open('/proc/cpuinfo','r').read(),
            'list': hw if hw else 'Unknown',
        },
        'sw':   {
            'os':       open('/proc/version','r').read(),
            'python':   python_ver if python_ver else 'Unknown',
            'gcc':      gcc_ver if gcc_ver else 'Unknown',
            'env':      os.environ.copy(),
        },
    }

    return info

def perf_counters():
    """Grabs all events pre-defined by 'perf'."""

    p = Popen(              # Try grabbing the repos-revision
        ["perf", "list"],
        stdin   = PIPE,
        stdout  = PIPE
    )
    out, err = p.communicate()

    events = []
    for m in re.finditer('  (\w+-[\w-]+) ', out):
        events.append( m.group(1) )

    return ','.join(events)

def main(config, src_root, output, suite, runs=5, use_perf=True):

    benchmark   = suites[suite]
    script_path = src_root +os.sep+ 'benchmark' +os.sep+ 'Python' +os.sep
    
    parser = SafeConfigParser()     # Parser to modify the cphvb configuration file.
    parser.read(config)             # Read current configuration

    results = {
        'meta': meta(src_root, suite),
        'runs': []
    }

    with tempfile.NamedTemporaryFile(delete=False, dir=output, prefix='benchmark-', suffix='.json') as fd:
        print "Running benchmark suite '%s'; results are written to: %s." % (suite, fd.name)
        for mark, script, arg in (scripts[snr] for snr in benchmark['scripts']):
            for alias, engine, env in (engines[enr] for enr in benchmark['engines']):

                cphvb = False
                if engine:                                  # Enable cphvb with the given engine.
                    cphvb = True
                    parser.set("node", "children", engine)  
                    parser.write(open(config, 'wb'))

                envs = None                                 # Populate environment variables
                if env:
                    envs = os.environ.copy()
                    envs.update(env)
                                                            # Setup process + arguments
                args        = []
                args        += ['taskset', '-c', '1', 'python', script, arg, '--cphvb=%s' % cphvb ]
                args_str    = ' '.join(args)
                print "{ %s - %s ( %s ),\n  %s" % ( mark, alias, engine, args_str )

                times = []
                perfs = []
                for i in xrange(1, runs+1):

                    if use_perf:
                        pfd = tempfile.NamedTemporaryFile(delete=True, prefix='perf-', suffix='.txt')
                        cmd = ['perf', 'stat', '-e', perf_counters(), '-B', '-o', str(pfd.name)] + args
                    else:
                        cmd = args

                    p = Popen(                              # Run the command
                        cmd,
                        stdin=PIPE,
                        stdout=PIPE,
                        env=envs,
                        cwd=script_path
                    )
                    out, err = p.communicate()              # Grab the output
                    elapsed = 0.0
                    if err or not out:
                        print "ERR: Something went wrong %s" % err
                    else:
                        elapsed = float(out.split(' ')[-1] .rstrip())

                    print "  %d/%d, " % (i, runs), elapsed
                    
                    times.append( elapsed )
                    if use_perf:
                        perfs.append( open(pfd.name).read() )

                print "}"
                                                            # Accumulate results
                results['runs'].append(( mark, alias, engine, env, args_str, times, perfs ))
                results['meta']['ended'] = str(datetime.now())

                fd.truncate(0)                              # Store the results in a file...
                fd.seek(0)
                fd.write(json.dumps(results, indent=4))
                fd.flush()
                os.fsync(fd)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Runs a benchmark suite and stores the results in a json-file.')
    parser.add_argument(
        'src',
        help='Path to the cphvb source-code.'
    )
    parser.add_argument(
        '--suite',
        default="default",
        choices=[x for x in suites],
        help="Name of the benchmark suite to run."
    )
    parser.add_argument(
        '--output',
        default="results",
        help='Where to store benchmark results.'
    )
    parser.add_argument(
        '--runs',
        default=5,
        help="How many times should each benchmark run"
    )
    args = parser.parse_args()

    main(
        os.getenv('HOME')+os.sep+'.cphvb'+os.sep+'config.ini',
        args.src,
        args.output,
        args.suite,
        int(args.runs)
    )

