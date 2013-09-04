#!/usr/bin/env python
#
#
# (source, token, regex, converter)
#
# The result-file has three sources: "output", "time", and "perf".
# They contain the plain-text output from the standard output
# when running the benchmark, the output from /usr/bin/time and
# the output of the perf-tool with as many counters as possible.
#
# Tokens include elapsed, utime, stime, wtime, etc.
#
# The regex in the expression that will search through the source.
#
# Converter is any function x -> x. Useful for converting to 
# floats etc.
#
import pprint
import json
import sys
import os
import re

tokens = [
    ('output',  'elapsed', 'elapsed-time: ([\d.]+)', float),
    ('output',  'bytes_missed', "bytes_missed:.?'(\d+)'", int),
    ('output',  'bytes_reused', "bytes_reused:.?'(\d+)'", int),
    ('time',    'utime', "User\stime\s\(seconds\):\s([\d.]+)", float),
    ('time',    'stime', "System\stime\s\(seconds\):\s([\d.]+)", float),
    ('time',    'resident_kb', "Maximum\sresident\sset\ssize\s\(kbytes\):\s(\d+)", int),
]

def from_file(results_fn):
    """Parses a result-file into something slightly more useful."""

    res = []
    with(open(results_fn)) as fd:
        results = json.load(fd)['runs']
        for run in results:

            data = {}                   # Grab the tokens
            for source, token, regex, conv in tokens:
                if source not in run:   # Source is not available
                    continue
                if token not in data:   # First entry for this token
                    data[token] = []

                topic = ''.join(run[source])
                matches = re.finditer(regex, topic)
                for m in matches:       # Remaining entries
                    data[token].append(conv(m.group(1)))

                                        # Legacy mode...
            if 'elapsed' not in data and 'times' in run:
                data['elapsed'] = run['times']
            
            res.append((
                run['script_alias'],
                run['bridge_alias'],
                run['manager_alias'],
                run['engine_alias'],
                data
            ))
    res = sorted(res)

    return res

