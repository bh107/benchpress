#!/usr/bin/env python
from ConfigParser import SafeConfigParser
import subprocess
from subprocess import Popen, PIPE, CalledProcessError
from datetime import datetime
from multiprocessing import Pool

import tempfile
import argparse
import pkgutil
import json
import os
import sys
import re
import StringIO

import suites

class _C:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


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
    #for m in re.finditer('  ([\w-]+) [\w -]+\[.+\]', out):
    for m in re.finditer('  ([\w-]+) [\w -]+\[(?:Hardware|Software).+\]', out):
        events.append( m.group(1) )

    return ','.join(events)


def write2json(json_file, obj):
    json_file.truncate(0)
    json_file.seek(0)
    json_file.write(json.dumps(obj, indent=4))
    json_file.flush()
    os.fsync(json_file)


def parse_elapsed_times(output):
    """Return list of elapsed times from the output"""

    times = []
    for t in re.finditer("elapsed-time:\s*(\d*\.?\d*)", output):
        times.append(float(t.group(1)))

    if len(times) == 0:
        times = [None]
    return times

def wrap_popen(task):
    p = Popen(                              # Run the command
        task['cmd'],
        stderr=PIPE,
        stdout=PIPE,
        env=task['run']['envs'],
        cwd=task['run']['cwd']
    )
    out, err = p.communicate()              # Grab the output

    #if err or not out:
    #    print "The command '%s' failed:\n%s"%(' '.join(task['cmd']), err)
    #    raise CalledProcessError(returncode=p.returncode, cmd=task['cmd'], output=err)

    res_elapsed = parse_elapsed_times(out)[0]
    res_perf    = ""
    res_time    = ""
    if task['run']['use_perf']:
        res_perf = open(task['run']['use_perf']).read()
    if task['run']['use_time']:
        res_time = open(task['run']['use_time']).read()

    result = (res_elapsed, res_perf, res_time, out)

    return result


def execute_run(run):
    """Execute the run locally"""

    with open(run['pending_job']['filename'], 'w') as f:
        #First we have to write the batch script to a file
        f.write(run['pending_job']['script'])
        f.flush()
        os.fsync(f)
        try:# Then we execute the batch script
            p = Popen(['bash', f.name])
            p.wait()
        except KeyboardInterrupt:
            p.kill()
            raise

def submit_run(run, nnodes=1, queue=None):
    """Submit the run to SLURM using 'nnodes' number of nodes"""

    with open(run['pending_job']['filename'], 'w') as f:
        f.write(run['pending_job']['script'])
        f.flush()
        os.fsync(f)
        print "Submitting %s on %d nodes"%(f.name, nnodes),
        cmd = ['sbatch']
        if queue:
            cmd += ['-p', queue]
        cmd += ['-N', '%d'%nnodes, f.name]
        try:
            subprocess.check_call(cmd)
        except CalledProcessError:
            print "ERR: submitting SLURM job: "
            raise

        job_id = int(out.split(' ')[-1] .rstrip())
        print "with SLURM ID %d"%job_id
        return job_id


def parse_run(run):
    """Parsing the pending run. NB: the run must be finished!"""
    job = run['pending_job']

    for i in xrange(job['nrun']):
        base = "%s-%d"%(job['filename'], i)
        stdout = "%s.out"%base
        stderr = "%s.err"%base
        #print "Parsing result file: %s"%stdout
        with open(stdout, 'r') as out:
            with open(stderr, 'r') as err:
                out = out.read()
                err = err.read()
                run['stdout'].append(out)
                run['stderr'].append(err)
                elapsed = parse_elapsed_times(out)[0]
                print elapsed
                run['elapsed'].append(elapsed)
                if elapsed is None:
                    print _C.WARNING,"Could not find elapsed-time!", _C.ENDC
                    print _C.WARNING,"STDOUT: ",_C.ENDC
                    print _C.OKGREEN,"\t",out.replace('\n', '\n\t'),_C.ENDC
                else:
                    #We got the result, now the job is finished
                    run['pending_job'] = None
                if len(err) > 0:
                    print _C.WARNING,"STDERR: ",_C.ENDC
                    print _C.FAIL,"\t",err.replace('\n', '\n\t'),_C.ENDC
        os.remove(stdout)
        os.remove(stderr)
    os.remove(job['filename'])



