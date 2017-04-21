# -*- coding: utf-8 -*-

import os
import json
from subprocess import Popen, PIPE
import argument_handling
from argument_handling import args


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


def job_execute_locally(job, verbose=False):
    """Execute the job locally"""

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
            raise


def job_gather_results(job):
    """Gather the results of the bash job. NB: the job must be finished!"""

    ret = []
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
            os.remove(stdout)
            os.remove(stderr)
        except IOError:
            print (C.WARN, "Could not find the stdout and/or the stderr file", C.END)
        # Append result of the run
        ret.append(result)
    return ret


def main():
    """Run the commands in the '--output' JSON file not already finished"""

    if args().output is None:
        argument_handling.error("When running, please set argument '--output'")

    with open(args().output, 'r+') as json_file:
        cmd_list = json.load(json_file)
        for cmd in cmd_list:
            for job in cmd['jobs']:
                if job['status'] == 'pending':
                    # The user wants local execution
                    print ("Executing '%s'" % (cmd['label']))
                    job_execute_locally(job)
                    job['results'] = job_gather_results(job)
                    if all(res['success'] for res in job['results']):
                        job['status'] = 'finished'
                    else:
                        job['status'] = 'failed'
                    write2json(json_file, cmd_list)


if __name__ == "__main__":
    main()
