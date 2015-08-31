#!/usr/bin/env python
import pprint
import math
import json
import re

ident_mapping = {
    "C/SEQ/NA/NA": "C/S",
    "C/SEQ/TS/NA/NA": "C/ST",
    "C/OMP/node/omp": "C/P",
    "C/OMP//omp": "C/P",
    "C/OMP/node/omp_af": "C/PA",
    "C/OMP//omp_af": "C/PA",

    "C/SEQ/NA/NA": "C/SS",
    "C/OMP/node/omp_si_pe": "C/SP",
    "C/OMP/node/omp_pi_se": "C/PS",
    "C/OMP/node/omp_pi_pe": "C/PP",
    "C/OMP/node/omp_af_pi_pe": "C/PP/AF",
    "C/OMP/node/omp_af_si_pe": "C/SP/AF",

    "CPP/OMP/node/omp": "C++/P",
    "CPP/OMP//omp": "C++/P",
    "CPP/OMP/node/omp_af": "C++/PA",
    "CPP/OMP//omp_af": "C++/PA",
    "CPP/BH/node/cpu_vc_fs_ct": "BXX/VFC",
    "Python/BH/node/cpu": "BHP",
    "Python/BH//cpu": "BHP",
    "Python/BH/node/cpu_vc": "BHP/V",
    "Python/BH//cpu_vc": "BHP/V",
    "Python/BH/node/cpu_vc_fs": "BHP/VF",
    "Python/BH//cpu_vc_fs": "BHP/VF",
    "Python/BH/node/cpu_vc_fs_ct": "BHP/VFC",
    "Python/BH//cpu_vc_fs_ct": "BHP/VFC",
    "Python/BH/node/cpu_fs": "BHP/VFC",
    "Python/BH//cpu_fs": "BHP/VFC",
    "Python/NP/NA/NA": "NumPy",
}

ident_ordering = [
    "NumPy",

    "C/SS",
    "C/SP",
    "C/PS",
    "C/PP",
    "C/SP/AF",
    "C/PP/AF",
    "C/PS/AF",

    "C/S",
    "C/ST",
    "C/P",
    "C/PA",
    "C++/P",
    "C++/PA",
    "BHP",
    "BHP/V",
    "BHP/VF",
    "BHP/VFC",
    "BXX",
    "BXX/V",
    "BXX/VF",
    "BXX/VFC"
]

def order_idents(idents, ordering):

    no_order = list(set(idents) - set(ordering))
    if len(no_order) > 0:
        raise Exception("Ordering is not defined for idents(%s)" % no_order)

    ordered = []
    for ident in ordering:
        if ident in idents:
            ordered.append(ident)
    return ordered

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
    if len(samples) <= 1:
        return mean(samples)

    tsamples = list(samples)        # Truncate samples
    largest = pop_max(tsamples)
    smallest = pop_min(tsamples)

    return mean(tsamples)            # Compute average

def tstd_dev(samples):
    """Compute the truncated standard deviation within the samples."""
    if len(samples) <= 1:
        return std_dev(samples)

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

def datasets_baselinify(datasets):
    """
    Create baseline versions of the datasets.
    Uses the first value of each dataset.

    Adds min/max, removed dev as it does not apply
    well to the relative numbers...
    """
    global_max = 0.0
    baselines = {ident: datasets[ident]["avg"][0] for ident in datasets}
    baselined = {}                  # Make datasets relative
    for bsl_ident in baselines:
        if bsl_ident not in baselined:
            baselined[bsl_ident] = {}
        bsl = baselines[bsl_ident]  # Grab the baseline

        for ident in datasets:
            # Constrcut the baselined entry
            baselined[bsl_ident][ident] = {
                "avg": [],
                "min": 0.0,
                "max": 0.0
            }
            # Compute the relative numbers
            for sample in datasets[ident]["avg"]:
                baselined[bsl_ident][ident]["avg"].append(
                    bsl / sample
                )
            # Highest relative value
            baselined[bsl_ident][ident]["min"] = min(
                baselined[bsl_ident][ident]["avg"]
            )
            # Lowest relative value
            local_max = max(
                baselined[bsl_ident][ident]["avg"]
            )
            baselined[bsl_ident][ident]["max"] = local_max
            if local_max > global_max:
                global_max = local_max

    return global_max, baselined

def extract_parameters(raw):

    # Extract script aliases
    script_aliases = list(set([result["script_alias"] for result in raw["runs"]]))
    script_aliases.sort()

    # Extract script size-args from cmd
    script_aliases = []
    script_args = {}
    for result in raw["runs"]:
        script_alias = result["script_alias"]
        if script_alias not in script_aliases:
            script_aliases.append(script_alias)
            script_args[script_alias] = []

        script_args[script_alias].append(
            result["script_args"]
        )

    # Verify that the same arguments are used for scripts
    for script_alias in script_aliases:
        if len(set(script_args[script_alias])) != 1:
            raise Exception("Different args used for same script!")
        script_args[script_alias] = script_args[script_alias][0]

    script_aliases.sort()

    # Extract bridge aliases
    bridge_aliases = list(set([result["bridge_alias"] for result in raw["runs"]]))
    bridge_aliases.sort()

    # Extract engine aliases
    engine_aliases = list(set([result["engine_alias"] for result in raw["runs"]]))
    engine_aliases.sort()

    # Extract manager aliases
    manager_aliases = list(set([result["manager_alias"] for result in raw["runs"]]))
    manager_aliases.sort()

    # Extract environment variables
    env_vars = list(set([env for result in raw["runs"] for env in result["envs_overwrite"] ]))
    env_vars.sort()

    # Extract values of environment variables and convert their types
    env_values = {env: [] for env in env_vars}
    for result in raw["runs"]:
        for env in env_vars:
            if env in result["envs_overwrite"]:
                env_values[env].append(result["envs_overwrite"][env])

    # Sort the extracted environment variables
    for env in env_vars:
        env_values[env] = list(set(env_values[env]))
        env_values[env].sort()

    return {
        "env_vars": env_vars,
        "env_values": env_values,
        "script_aliases": script_aliases,
        "script_args": script_args,
        "bridge_aliases": bridge_aliases,
        "engine_aliases": engine_aliases,
        "manager_aliases": manager_aliases
    }


if __name__ == "__main__":
    path = "/home/safl/remote/erda/public_base/Bohrium/safl/numbers/engine-01/result.json"

    results = json.load(open(file_path))

    runs = results["runs"]
    runs_flattened = flatten(runs)
    runs_grouped = group_by_script(runs_flattened)
    datasets = datasetify(runs_grouped)
    datasets_renamed = datasets_rename(datasets, ident_mapping)