def add_pending_job(setup, nrun, uid):

    cwd = os.path.abspath(os.getcwd())
    filename = os.path.join(cwd,"bh-job-%s.sh"%uid)

    job = "#!/bin/bash\n"
    for i in xrange(nrun):
        tmp_config_name = "%s_%d.config.ini"%(filename, i)
        for env_key, env_value in setup['envs'].iteritems():      #Write environment variables
            job += 'export %s="${%s:-%s}"\n'%(env_key,env_key,env_value)

        job += 'export BH_CONFIG=%s\n'%tmp_config_name          #Always setting BH_CONFIG

        job += "\n#SBATCH -J %s\n"%setup['script']                #Write Slurm parameters
        job += "#SBATCH -o %s/bh-job-%%j.out\n"%cwd
        job += "#SBATCH -e %s/bh-job-%%j.err\n"%cwd

        #We need to write the bohrium config file to an unique path
        job += 'echo "%s" > %s'%(setup['bh_config'], tmp_config_name)

        job += "\ncd %s\n"%setup['cwd']                           #Change dir and execute cmd
        job += "%s "%(' '.join(setup['cmd']))                     #The command to execute

        #Pipe the output to files
        job += '1> %s-%d.out 2> %s-%d.err\n'%(filename,i,filename,i)

        #Cleanup the config file
        job += "\nrm %s\n\n\n"%tmp_config_name

    setup['pending_job'] = {'filename': filename, 'nrun': nrun, 'script': job}


def slurm_gather( result_file ):

    result_file.seek(0)
    res = json.load(result_file)

    for run in res['runs']:
        if 'slurm' not in run:
            continue

        for i in xrange(len(run['slurm']['pending_jobs'])):
            job = run['slurm']['pending_jobs'][i]
            if not job:
                continue
            print "Checking job %d"%job['id']

            out = subprocess.check_output(['squeue'])
            if out.find(" %d "%job['id']) != -1:
                continue # The job is still in the SLURM queue

            print "Slurm job %d finished -- parsing %s"%(job['id'], job['out'])
            try:
                with open(job['out'], "r") as fd:
                    out = fd.read()
                    times = parse_elapsed_times(out)
                    times = times[job['warm_ups']:]         #Remove the warm-up runs
                    for t in times:
                        run['times'].append(t)
                        print "elapsed time: ", t
                    run['slurm']['finished_jobs'].append(job)
                    run['slurm']['pending_jobs'][i] = None  #Update the pending job list
                    write2json(result_file, res)            #and save to disk
            except ValueError:
                with open(job['err'], "r") as fd:
                    print "ERR job %d: %s"%(job['id'], fd.read())
            except IOError:
                print "WARNING: couldn't find job file '%s'"%job['out']

    print "Result-file: %s" % result_file.name


