#!/usr/bin/env python
from ConfigParser import SafeConfigParser
import subprocess
from subprocess import Popen, PIPE, CalledProcessError,check_call
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
import uuid
import time

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
            'cpu':  open('/proc/cpuinfo','r').read() if os.path.isfile('/proc/cpuinfo') else "Unknown",
            'list': hw if hw else 'Unknown',
        },
        'sw':   {
            'os':       open('/proc/version','r').read() if os.path.isfile('/proc/cpuinfo') else 'Probably MacOSX',
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

def execute_run(job):
    """Execute the run locally"""

    with open(job['filename'], 'w') as f:
        #First we have to write the batch script to a file
        f.write(job['script'])
        f.flush()
        os.fsync(f)
        try:# Then we execute the batch script
            p = Popen(['bash', f.name])
            p.wait()
        except KeyboardInterrupt:
            p.kill()
            raise

def slurm_run(job, nnodes=1, queue=None):
    """Submit the run to SLURM using 'nnodes' number of nodes"""
    with open(job['filename'], 'w') as f:
        f.write(job['script'])
        f.flush()
        os.fsync(f)
        print "Submitting %s on %d nodes"%(f.name, nnodes),
        cmd = ['sbatch']
        if queue:
            cmd += ['-p', queue]
        cmd += ['-N', '%d'%nnodes, f.name]
        try:
            p = Popen(cmd, stderr=PIPE, stdout=PIPE)
            out, err = p.communicate()
            job_id = int(out.split(' ')[-1] .rstrip())
            print "with SLURM ID %d"%job_id
        except:
            print _C.FAIL,"ERR: submitting SLURM job!",_C.ENDC
            job['status'] = 'failed'
            raise
        job['slurm_id'] = job_id

def slurm_run_finished(job):
    print "Checking job %d"%job['slurm_id']
    out = subprocess.check_output(['squeue'])
    if out.find(" %d "%job['slurm_id']) != -1:
        return False
    else:
        return True

def parse_run(run, job):
    """Parsing the pending run. NB: the run must be finished!"""
    for i in xrange(job['nrun']):
        base = "%s-%d"%(job['filename'], i)
        stdout = "%s.out"%base
        stderr = "%s.err"%base
        try:
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
                        job['status'] = "failed"
                    else:
                        #We got the result, now the job is finished
                        job['status'] = "finished"
                    if len(err) > 0:
                        print _C.WARNING,"STDERR: ",_C.ENDC
                        print _C.FAIL,"\t",err.replace('\n', '\n\t'),_C.ENDC
            os.remove(stdout)
            os.remove(stderr)
        except IOError:
            print _C.WARNING,"Could not find the stdout and/or the stderr file",_C.ENDC
        try:
            with open("%s.perf"%base, 'r') as perf:
                run['perf'].append(perf.read())
            os.remove("%s.perf"%base)
        except IOError:
            if run['use_perf']:
                print _C.WARNING,"Could not find the perf output file",_C.ENDC
        try:
            with open("%s.time"%base, 'r') as time:
                run['time'].append(time.read())
            os.remove("%s.time"%base)
        except IOError:
            if run['use_time']:
                print _C.WARNING,"Could not find the time output file",_C.ENDC
    try:
        os.remove(job['filename'])
    except OSError:
        print _C.WARNING,"Could not find the batch script: ",job['filename'],_C.ENDC


def get_perf(filename):
    """Return the perf command"""
    out, err = Popen(
        ['which', 'perf'],
        stdout=PIPE,
        stderr=PIPE
    ).communicate()

    # Some distros have a wrapper script :(
    if not err and out:
        perf_cmd = out.strip()
        out, err = Popen(
            ['perf', 'list'],
            stderr=PIPE,
            stdout=PIPE,
        ).communicate()

    if err or not out:
        print _C.WARNING,"ERR: perf installation broken, disabling perf (%s): %s"%(err,out),_C.ENDC
        perf_cmd = ""
    else:
        perf_cmd += ' stat -x , -e %s -o %s '%(perf_counters(), filename)
    return perf_cmd


def get_time(filename):
    """Return the time command"""
    out, err = Popen(
        ['which', 'time'],
        stdout=PIPE,
        stderr=PIPE
    ).communicate()
    if err or not out:
        print _C.WARNING,"ERR: time installation broken, disabling time (%s): %s"%(err,out),_C.ENDC
        time_cmd = ""
    else:
        time_cmd = " %s -v -o %s "%(out.strip(),filename)
    return time_cmd


def add_pending_job(setup, nrun, bridge_cmd, manager_cmd, partition=None):

    cwd = os.path.abspath(os.getcwd())
    basename = "bh-job-%s.sh"%uuid.uuid4()
    filename = os.path.join(cwd,basename)

    job = "#!/bin/bash\n"
    for i in xrange(nrun):
        tmp_config_name = "/tmp/%s_%d.config.ini"%(basename, i)
        for env_key, env_value in setup['envs'].iteritems():      #Write environment variables
            job += 'export %s="${%s:-%s}"\n'%(env_key,env_key,env_value)

        for env_key, env_value in setup['envs_overwrite'].iteritems(): #Write forced environment variables
            job += 'export %s="%s"\n'%(env_key,env_value)

        job += 'export BH_CONFIG=%s\n'%tmp_config_name          #Always setting BH_CONFIG

        job += "\n#SBATCH -J '%s'\n"%setup['script_alias']      #Write Slurm parameters
        job += "#SBATCH -o /tmp/bh-slurm-%%j.out\n"
        job += "#SBATCH -e /tmp/bh-slurm-%%j.err\n"
        if partition is not None:
            job += "#SBATCH -p %s\n"%partition

        #We need to write the bohrium config file to an unique path
        job += 'echo "%s" > %s'%(setup['bh_config'], tmp_config_name)

        job += "\ncd %s\n"%setup['cwd']                           #Change dir and execute cmd

        outfile = "%s-%d"%(filename,i)

        cmd = ""
        if setup['use_time']:
            cmd += get_time("%s.time"%outfile)
        if setup['use_perf']:
            cmd += get_perf("%s.perf"%outfile)
        cmd += bridge_cmd
        if manager_cmd is not None and len(manager_cmd) > 0:
            cmd = manager_cmd.replace("{bridge}", cmd)
        job += "%s "%cmd

        #Pipe the output to files
        job += '1> %s.out 2> %s.err\n'%(outfile,outfile)

        #Cleanup the config file
        job += "\nrm %s\n\n\n"%tmp_config_name

    setup['jobs'].append({'status': 'pending',
                          'filename': filename,
                          'nrun': nrun,
                          'script': job})


def gen_jobs(result_file, config, src_root, suite_file,
             nrun, use_perf, use_time, partition, multi_jobs):
    """Generates benchmark jobs based on the benchmark suites"""

    results = {
        'meta': meta(src_root, suite_file.name),
        'runs': []
    }

    #Lets import the suite file as a Python module
    sys.path.append(os.path.abspath(os.path.dirname(suite_file.name)))
    benchmarks = __import__(os.path.basename(suite_file.name)[:-3]).suites

    print "Benchmark suite '%s'; results are written to: %s" % (suite_file.name, result_file.name)
    i=0
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
                        #if manager and manager != "node":
                        #    confparser.set(manager, "children", "node")
                        if engine:                          # Set the current engine
                            confparser.set("node", "children", engine)

                        confparser.write(bh_config)         # And write it to a string buffer

                        envs = os.environ.copy()            # Populate environment variables
                        envs_overwrite = {}
                        if engine_env is not None:
                            envs_overwrite.update(engine_env)
                        if manager_env is not None:
                            envs_overwrite.update(manager_env)
                        if bridge_env is not None:
                            envs_overwrite.update(bridge_env)

                        bridge_cmd = bridge_cmd.replace("{script}", script)
                        bridge_cmd = bridge_cmd.replace("{args}", script_args)

                        p = "Scheduling %s/%s on "%(bridge_alias,script)
                        if manager and manager != "node":
                            p += "%s/"%manager_alias
                        print "%snode/%s"%(p,engine_alias)

                        run = {'script_alias':script_alias,
                               'bridge_alias':bridge_alias,
                               'engine_alias':engine_alias,
                               'manager_alias':manager_alias,
                               'script':script,
                               'manager':manager,
                               'engine':engine,
                               'envs':envs,
                               'envs_overwrite':envs_overwrite,
                               'cmd': bridge_cmd.split(" "),
                               'cwd':src_root,
                               'pre-hook': benchmark.get('pre-hook', None),
                               'post-hook': benchmark.get('post-hook', None),
                               'jobs':[],
                               'bh_config':bh_config.getvalue(),
                               'use_perf':use_perf,
                               'use_time':use_time,
                               'use_slurm_default':benchmark.get('use_slurm_default', False),
                               'elapsed': [],
                               'time': [],
                               'stdout': [],
                               'stderr': [],
                               'perf':[]}
                        njobs = 1
                        job_nrun = nrun
                        if multi_jobs:
                            njobs = nrun
                            job_nrun = 1
                        for _ in xrange(njobs):
                            i += 1
                            add_pending_job(run, job_nrun, bridge_cmd, manager_cmd, partition)
                        results['runs'].append(run)
                        results['meta']['ended'] = str(datetime.now())

                        bh_config.close()
                        write2json(result_file, results)

def handle_result_file(result_file, args):
    """Execute, submits, and/or parse results of the benchmarks in 'result_file'
       Returns True when all benchmark runs is finished or failed"""

    result_file.seek(0)
    res = json.load(result_file)
    for run in res['runs']:
        for job in run['jobs']:
            if job['status'] == 'finished' or (job['status'] == 'failed' and not args.restart):
                continue
            slurm_id = job.get('slurm_id', None)
            if slurm_id is None or (job['status'] == 'failed' and args.restart):
                #The user wants to use SLURM
                if not args.no_slurm and (args.slurm or run.get('use_slurm_default',False)):
                    nnodes = run['envs'].get('BH_SLURM_NNODES', 1)
                    nnodes = run['envs_overwrite'].get('BH_SLURM_NNODES', nnodes)
                    slurm_run(job, nnodes, queue=None)
                else:
                    #The user wants local execution
                    p = "Executing %s/%s on "%(run['bridge_alias'],run['script'])
                    if run['manager'] and run['manager'] != "node":
                        p += "%s/"%run['manager_alias']
                    print "%snode/%s"%(p,run['engine_alias'])
                    if run['pre-hook'] is not None:
                        print "pre-hook cmd: \"%s\""%run['pre-hook']
                        check_call(run['pre-hook'], shell=True)
                    execute_run(job)
                    parse_run(run, job)
            else:#The job has been submitted to SLURM
                if slurm_run_finished(job):#And it is finished
                    parse_run(run, job)
            write2json(result_file, res)

    #Check if any jobs are pending
    for run in res['runs']:
        for job in run['jobs']:
            if job['status'] == 'pending':
                return False
    return True

def parser_bohrium_src(parser, path):
    """Check that 'path' points to the Bohrium source dir"""
    if os.path.isdir(path):
        return os.path.abspath(path)
    else:
        parser.error("The path %s does not exist!"%path)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Runs a benchmark suite and stores the results in a json-file.')
    parser.add_argument(
        'bohrium_src',
        help='Path to the Bohrium source-code.',
        type=lambda x: parser_bohrium_src(parser, x)
    )
    parser.add_argument(
        'suite_file',
        type=argparse.FileType('r'),
        help="Path to the benchmark suite file."
    )
    parser.add_argument(
        '--output',
        type=str,
        metavar='RESULT_FILE',
        help='Path to the JSON file where the benchmark results will be written. '
             'If the file exist, the benchmark will resume.'
    )
    parser.add_argument(
        '--runs',
        default=3,
        type=int,
        help="How many times should each benchmark run."
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
    parser.add_argument(
        '--restart',
        action="store_true",
        help="Restart execution or submission of failed jobs."
    )

    PUB_CMD_DEFAULT="git clone git@bitbucket.org:bohrium/bohrium-by-night.git "\
                    "&& mv $OUT bohrium-by-night/test/python/numpytest.py.json "\
                    "&& cd bohrium-by-night && git commit -am 'nightly-test' && git push"
    parser.add_argument(
        '--publish-cmd',
        type=str,
        nargs='?',
        const=PUB_CMD_DEFAULT,
        metavar='COMMAND',
        help='The publish command to use before exiting (use together with --wait). '\
             'NB: $OUT is replaced with the name of the output JSON file. '\
             'The default command is: "%s"'%PUB_CMD_DEFAULT
    )
    slurm_grp = parser.add_argument_group('SLURM Queuing System')
    slurm_grp.add_argument(
        '--slurm',
        action="store_true",
        help="Use the SLURM queuing system. This overwrite the default value "\
	     "specified in the suite ('use_slurm_default')"
    )
    slurm_grp.add_argument(
        '--no-slurm',
        action="store_true",
        help="Do not use the SLURM queuing system. This overwrite the default value "\
	     "specified in the suite ('use_slurm_default')"
    )
    slurm_grp.add_argument(
        '--partition',
        type=str,
        help="Submit to a specific SLURM partition."
    )
    slurm_grp.add_argument(
        '--multi-jobs',
        action="store_true",
        help="Submit 'runs' SLURM jobs instead of one job with 'runs' number of runs."
    )
    slurm_grp.add_argument(
        '--wait',
        action="store_true",
        help="Wait for all SLURM jobs to finished before returning."
    )
    args = parser.parse_args()

    if args.publish_cmd and not args.wait:
        parser.error( '--publish-cmd must be used together with --wait' )

    file_name_prefix = 'benchmark-%s-'%os.path.basename(args.suite_file.name)
    try:
        try:
            if args.output is None:
                raise IOError
            result_file = open(args.output, 'r+')
        except IOError:
            if args.output is None:
                result_file = tempfile.NamedTemporaryFile(delete=False,
                                             prefix=file_name_prefix,
                                             suffix='.json')
            else:
                result_file = open(args.output, 'w+')

            #Populate 'result_file' with benchmark jobs/runs
            gen_jobs(result_file,
                os.getenv('HOME')+os.sep+'.bohrium'+os.sep+'config.ini',
                args.bohrium_src,
                args.suite_file,
                args.runs,
                args.no_perf,
                args.no_time,
                args.partition,
                args.multi_jobs
            )

        if args.wait:
            while True:#Probe for finished jobs (one second delay)
                if handle_result_file(result_file, args):
                    all_finished = True
                    break
                time.sleep(5)
        else:
            all_finished = handle_result_file(result_file, args)

        if all_finished:
            print _C.OKGREEN,"Benchmark all finished:",result_file.name,_C.ENDC
        else:
            print _C.WARNING,"Benchmark saved in",result_file.name,
            print "use resume on",result_file.name,_C.ENDC

        if args.publish_cmd:
            tmpdir = tempfile.mkdtemp()
            cmd = "cd %s && "%tmpdir
            cmd += args.publish_cmd.replace("$OUT", result_file.name)
            cmd += " && cd .. && rm -Rf %s"%tmpdir
            print _C.WARNING,"Publishing results using '%s'"%cmd,_C.ENDC
            check_call(cmd, shell=True)

    except KeyboardInterrupt:
        print _C.WARNING,"Suspending the benchmark execution,",
        print "use resume on",result_file.name,_C.ENDC
    finally:
        result_file.close()
