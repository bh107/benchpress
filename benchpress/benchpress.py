# -*- coding: utf-8 -*-
import json
import os
import uuid
import tempfile
from argument_handling import args


def _check_cmd(cmd_list):
    """Sanity check of the commands in 'cmd_list'"""
    for cmd in cmd_list:
        assert "jobs" not in cmd
        assert "cmd" in cmd
        assert "label" in cmd


def _bash_job(cmd, nruns=1):
    """Creates a bash job based on the 'cmd' dict that runs the 'cmd['cmd']' 'nruns' times"""

    cwd = os.path.abspath(os.getcwd())
    basename = "bh-job-%s.sh" % uuid.uuid4()
    filename = os.path.join(cwd, basename)

    bash = "#!/bin/bash\n"

    # Write Slurm parameters
    bash += "\n#SBATCH -J '%s'\n" % cmd['label']
    bash += "#SBATCH -o /tmp/bh-slurm-%%j.out\n"
    bash += "#SBATCH -e /tmp/bh-slurm-%%j.err\n"
    if args().partition is not None:
        bash += "#SBATCH -p %s\n" % args().partition
    bash += "#SBATCH --nice=%d\n" % args().nice

    # Write environment variables
    for env_key, env_value in cmd.get('env', {}).items():
        bash += 'export %s="%s"\n' % (env_key, env_value)

    # Execute command 'nruns' times
    for i in range(nruns):
        # Write the command to execute
        bash += "%s " % cmd['cmd']

        # Pipe the output to file
        outfile = "%s-%d" % (filename, i)
        bash += '> >(tee %s.out) 2> >(tee %s.err >&2)\n' % (outfile, outfile)

        # Finally, we call sync
        bash += 'sync\n'

    return {'status': 'pending', 'filename': filename, 'nruns': nruns, 'script': bash}


def create_suite(cmd_list):
    """Create a suite file (JSON) based on a list of commands
    
    Parameters
    ----------
    cmd_list : list of dict
        List of commands that makes up this benchmark suite. 
        
    See Also
    --------
    command : Help function to create a new command

    """
    _check_cmd(cmd_list)

    # Find the number of bash jobs and the number of runs with each bash job
    njobs = 1
    nruns_per_job = args().runs
    if args().multi_jobs:
        njobs = args().runs
        nruns_per_job = 1

    # Let's create pending bash jobs
    for cmd in cmd_list:
        print ("Scheduling '%s': '%s'" % (cmd['label'], cmd['cmd']))
        cmd['jobs'] = [_bash_job(cmd, nruns=nruns_per_job) for _ in range(njobs)]

    # Write the json file at an user specified or temporary location
    json_string = json.dumps(cmd_list, indent=4)
    if args().output is None:
        f = tempfile.NamedTemporaryFile(delete=False, prefix='benchpress-', suffix='.json')
    else:
        f = open(args().output, 'w')
    f.write(json_string)
    f.flush()
    os.fsync(f.fileno())
    print ("Writing suite file: %s" % f.name)
    f.close()


def command(cmd, label, env={}):
    """Create a Benchpress command, which define a single benchmark execution

    This is a help function to create a Benchpress command, which is a Python `dict` of the parameters given.

    Parameters
    ----------
    cmd : str
        The bash string that makes up the command
    label : str
        The human readable label of the command
    env : dict
        The Python dictionary of environment variables to define before execution'
    """
    return {'cmd': cmd,
            'label': label,
            'env': env}
