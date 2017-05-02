"""
===============================
NAS Parallel Benchmarks by NASA
===============================

This script generates a Benchpress suite file that will run the NAS benchmark suite 
<https://www.nas.nasa.gov/publications/npb.html>.
It download and compile the NAS benchmark based on the configuration specified with '--nas-config'

Example
-------

Use the GCC config::
    
    python nas_parallel_benchmark.py --nas-config "make.def.gcc_x86" --output nas_suite.json

And then *run* the suite::

    bp-run nas_suite.json
    
Finally, check the result:: 

    # Wall clock timings
    bp-cli nas_suite.json --parse-regex "Time in seconds\s*=(.+)"
    
    # Mop/s
    bp-cli nas_suite.json --parse-regex "Mop/s total\s*=(.+)"

"""
import urllib
import tarfile
import tempfile
import subprocess
import os
from os.path import join
import benchpress as bp
from benchpress.argument_handling import args, add_argument

if __name__ == "__main__":

    # Adding arguments that are specific to this Benchpress suite
    add_argument(
        '--nas-config',
        default="make.def.gcc_x86",
        help="The name of the NAS config to use."
    )

    # Let's download and unpack the NAS benchmark
    tdir = tempfile.mkdtemp()
    nas_filename = join(tdir, "NAS.tgz")
    print ("Download NAS benchmark to '%s'" % nas_filename)
    urllib.urlretrieve("https://www.nas.nasa.gov/assets/npb/NPB3.3.1.tar.gz", nas_filename)
    tar = tarfile.open(nas_filename)
    tar.extractall(path=tdir)
    tar.close()

    # Choose NAS config
    print ("Using NAS config '%s'" % args().nas_config)
    wdir = join(tdir, "NPB3.3.1/NPB3.3-OMP")
    os.rename("%s/config/NAS.samples/%s" % (wdir, args().nas_config), "%s/config/make.def" % wdir)

    benchmarks = ['bt', 'cg', 'dc', 'ft', 'is', 'lu', 'mg', 'sp', 'ua']
    size = "W"

    for benchmark in benchmarks:
        subprocess.check_call(["make %s CLASS=%s" % (benchmark, size)], shell=True, cwd=wdir)
    print ("BUILD FINISHED\n\n")

    cmd_list = []
    for label in benchmarks:
        bash_cmd = "{root}/bin/{label}.{size}.x".format(root=wdir, label=label, size=size)
        cmd_list.append(bp.command(bash_cmd, "%s/%s/OMP1" % (label, size), env={'OMP_NUM_THREADS': 1}))

    bp.create_suite(cmd_list)
