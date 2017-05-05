# -*- coding: utf-8 -*-
from __future__ import absolute_import
import json
import os
import tempfile
from .argument_handling import args
from . import time_util


def _check_cmd(cmd_list):
    """Sanity check of the commands in 'cmd_list'"""
    for cmd in cmd_list:
        assert "jobs" not in cmd
        assert "cmd" in cmd
        assert "label" in cmd


def create_suite(cmd_list, output_path=None):
    """Create a suite file (JSON) based on a list of commands
    
    Parameters
    ----------
    cmd_list : list of dict
        List of commands that makes up this benchmark suite. 
    output_path : str
        Path to the output file when the `--output` argument is unset. If `None`, a path to a temporary file is used.  
        
    See Also
    --------
    command : Help function to create a new command

    """
    _check_cmd(cmd_list)

    # Let's print the scheduled jobs
    for cmd in cmd_list:
        print ("Scheduling '%s': '%s'" % (cmd['label'], cmd['cmd']))

    # Beside the commands list, the suite file contains other relevant information:
    suite_dict = {
        'cmd_list': cmd_list,
        'creation_date_utc': time_util.utcnow_str(),
    }

    # Write the json file at an user specified or temporary location
    json_string = json.dumps(suite_dict, indent=4)
    if args().output is not None:
        f = open(args().output, 'w')
    elif output_path is not None:
        f = open(output_path, 'w')
    else:
        f = tempfile.NamedTemporaryFile(delete=False, prefix='benchpress-', suffix='.json')

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
        
    Returns
    -------
    command : dict
        The created Benchpress command        
    """
    return {'cmd': cmd,
            'label': label,
            'env': env}
