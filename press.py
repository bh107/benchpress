#!/usr/bin/env python
from ConfigParser import SafeConfigParser
import subprocess
from subprocess import Popen, PIPE, CalledProcessError
from datetime import datetime

import tempfile
import argparse
import pkgutil
import json
import os
import sys
import re
import StringIO

import suites


def meta(src_dir, suite):
    try:
        p = Popen(              # Try grabbing the repos-revision
            ["git", "log", "--pretty=format:%H", "-n", "1"],
            stderr  = PIPE,
            stdout  = PIPE,
            cwd     = src_dir
        )
        rev, err = p.communicate()
    except OSError:
        rev = "Unknown"

    try:
        p = Popen(              # Try grabbing hw-info
            ["lshw", "-quiet", "-numeric"],
            stderr  = PIPE,
            stdout  = PIPE,
        )
        hw, err = p.communicate()
    except OSError:
        hw = "Unknown"

    try:
        p = Popen(              # Try grabbing hw-info
            ["hostname"],
            stderr  = PIPE,
            stdout  = PIPE,
        )
        hostname, err = p.communicate()
    except OSError:
        hostname = "Unknown"

    try:
        p = Popen(              # Try grabbing python version
            ["python", "-V"],
            stderr  = PIPE,
            stdout  = PIPE,
        )
        python_ver, err = p.communicate()
        python_ver  += err
    except OSError:
        python_ver = "Unknown"

    try:
        p = Popen(              # Try grabbing gcc version
            ["gcc", "-v"],
            stderr  = PIPE,
            stdout  = PIPE,
        )
        gcc_ver, err = p.communicate()
        gcc_ver += err
    except OSError:
        gcc_ver = "Unknown"

    try:
        p = Popen(              # Try grabbing clang version
            ["clang", "-v"],
            stderr  = PIPE,
            stdout  = PIPE,
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
        stderr  = PIPE,
        stdout  = PIPE
    )
    out, err = p.communicate()

    events = []
    for m in re.finditer('  ([\w-]+) [\w -]+\[.+\]', out):
        events.append( m.group(1) )

    return ','.join(events)


def write2json(json_file, obj):
    json_file.truncate(0)
    json_file.seek(0)
    json_file.write(json.dumps(obj, indent=4))
    json_file.flush()
    os.fsync(json_file)


def parse_elapsed_times( output ):
    """Return list of elapsed times from the output"""

    times = []
    for t in re.finditer("elapsed-time:\s*(\d*\.?\d*)", output):
        times.append(float(t.group(1)))
    return times


def execute( result_file, runs ):
    result_file.seek(0)
    res = json.load(result_file)

    try:
        for run in res['runs']:
            if 'slurm' in run:
                print "Skipping, will not resume SLURM jobs without the --slurm flag"
                continue

            try:
                while len(run['times']) < runs:
                    with tempfile.NamedTemporaryFile(prefix='bohrium-config-', suffix='.ini') as conf:

                        print "Executing %s/%s on %s" %(run['bridge_alias'],run['script'],run['engine_alias'])
                        run['envs']['BH_CONFIG'] = conf.name
                        conf.write(run['bh_config'])            # And write it to a temp file
                        conf.flush()
                        os.fsync(conf)

                        p = Popen(                              # Run the command
                            run['cmd'],
                            stderr=PIPE,
                            stdout=PIPE,
                            env=run['envs'],
                            cwd=run['cwd']
                        )
                        out, err = p.communicate()              # Grab the output

                        if err or not out:
                            raise CalledProcessError(returncode=p.returncode, cmd=run['cmd'], output=err)

                        elapsed = parse_elapsed_times(out)[0]
                        run['times'].append(elapsed)
                        write2json(result_file, res)
                        print "elapsed time: ", elapsed

            except CalledProcessError, ValueError:
                print "Error in the execution -- skipping to the next benchmark"

            write2json(result_file, res)
        print "All finished and saved in %s"%result_file.name

    except KeyboardInterrupt:
        print "Suspending the benchmark execution, use resume on %s"%result_file.name


def slurm_dispatch( result_file, runs, one_job ):

    result_file.seek(0)
    res = json.load(result_file)

    for run in res['runs']:
        runs -= len(run['times']) #Some runs may be done
        run.setdefault('slurm', {'pending_jobs':[]})

        for _ in xrange(runs if not one_job else 1):
            with tempfile.NamedTemporaryFile(delete=False, prefix='bh-', suffix='.slurm') as job_file:

                job = "#!/bin/bash\n"

                for i in xrange(runs if one_job else 1):

                    tmp_config_name = "%s_%d.config.ini"%(job_file.name, i)
                    for env_key, env_value in run['envs'].iteritems():      #Write environment variables
                        job += 'export %s="${%s:-%s}"\n'%(env_key,env_key,env_value)

                    job += 'export BH_CONFIG=%s\n'%tmp_config_name          #Always setting BH_CONFIG
                    run['envs']['BH_CONFIG'] = tmp_config_name

                    job += "\n#SBATCH -J %s\n"%run['script']                #Write Slurm parameters
                    cwd = os.path.abspath(os.getcwd())
                    job += "#SBATCH -o %s/bh-slurm-%%j.out\n"%cwd
                    job += "#SBATCH -e %s/bh-slurm-%%j.err\n"%cwd

                    #We need to write the bohrium config file to an unique path
                    job += 'echo "%s" > %s'%(run['bh_config'], tmp_config_name)

                    job += "\ncd %s\n"%run['cwd']                           #Change dir and execute cmd
                    job += "%s\n"%(' '.join(run['cmd']))

                    job += "\nrm %s\n\n\n"%tmp_config_name

                job_file.write(job)
                job_file.flush()
                os.fsync(job_file)
                print "Submitting %s"%job_file.name,

                p = Popen(
                    ['sbatch','-N', '1', job_file.name],
                    stderr=PIPE,
                    stdout=PIPE
                )
                out, err = p.communicate()
                if err or not out:
                    print "ERR: submitting SLURM job: %s"%err
                    return

                job_id = int(out.split(' ')[-1] .rstrip())
                print "with SLURM ID %d"%job_id

                run['slurm']['pending_jobs'].append((job_id, "%s/bh-slurm-%s.out"%(cwd,job_id),
                                                             "%s/bh-slurm-%s.err"%(cwd,job_id)))
                write2json(result_file, res)


