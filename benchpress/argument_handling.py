# -*- coding: utf-8 -*-
import argparse

_parser = argparse.ArgumentParser(description='Runs a benchmark suite and stores the results in a JSON-file.')
_parser.add_argument(
    '--output',
    type=str,
    metavar='RESULT_FILE',
    help='Path to the JSON file where the benchmark results will be written. '
         'If the file exist, the benchmark will resume.'
)
_parser.add_argument(
    '--runs',
    default=3,
    type=int,
    help="How many times should each command run."
)


slurm_grp = _parser.add_argument_group('SLURM Queuing System')
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
slurm_grp.add_argument(
    '--wait',
    action="store_true",
    help="Wait for all SLURM jobs to finished before returning."
)
slurm_grp.add_argument(
    '--nice',
    type=int,
    help="The scheduling priority - range is from -10000 (highest priority) to "
         "10000 (lowest  priority) where zero is default.  Only  privileged  "
         "users can specify a negative priority.",
    default=0
)

# This module maintains the state to '_args'
_args = None


def args():
    """Return the argparse object"""
    global _args
    if _args is None:
        _args = _parser.parse_args()
    return _args


def error(msg):
    """Raise an argparse error"""
    _parser.error(msg)
