#!/usr/bin/env python
import pprint
import math
import json
import re

serial_launchers = ['Python/NP', 'CPP/SEQ', 'CPP/SEQ/TS', 'C/SEQ', 'C/SEQ/TS']
parallel_launchers = ['Python/BH', 'CPP/BH', 'CPP/OMP', 'C/OMP', 'C/OMP_MPI']

ident_mapping = {
    "C/SEQ/NA/NA": "C/S",
    "CPP/OMP/node/omp": "C++/P",
    "CPP/OMP/node/omp_af": "C++/PA",
    "Python/BH/node/cpu": "BH",
    "Python/BH/node/cpu_vc": "BH/V",
    "Python/BH/node/cpu_vc_fs": "BH/VF",
    "Python/BH/node/cpu_vc_fs_ct": "BH/VFC",
    "Python/BH/node/cpu_fs": "BH/VFC",
    "Python/NP/NA/NA": "NumPy",
}

def pop_max(samples):
    """Remove and return the largest among given samples."""

    largest = 0
    for i, e in enumerate(samples):
        if e > samples[largest]:
            largest = i
    return samples.pop(largest)

def pop_min(samples):
    """Remove and return the smallest among given samples."""
    smallest = 0
    for i, e in enumerate(samples):
        if e < samples[smallest]:
            smallest = i
    return samples.pop(smallest)

def mean(samples):
    """Compute the mean."""
    nsamples = float(len(samples))
    if nsamples > 0.0:
        return sum(samples) / nsamples
    else:
        return 0.0

def std_dev(samples):
    """Compute the standard deviation within the samples."""
    count = len(samples)
    if (count<2):
        return 0.0
    x_avg = mean(samples)
    return math.sqrt(mean([abs(x - x_avg)**2 for x in samples]))

def tmean(samples):
    """
    Returns a truncated mean, average of the samples without
    outliers (smallest and largest).
    """
    tsamples = list(samples)        # Truncate samples
    largest = pop_max(tsamples)
    smallest = pop_min(tsamples)

    return mean(tsamples)            # Compute average

def tstd_dev(samples):
    """Compute the truncated standard deviation within the samples."""
    tsamples = list(samples)        # Truncate samples
    pop_max(tsamples)
    pop_min(tsamples)

    count = len(tsamples)
    if (count<2):
        return 0.0
    x_avg = mean(tsamples)
    return math.sqrt(mean([abs(x - x_avg)**2 for x in tsamples]))

def flatten(runs, averager=tmean, deviater=tstd_dev):
    """
    Flatten the runs averaging elapsed time and computing deviation.
    """
    runs_flattened = []
    for run in runs:
        runs_flattened.append((
            run["script_alias"], run["bridge_alias"],
            run["manager_alias"], run["engine_alias"],
            averager(run["elapsed"]), deviater(run["elapsed"])
        ))
    runs_flattened.sort()
    return runs_flattened

def group_by_script(runs_flattened):
    """
    Group by script, squash the Bohrium stack-configuration into a single string.
    Something like:
    {"Heat Equation": [
        (CPP/OMP/node/omp_t01, 42.2, 0.002),
        ...
        (CPP/OMP/node/omp_t02, 38.2, 0.003),
    ]
    """

    grouped = {}
    squashes = {}
    for script, bridge, manager, engine, avg, dev in runs_flattened:
        if script not in grouped:
            grouped[script] = []
            squashes[script] = []

        squash = "/".join([bridge, manager, engine])
        if squash in squashes[script]:
            raise Exception("%s is already in there" % squash)
        squashes[script].append(squash)
        grouped[script].append((squash, avg, dev))

    return grouped

def datasetify(runs_grouped, length=6):
    """
    {
        "Heat Equation": {
            "Python/NP/NA/NA": {
                "avg": [2,2,2,2,2,2],
                "dev": [0,0,0,0,0,0]
            },
            "Python/BH/node/cpu": {
                "avg": [40, 20, 10, 5, 2.5, 1.25],
                "dev": [0, 0, 0, 0, 0, 0]
            }
        }
    }
    """

    def par_postfix(ident):
        parallel_postfix = "(.*)_t(\d\d$)"
        m = re.match(parallel_postfix, ident)
        if m:
            return m.group(1), m.group(2)
        else:
            return ident, None

    dataset = {}
    for script in runs_grouped:
        if script not in dataset:
            dataset[script] = {}

        for squash, avg, dev in runs_grouped[script]:
            ident, parallel = par_postfix(squash)
            if ident not in dataset[script]:
                dataset[script][ident] = {
                    'avg': [],
                    'dev': [],
                }
            dataset[script][ident]["avg"].append(avg)
            dataset[script][ident]["dev"].append(dev)

            if not parallel:
                dataset[script][ident]["avg"] += [avg]*(length-1)
                dataset[script][ident]["dev"] += [dev]*(length-1)

    return dataset

def dataset_rename(dataset, mapping):
    renamed = {}
    for ident in dataset:
        if ident not in mapping:
            raise Exception("Failed renaming, ident(%s) does not exist in mapping." % ident)
        renamed[mapping[ident]] = dataset[ident]
    return renamed

def datasets_rename(datasets, mapping):
    renamed = {}
    for script in datasets:
        renamed[script] = dataset_rename(datasets[script], mapping)
    return renamed

if __name__ == "__main__":
    path = "/home/safl/remote/erda/public_base/Bohrium/safl/numbers/engine-01/result.json"

    results = json.load(open(file_path)) 

    runs = results["runs"]
    runs_flattened = flatten(runs)
    runs_grouped = group_by_script(runs_flattened)
    datasets = datasetify(runs_grouped)
    datasets_renamed = datasets_rename(datasets, ident_mapping)