def slurm_gather( result_file ):

    result_file.seek(0)
    res = json.load(result_file)

    for run in res['runs']:
        if 'slurm' not in run:
            continue

        while len(run['slurm']['pending_jobs']) > 0:
            job_id, out_file, err_file = run['slurm']['pending_jobs'].pop()
            print "Checking job %d"%job_id

            out = subprocess.check_output(['squeue'])
            if out.find(" %d "%job_id) != -1:
                continue # The job is still in the SLURM queue

            print "Slurm job %d finished -- parsing %s"%(job_id, out_file)
            try:
                with open(out_file, "r") as fd:
                    out = fd.read()
                    times = parse_elapsed_times(out)
                    if len(times) == 0:
                        raise ValueError
                    for t in times:
                        run['times'].append(t)
                        write2json(result_file, res) #Note that we also save the updated pending_job list here
                        print "elapsed time: ", t
                    #os.remove(out_file)
                    #os.remove(err_file)
            except ValueError:
                with open(err_file, "r") as fd:
                    print "ERR job %d: %s"%(job_id, fd.read())
            except IOError:
                print "WARNING: couldn't find job file '%s'"%out_file


def gen_jobs(result_file, config, src_root, output, suite, benchmarks, use_perf):
    """Generates benchmark jobs based on the benchmark suites"""

    results = {
        'meta': meta(src_root, suite),
        'runs': []
    }

    if use_perf:
        out, err = Popen(
            ['which', 'perf'],
            stdout=PIPE,
            stderr=PIPE
        ).communicate()

        # Some distros have a wrapper script :(
        if not err and out:
            out, err = Popen(
                ['perf', 'list'],
                stderr=PIPE,
                stdout=PIPE,
            ).communicate()

        if err or not out:
            print "ERR: perf installation broken, disabling perf (%s): %s" % (err, out)
            use_perf = False

    print "Benchmark suite '%s'; results are written to: %s" % (suite, result_file.name)
    for benchmark in benchmarks:
        for script_alias, script, script_args in benchmark['scripts']:
            for bridge_alias, bridge_cmd, bridge_env in benchmark['bridges']:
                for engine_alias, engine, engine_env in benchmark.get('engines', [('N/A',None,None)]):

                    bh_config = StringIO.StringIO()
                    confparser = SafeConfigParser()     # Parser to modify the Bohrium configuration file.
                    confparser.read(config)             # Read current configuration
                    if engine:                          # Set the current engine
                        confparser.set("node", "children", engine)

                    confparser.write(bh_config)         # And write it to a string buffer

                    envs = os.environ.copy()            # Populate environment variables
                    if engine_env is not None:
                        envs.update(engine_env)
                    if bridge_env is not None:
                        envs.update(bridge_env)

                    cmd = bridge_cmd.replace("{script}", script)
                    cmd = cmd.replace("{args}", script_args)

                    print "Scheduling %s/%s on %s" %(bridge_alias,script,engine_alias)

                    cmd = ['taskset', '-c', '0'] + cmd.split(' ')

                    results['runs'].append({'script_alias':script_alias,
                                            'bridge_alias':bridge_alias,
                                            'engine_alias':engine_alias,
                                            'script':script,
                                            'engine':engine,
                                            'envs':envs,
                                            'cwd':src_root,
                                            'cmd':cmd,
                                            'bh_config':bh_config.getvalue(),
                                            'use_perf':use_perf,
                                            'times':[],
                                            'perfs':[]})
                    results['meta']['ended'] = str(datetime.now())

                    bh_config.close()
                    write2json(result_file, results)


if __name__ == "__main__":

    bsuites = {}        # Load benchmark-suites from 'suites'
    for name, m in ((module, __import__("suites.%s" % module)) for importer, module, _ in pkgutil.iter_modules(['suites'])):
        bsuites[name] = m.__dict__[name].suites

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
        type=int,
        help="How many times should each benchmark run"
    )
    parser.add_argument(
        '--resume',
        help='Path to the stored benchmark results.'
    )
    parser.add_argument(
        '--no-perf',
        action="store_false",
        help="Disable the use of the perf measuring tool"
    )
    parser.add_argument(
        '--slurm',
        action="store_true",
        help="Use the SLURM queuing system"
    )
    parser.add_argument(
        '--one-job',
        action="store_true",
        help="Submit all runs of a benchmark as one SLURM job"
    )

    args = parser.parse_args()
    runs = int(args.runs)

    if args.resume:
        with open(args.resume, 'r+') as res:
            if args.slurm:
                slurm_gather( res )
            else:
                execute(res, runs)
    else:
        with tempfile.NamedTemporaryFile(delete=False, dir=args.output,
                                         prefix='benchmark-%s-' % args.suite,
                                         suffix='.json') as res:
                gen_jobs(res,
                    os.getenv('HOME')+os.sep+'.bohrium'+os.sep+'config.ini',
                    args.src,
                    args.output,
                    args.suite,
                    bsuites[args.suite],
                    args.no_perf,
                )
                if args.slurm:
                    slurm_dispatch( res, runs, args.one_job )
                    slurm_gather( res )
                else:
                    execute( res, runs )