def gen_jobs(uid, result_file, config, src_root, output, suite,
             benchmarks, nrun, use_perf, use_time):
    """Generates benchmark jobs based on the benchmark suites"""

    results = {
        'meta': meta(src_root, suite),
        'runs': []
    }

    perf_cmd = []
    if use_perf:
        out, err = Popen(
            ['which', 'perf'],
            stdout=PIPE,
            stderr=PIPE
        ).communicate()

        # Some distros have a wrapper script :(
        if not err and out:
            perf_cmd = [out.strip()]
            out, err = Popen(
                ['perf', 'list'],
                stderr=PIPE,
                stdout=PIPE,
            ).communicate()

        if err or not out:
            print "ERR: perf installation broken, disabling perf (%s): %s" % (err, out)
            use_perf = False
            perf_cmd = []
        else:
            pcounters = perf_counters()

            perf_tmp = tempfile.NamedTemporaryFile(
                prefix='perf-',
                suffix='.data',
                delete=False
            )
            use_perf = perf_tmp.name
            perf_cmd += ['stat', '-x', ',', '-e', pcounters, '-o', perf_tmp.name]

    time_cmd = []
    if use_time:
        out, err = Popen(
            ['which', 'time'],
            stdout=PIPE,
            stderr=PIPE
        ).communicate()
        time_tmp = tempfile.NamedTemporaryFile(
            prefix='time-',
            suffix='.data',
            delete=False
        )
        use_time = time_tmp.name
        time_cmd = [out.strip(), '-v', '-o', time_tmp.name]

        if err or not out:
            print "ERR: time installation broken, disabling time (%s): %s" % (err, out)
            use_time = False
            time_cmd = []

    print "Benchmark suite '%s'; results are written to: %s" % (suite, result_file.name)
    for benchmark in benchmarks:
        for script_alias, script, script_args in benchmark['scripts']:
            for bridge_alias, bridge_cmd, bridge_env in benchmark['bridges']:
                for manager_alias, manager, manager_cmd, manager_env in benchmark.get('managers', [('N/A',None,None,None)]):
                    for engine_alias, engine, engine_env in benchmark.get('engines', [('N/A',None,None)]):

                        bh_config = StringIO.StringIO()
                        confparser = SafeConfigParser()     # Parser to modify the Bohrium configuration file.
                        confparser.read(config)             # Read current configuration
                                                            # Set the current manager
                        confparser.set("bridge", "children", manager if manager else "node")
                        if manager and manager != "node":
                            confparser.set(manager, "children", "node")
                        if engine:                          # Set the current engine
                            confparser.set("node", "children", engine)

                        confparser.write(bh_config)         # And write it to a string buffer

                        envs = os.environ.copy()            # Populate environment variables
                        if engine_env is not None:
                            envs.update(engine_env)
                        if manager_env is not None:
                            envs.update(manager_env)
                        if bridge_env is not None:
                            envs.update(bridge_env)

                        cmd = bridge_cmd.replace("{script}", script)
                        cmd = cmd.replace("{args}", script_args)

                        if manager and manager != "node":
                            cmd = manager_cmd.replace("{bridge}", cmd)

                        p = "Scheduling %s/%s on "%(bridge_alias,script)
                        if manager and manager != "node":
                            p += "%s/"%manager_alias
                        print "%snode/%s"%(p,engine_alias)

                        command = cmd.split(' ')

                        if use_time:
                            command = time_cmd + command

                        if use_perf:
                            command = perf_cmd + command

                        run = {'script_alias':script_alias,
                                                'bridge_alias':bridge_alias,
                                                'engine_alias':engine_alias,
                                                'manager_alias':manager_alias,
                                                'script':script,
                                                'manager':manager,
                                                'engine':engine,
                                                'envs':envs,
                                                'cwd':src_root,
                                                'cmd':command,
                                                'bh_config':bh_config.getvalue(),
                                                'use_perf':use_perf,
                                                'use_time':use_time,
                                                'elapsed': [],
                                                'time': [],
                                                'stdout': [],
                                                'stderr': [],
                                                'perf':[]}
                        add_pending_job(run, nrun, uid)
                        results['runs'].append(run)

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
        default=3,
        type=int,
        help="How many times should each benchmark run."
    )
    parser.add_argument(
        '--resume',
        help='Path to the stored benchmark results.'
    )
    parser.add_argument(
        '--no-perf',
        action="store_false",
        help="Disable the use of the perf measuring tool."
    )
    parser.add_argument(
        '--no-time',
        action="store_false",
        help="Disable the use of the '/usr/bin/time -v' measuring tool."
    )
    """
    affinity_grp = parser.add_argument_group('Saturated Execution')
    affinity_grp.add_argument(
        '--cores',
        nargs='+',
        default=[],
        help="Launch each benchmark concurrently on each provided CPU core."
    )

    slurm_grp = parser.add_argument_group('SLURM Queuing System')
    slurm_grp.add_argument(
        '--slurm',
        action="store_true",
        help="Use the SLURM queuing system."
    )
    slurm_grp.add_argument(
        '--partition',
        type=str,
        help="Submit to a specific SLURM partition."
    )
    slurm_grp.add_argument(
        '--one-job',
        action="store_true",
        help="Submit all runs of a benchmark as one SLURM job."
    )
    slurm_grp.add_argument(
        '--warm-ups',
        type=int,
        default=0,
        help='Submits a number of "warm-up" jobs before the real job.'
    )
    """

    args = parser.parse_args()
    runs = int(args.runs)

    if args.resume:
        result_file = open(args.resume, 'r+')
    else:
        result_file = tempfile.NamedTemporaryFile(delete=False,
                                     dir=args.output,
                                     prefix='benchmark-%s-'%args.suite,
                                     suffix='.json')
    try:
        if not args.resume:
            uid = os.path.basename(result_file.name)[len('benchmark-%s-'%args.suite):-5]
            gen_jobs(uid,
                result_file,
                os.getenv('HOME')+os.sep+'.bohrium'+os.sep+'config.ini',
                args.src,
                args.output,
                args.suite,
                bsuites[args.suite],
                runs,
                args.no_perf,
                args.no_time
            )

        result_file.seek(0)
        res = json.load(result_file)
        for run in res['runs']:
            if run['pending_job'] is None:
                continue
            p = "Executing %s/%s on "%(run['bridge_alias'],run['script'])
            if run['manager'] and run['manager'] != "node":
                p += "%s/"%run['manager_alias']
            print "%snode/%s"%(p,run['engine_alias'])
            execute_run(run)
            parse_run(run)
            write2json(result_file, res)
        print "Results saved in %s"%result_file.name

    except KeyboardInterrupt:
        print _C.WARNING,"Suspending the benchmark execution,",
        print "use resume on",result_file.name,_C.ENDC
    finally:
        result_file.close()
