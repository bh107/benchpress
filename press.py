#!/usr/bin/env python
from ConfigParser import SafeConfigParser
from subprocess import Popen, PIPE, STDOUT
from datetime import datetime

from multiprocessing import Pool
import tempfile
import argparse
import pkgutil
import json
import os
import re

import suites


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

    p = Popen(              # Try grabbing python version
        ["clang", "-v"],
        stdin   = PIPE,
        stdout  = PIPE,
        stderr  = PIPE
    )
    clang_ver, err = p.communicate()
    clang_ver += err

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
            'clang':    clang_ver if clang_ver else 'Unknown',
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
    for m in re.finditer('  ([\w-]+) [\w -]+\[.+\]', out):
        events.append( m.group(1) )

    return ','.join(events)

def execute_numpy( param_set ):

    script, bohrium, envs, script_path, arg, use_perf, affinity = param_set

    args        = []
    args        += ['taskset', '-c', str(affinity), 'python', script, arg, '--bohrium=%s' % bohrium ]
    args_str    = ' '.join(args)

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

    perfs = None
    if use_perf:
        perfs = open(pfd.name).read()

    print affinity, elapsed
    return (elapsed, perfs, args_str)

def run_bohriumnumpy( config, suite, mark, script, arg, alias, engine, env, runs, use_perf, script_path, parallel ):

    confparser = SafeConfigParser()     # Parser to modify the Bohrium configuration file.
    confparser.read(config)             # Read current configuration

    bohrium = False
    if engine:                                  # Enable Bohrium with the given engine.
        bohrium = True
        confparser.set("node", "children", engine)  
        confparser.write(open(config, 'wb'))

    envs = None                                 # Populate environment variables
    if env:
        envs = os.environ.copy()
        envs.update(env)
                                                # Setup process + arguments
    times = []
    perfs = []

    pool = Pool(processes=parallel)
    
    print "Running %s" % mark
    for i in xrange(1, runs+1):

        param_set = [[script, bohrium, envs, script_path, arg, use_perf, j] for j in xrange(0, parallel)]

        res = pool.map( execute_numpy, param_set, 1 )

        for elapsed, perf, args_str in res:
            times.append( elapsed )
            perfs.append( perf )

    return (times, perfs, args_str)


def execute_ccode( param_set ):

    script, bohrium, envs, script_path, arg, use_perf, affinity = param_set

    args        = []
    args        += ['taskset', '-c', str(affinity), script] + arg.split(' ')
    args_str    = ' '.join(args)

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
        elapsed = float(out.split(' ')[5].rstrip())

    perfs = None
    if use_perf:
        perfs = open(pfd.name).read()

    print affinity, elapsed

    return (elapsed, perfs, args_str)

def run_ccode( config, suite, mark, script, arg, alias, engine, env, runs, use_perf, script_path, parallel ):

    envs = None                                 # Populate environment variables
    if env:
        envs = os.environ.copy()
        envs.update(env)
                                                # Setup process + arguments
    times = []
    perfs = []

    pool = Pool(processes=parallel)

    print "Running %s" % mark
    for i in xrange(1, runs+1):

        param_set = [[script, False, envs, script_path, arg, use_perf, j] for j in xrange(0, parallel)]

        res = pool.map( execute_ccode, param_set, 1 )

        for elapsed, perf, args_str in res:
            times.append( elapsed )
            perfs.append( perf )

    return (times, perfs, args_str)

def main(config, src_root, output, suite, benchmark, runs, use_perf, parallel):

    script_path = src_root +os.sep+ 'benchmark' +os.sep+ 'Python' +os.sep

    results = {
        'meta': meta(src_root, suite),
        'runs': []
    }
    
    if use_perf:
        out, err = Popen(
            ['which', 'perf'],
            stdout=PIPE
        ).communicate()

        # Some distros have a wrapper script :(
        if not err and out:
            out, err = Popen(
                ['perf', 'list'],
                stdin=PIPE,
                stdout=PIPE,
                cwd=script_path
            ).communicate()

        if err or not out:
            print "ERR: perf installation broken, disabling perf (%s): %s" % (err, out)
            use_perf = False
            
    with tempfile.NamedTemporaryFile(delete=False, dir=output, prefix='benchmark-%s-' % suite, suffix='.json') as fd:
        print "Running benchmark suite '%s'; results are written to: %s." % (suite, fd.name)
        for mark, script, arg in benchmark['scripts']:
            for alias, engine, env in benchmark['engines']:

                accum = []
                if '.py' in script:

                    (times, perfs, args_str) = run_bohriumnumpy(config, suite, mark, script, arg, alias, engine, env, runs, use_perf, script_path, parallel)
                        
                else:
                    (times, perfs, args_str) = run_ccode(config, suite, mark, script, arg, alias, engine, env, runs, use_perf, script_path, parallel)
                                                            # Accumulate results
                results['runs'].append(( mark, alias, engine, env, args_str, times, perfs ))
                results['meta']['ended'] = str(datetime.now())

                fd.truncate(0)                              # Store the results in a file...
                fd.seek(0)
                fd.write(json.dumps(results, indent=4))
                fd.flush()
                os.fsync(fd)

if __name__ == "__main__":

    bsuites = {}        # Load benchmark-suites from 'suites'
    for name, m in ((module, __import__("suites.%s" % module)) for importer, module, _ in pkgutil.iter_modules(['suites'])):
        bsuites[name] = m.__dict__[name].suite

    parser = argparse.ArgumentParser(description='Runs a benchmark suite and stores the results in a json-file.')
    parser.add_argument(
        'src',
        help='Path to the Bohrium source-code.'
    )
    parser.add_argument(
        '--suite',
        default="default",
        choices=[x for x in bsuites],
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
    parser.add_argument(
        '--useperf',
        default=True,
        help="True to use perf for measuring, false otherwise"
    )
    parser.add_argument(
        '--parallel',
        default=1,
        help="Performs runs * parallel jobs on different processors."
    )
    args = parser.parse_args()

    main(
        os.getenv('HOME')+os.sep+'.bohrium'+os.sep+'config.ini',
        args.src,
        args.output,
        args.suite,
        bsuites[args.suite],
        int(args.runs),
        bool(args.useperf),
        int(args.parallel)
    )

