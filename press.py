#!/usr/bin/env python
from ConfigParser import SafeConfigParser
from subprocess import Popen, PIPE, CalledProcessError
from datetime import datetime

import tempfile
import argparse
import pkgutil
import json
import os
import re

import suites


def meta(src_dir, suite):
    try:
        p = Popen(              # Try grabbing the repos-revision
            ["git", "log", "--pretty=format:%H", "-n", "1"],
            stdin   = PIPE,
            stdout  = PIPE,
            cwd     = src_dir
        )
        rev, err = p.communicate()
    except OSError:
        rev = "Unknown"

    try:
        p = Popen(              # Try grabbing hw-info
            ["lshw", "-quiet", "-numeric"],
            stdin   = PIPE,
            stdout  = PIPE,
        )
        hw, err = p.communicate()
    except OSError:
        hw = "Unknown"

    try:
        p = Popen(              # Try grabbing hw-info
            ["hostname"],
            stdin   = PIPE,
            stdout  = PIPE,
        )
        hostname, err = p.communicate()
    except OSError:
        hostname = "Unknown"

    try:
        p = Popen(              # Try grabbing python version
            ["python", "-V"],
            stdin   = PIPE,
            stdout  = PIPE,
            stderr  = PIPE
        )
        python_ver, err = p.communicate()
        python_ver  += err
    except OSError:
        python_ver = "Unknown"

    try:
        p = Popen(              # Try grabbing gcc version
            ["gcc", "-v"],
            stdin   = PIPE,
            stdout  = PIPE,
            stderr  = PIPE
        )
        gcc_ver, err = p.communicate()
        gcc_ver += err
    except OSError:
        gcc_ver = "Unknown"

    try:
        p = Popen(              # Try grabbing clang version
            ["clang", "-v"],
            stdin   = PIPE,
            stdout  = PIPE,
            stderr  = PIPE
        )
        clang_ver, err = p.communicate()
        clang_ver += err
    except OSError:
        clang_ver = "Unknown"

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

def execute( cmd,envs,src_root,use_perf ):

    cmd = ['taskset', '-c', '0'] + cmd.split(' ')

    if use_perf:
        pfd = tempfile.NamedTemporaryFile(delete=True, prefix='perf-', suffix='.txt')
        cmd = ['perf', 'stat', '-e', perf_counters(), '-B', '-o', str(pfd.name)] + cmd

    cmd_str = ' '.join(cmd)
    print cmd_str
    p = Popen(                              # Run the command
        cmd,
        stdin=PIPE,
        stdout=PIPE,
        env=envs,
        cwd=src_root
    )
    out, err = p.communicate()              # Grab the output
    elapsed = 0.0
    if err or not out:
        raise CalledProcessError(returncode=p.returncode, cmd=cmd, output=err)

    perfs = None
    if use_perf:
        perfs = open(pfd.name).read()

    return (out, perfs, cmd_str)


def main(config, src_root, output, suite, benchmark, runs, use_perf, parallel):

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
            ).communicate()

        if err or not out:
            print "ERR: perf installation broken, disabling perf (%s): %s" % (err, out)
            use_perf = False

    with tempfile.NamedTemporaryFile(delete=False, dir=output, prefix='benchmark-%s-' % suite, suffix='.json') as fd,\
         tempfile.NamedTemporaryFile(delete=True, prefix='bohrium-config-', suffix='.ini') as conf:
        print "Running benchmark suite '%s'; results are written to: %s." % (suite, fd.name)
        for script_alias, script, script_args in benchmark['scripts']:
            for bridge_alias, bridge_cmd, bridge_env in benchmark['bridges']:
                for engine_alias, engine, engine_env in benchmark['engines']:

                    confparser = SafeConfigParser()     # Parser to modify the Bohrium configuration file.
                    confparser.read(config)             # Read current configuration
                    confparser.set("node", "children", engine_alias)
                    conf.truncate(0)                    # And write it to a temp file
                    conf.seek(0)
                    confparser.write(conf)
                    conf.flush()
                    os.fsync(conf)

                    envs = os.environ.copy()            # Populate environment variables
                    envs['BH_CONFIG'] = conf.name
                    if engine_env is not None:
                        envs.update(engine_env)
                    if bridge_env is not None:
                        envs.update(bridge_env)

                    cmd = bridge_cmd.replace("{script}", script)
                    cmd = cmd.replace("{args}", script_args);

                    print "Running %s/%s on %s" %(bridge_alias,script,engine_alias)
                    times = []
                    perfs = []
                    try:
                        for i in xrange(1, runs+1):

                            out, perf, cmd_str = execute( cmd,envs,src_root,use_perf )

                            elapsed = float(out.split(' ')[-1] .rstrip())
                            print "elapsed time: ", elapsed
                            times.append( elapsed )
                            perfs.append( perf )
                    except ValueError:
                        print "Could not parse the output"
                    except CalledProcessError:
                        print "Error in the execution -- skipping to the next benchmark"

                                                         # Accumulate results
                    results['runs'].append({'script':script_alias,
                                            'bridge':bridge_alias,
                                            'engine':engine_alias,
                                            'envs':envs,
                                            'cmd':cmd_str,
                                            'times':times,
                                            'perfs':perfs})
                    results['meta']['ended'] = str(datetime.now())

                    fd.truncate(0)                       # Store the results in a file...
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
        help="Performs * parallel jobs on different processors."
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

