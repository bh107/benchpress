# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
import json
import argparse
import uuid
from subprocess import Popen, PIPE, check_output


class C:
    HEAD = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARN = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'


def write2json(json_file, obj):
    """Write the 'obj' into file 'json_file' """
    json_file.truncate(0)
    json_file.seek(0)
    json_file.write(json.dumps(obj, indent=4))
    json_file.flush()
    os.fsync(json_file)


def bash_job(args, cmd, nruns):
    """Creates a bash job based on the 'cmd' dict that runs the 'cmd['cmd']' 'nruns' times"""

    cwd = os.path.abspath(os.getcwd())
    basename = "bh-job-%s.sh" % uuid.uuid4()
    filename = os.path.join(cwd, basename)

    bash = "#!/bin/bash\n"

    # Write Slurm parameters
    bash += "\n#SBATCH -J '%s'\n" % cmd['label']
    bash += "#SBATCH -o /tmp/bh-slurm-%%j.out\n"
    bash += "#SBATCH -e /tmp/bh-slurm-%%j.err\n"
    if args.partition is not None:
        bash += "#SBATCH -p %s\n" % args.partition
    bash += "#SBATCH --nice=%d\n" % args.nice
    bash += "\n"

    # Write environment variables
    for env_key, env_value in cmd.get('env', {}).items():
        bash += 'export %s="%s"\n' % (env_key, env_value)
    bash += "\n"

    # Execute the warm up run
    if args.warmup:
        bash += "# Warm up run\n%s\n" % cmd['cmd']
        bash += 'sync\n\n'

    # Execute command 'nruns' times
    bash += "# The runs \n"
    for i in range(nruns):
        # Write the command to execute
        bash += "%s " % cmd['cmd']

        # Pipe the output to file
        outfile = "%s-%d" % (filename, i)
        bash += '> >(tee %s.out) 2> >(tee %s.err >&2)\n' % (outfile, outfile)

        # Finally, we call sync
        bash += 'sync\n'

    return {'status': 'pending', 'filename': filename, 'nruns': nruns, 'script': bash, 'warmup': args.warmup}


def create_jobs(args, cmd):
    """Create the list of bash jobs that will execute the 'cmd'"""

    # Find the number of bash jobs and the number of runs with each bash job
    njobs = 1
    nruns_per_job = args.nruns
    if args.multi_jobs:
        njobs = args.nruns
        nruns_per_job = 1
    return [bash_job(args, cmd, nruns_per_job) for _ in range(njobs)]


def job_execute_locally(job, verbose=False, dirty=False):
    """Execute the job locally"""
    try:
        with open(job['filename'], 'w') as f:
            # First we have to write the bash script to a file
            f.write(job['script'])
            f.flush()
            os.fsync(f)
            # Then we execute the bash script
            try:
                p = Popen(['bash', f.name], stdout=PIPE)
                if verbose:
                    while p.poll() is None:
                        print (p.stdout.readline())
                    print (p.stdout.read())
                p.wait()
            except KeyboardInterrupt:
                p.kill()
                if not dirty:
                    for i in range(job['nruns']):
                        base = "%s-%d" % (job['filename'], i)
                        stdout = "%s.out" % base
                        stderr = "%s.err" % base
                        try:
                            os.remove(stdout)
                            os.remove(stderr)
                        except OSError:
                            pass
                raise KeyboardInterrupt()
    finally:
        try:
            if not dirty:
                os.remove(job['filename'])
        except OSError:
            pass


def job_execute_slurm(job, dirty=False, partition=None):
    """Execute the job through SLURM"""
    try:
        with open(job['filename'], 'w') as f:
            # First we have to write the bash script to a file
            f.write(job['script'])
            f.flush()
            os.fsync(f)
            # Then we submit the SLURM script
            cmd = ['sbatch']
            if partition is not None:
                cmd += ['-p', partition]
            cmd += [f.name]
            p = Popen(cmd, stdout=PIPE)
            out, err = p.communicate()
            job['slurm_id'] = int(out.split(' ')[-1].rstrip())
            print ("with SLURM ID %d" % job['slurm_id'])
    finally:
        try:
            if not dirty:
                os.remove(job['filename'])
        except OSError:
            pass


def slurm_check_finished(job):
    """Check if a SLUM job has finished"""
    print ("Checking job %d"%job['slurm_id'])
    out = check_output(['squeue'])
    if out.find(" %d " % job['slurm_id']) != -1:
        return False
    else:
        return True


def job_gather_results(job, dirty=False):
    """Gather the results of the bash job and updates the job status. NB: the job must be finished!"""

    job['results'] = []
    for i in range(job['nruns']):
        base = "%s-%d" % (job['filename'], i)
        stdout = "%s.out" % base
        stderr = "%s.err" % base
        result = {'success': False}
        try:
            with open(stdout, 'r') as out:
                with open(stderr, 'r') as err:
                    result['stdout'] = out.read()
                    result['stderr'] = err.read()

                    # TODO: output validation check
                    result['success'] = True

                    if len(result['stderr']) > 0:
                        print ("%sSTDERR:%s" % (C.WARN, C.END))
                        print ("%s\t%s%s" % (C.FAIL, result['stderr'].replace('\n', '\n\t'), C.END))
            if not dirty:
                os.remove(stdout)
                os.remove(stderr)
        except IOError:
            print (C.WARN, "Could not find the stdout and/or the stderr file", C.END)
        # Append result of the run
        job['results'].append(result)

    # Finally, let's update the job status
    if all(res['success'] for res in job['results']):
        job['status'] = 'finished'
    else:
        job['status'] = 'failed'


def main():
    """Run the commands in the JSON file not already finished"""

    parser = argparse.ArgumentParser(description='Runs a benchmark suite and stores the results in a JSON-file.')
    parser.add_argument(
        'suite',
        type=argparse.FileType('r+'),
        help='Path to the JSON file where the benchmark results will be read and written. '
             'If the file exist, the benchmark will resume.'
    )
    parser.add_argument(
        '--nruns',
        default=3,
        type=int,
        help="How many times should each command run."
    )
    parser.add_argument(
        '--warmup',
        action="store_true",
        help="Execute one warm up run, before the measured runs"
    )
    parser.add_argument(
        '--dirty',
        action="store_true",
        help="Do no clean up."
    )
    parser.add_argument(
        '--tag',
        type=str,
        default=None,
        help="Assign a tag to the result."
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
        '--multi-jobs',
        action="store_true",
        help="Submit 'nruns' SLURM jobs instead of one job with 'nruns' number of runs."
    )
    # TODO: implement --wait
    """
    slurm_grp.add_argument(
        '--wait',
        action="store_true",
        help="Wait for all SLURM jobs to finished before returning."
    )
    """
    slurm_grp.add_argument(
        '--nice',
        type=int,
        help="The scheduling priority - range is from -10000 (highest priority) to "
             "10000 (lowest  priority) where zero is default.  Only  privileged  "
             "users can specify a negative priority.",
        default=0
    )
    args = parser.parse_args()

    print ("Running benchmark; results are written to: %s" % args.suite.name)
    try:
        suite = json.load(args.suite)
        if args.tag is not None:
            suite['tag'] = args.tag
        cmd_list = suite['cmd_list']
        for cmd in cmd_list:
            if 'jobs' not in cmd:
                cmd['jobs'] = create_jobs(args, cmd)
            for job in cmd['jobs']:
                if job['status'] == 'pending':
                    slurm_id = job.get('slurm_id', None)
                    if args.slurm and slurm_id is None: # We need to submit the job to SLURM
                        job_execute_slurm(job, partition=args.partition)

                    elif slurm_id is not None:  # The job has already been submitted to SLURM
                        if slurm_check_finished(job):
                            job_gather_results(job, dirty=args.dirty)

                    else:  # The user wants local execution
                        print ("Executing '%s'" % (cmd['label']))
                        job_execute_locally(job, dirty=args.dirty)
                        job_gather_results(job, dirty=args.dirty)
                    # We always need to update the json
                    write2json(args.suite, suite)
        print ("%sFinished execution, result written in '%s'%s" % (C.WARN, args.suite.name, C.END))
    except KeyboardInterrupt:
        print ("%sSuspending the benchmark execution, "
               "continue with: 'bp-run %s'%s" % (C.WARN, args.suite.name, C.END))


if __name__ == "__main__":
    main()
