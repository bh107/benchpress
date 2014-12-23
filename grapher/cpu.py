import logging
from graph import *
import pprint

from parser import standard_deviation, variance, avg

env_types = {
    "BH_VE_CPU_JIT_FUSION": int,
    "OMP_NUM_THREADS": int
}

def brange(begin, end):
    c = i = begin
    while i <= end:
        yield i
        i = 2**c
        c += 1

def extract_parameters(data):

    # Extract script aliases
    script_aliases = list(set([result["script_alias"] for result in data]))
    script_aliases.sort()

    # Extract bridge aliases
    bridge_aliases = list(set([result["bridge_alias"] for result in data]))
    bridge_aliases.sort()

    # Extract engine aliases
    engine_aliases = list(set([result["engine_alias"] for result in data]))
    engine_aliases.sort()

    # Extract manager aliases
    manager_aliases = list(set([result["manager_alias"] for result in data]))
    manager_aliases.sort()

    # Extract environment variables
    env_vars = list(set([env for result in data for env in result["envs_overwrite"] ]))
    env_vars.sort()

    # Extract values of environment variables and convert their types
    env_values = {env: [] for env in env_vars}
    for result in data:
        for env in env_vars:
            if env in result["envs_overwrite"]:
                env_values[env].append(
                    env_types[env](result["envs_overwrite"][env])
                )

    # Sort the extracted environment variables
    for env in env_vars:
        env_values[env] = list(set(env_values[env]))
        env_values[env].sort()

    return {
        "env_vars": env_vars,
        "env_values": env_values,
        "script_aliases": script_aliases,
        "bridge_aliases": bridge_aliases,
        "engine_aliases": engine_aliases,
        "manager_aliases": manager_aliases
    }

def flatten(data):
    """
    Flatten the input-data into sorted rows with eight columns of:
    
    (script_alias, bridge_alias, engine_alias, BH_VE_CPU_JIT_FUSION,
     OMP_NUM_THREADS, average(elapsed), var(elapsed), std_dev(elapsed))
  
    :param mixed data: Result file as produced by press.py
    :returns: List of tuples organized as described above.
    :rvalue: Mixed
    """

    def has_holes(elapsed):

        for etime in elapsed:
            if etime == None:
                return True

        return False

    flattened = []
    for result in data:

        elapsed = result["elapsed"]
        if has_holes(elapsed):  # Skip result if it "has holes" in elapsed time
            continue

        var = variance(elapsed) # Extract some time information
        average = avg(elapsed)
        std_dev = standard_deviation(elapsed)

        fusion = 0              # Other properties
        nthreads = 0
        if 'envs_overwrite' in result and 'OMP_NUM_THREADS' in result['envs_overwrite']:
            nthreads = int(result["envs_overwrite"]["OMP_NUM_THREADS"])
        if 'envs_overwrite' in result and 'BH_VE_CPU_JIT_FUSION' in result['envs_overwrite']:
            fusion = int(result["envs_overwrite"]["BH_VE_CPU_JIT_FUSION"])

        flattened.append((
            result['script_alias'],
            result['bridge_alias'],
            result['engine_alias'],
            fusion,
            nthreads,
            average,
            var,
            std_dev
        ))
    flattened.sort()

    return flattened

def restructure(data_flattened):
    """Take the flattened input and structure it somehow."""

    sample_size = 6
    labels = ["fusion+", "fusion-", "numpy"]

    structured = {}
    for data in data_flattened:

        script, bridge, engine, fusion, nthreads, average, var, std_dev = data
        if script not in structured:
            structured[script] = {
                'abs': {'fusion+': [], 'fusion-': [], 'numpy': []},
                'rel_first': {
                    'fusion+':  {'fusion+': [], 'fusion-': [], 'numpy': []},
                    'fusion-':  {'fusion+': [], 'fusion-': [], 'numpy': []},
                    'numpy':    {'fusion+': [], 'fusion-': [], 'numpy': []}
                },
                'rel_all': {
                    'fusion+':  {'fusion+': [], 'fusion-': [], 'numpy': []},
                    'fusion-':  {'fusion+': [], 'fusion-': [], 'numpy': []},
                    'numpy':    {'fusion+': [], 'fusion-': [], 'numpy': []}
                },
            }

        # Sort the results
        if 'fusion' in engine:
            structured[script]['abs']['fusion+'].append((average, var, std_dev))
        elif 'omp' in engine:
            structured[script]['abs']['fusion-'].append((average, var, std_dev))
        else:
            # Create pseudo-samples for NumPy
            for _ in xrange(sample_size):
                structured[script]['abs']['numpy'].append((average, var, std_dev))

    for script in structured:       # Compute relative numbers
        for bsl_label in labels:    # To first value
            baseline = [structured[script]["abs"][bsl_label][0][0]]*sample_size

            structured[script]['rel_first'][bsl_label] = {}

            for other_label in labels:
                other = [x[0] for x in structured[script]["abs"][other_label]]
                structured[script]["rel_first"][bsl_label][other_label] = [
                    bsl / oth for bsl, oth in zip(baseline, other)
                ]

        for bsl_label in labels:    # To each value
            baseline = [x[0] for x in structured[script]["abs"][bsl_label]]

            structured[script]['rel_all'][bsl_label] = {
                bsl_label: [1.0 for _ in baseline]
            }

            for other_label in (label for label in labels if label != bsl_label):
                other = [x[0] for x in structured[script]["abs"][other_label]]
                structured[script]["rel_all"][bsl_label][other_label] = [
                    bsl / oth for bsl, oth in zip(baseline, other)
                ]

    return structured

class Cpu(Graph):
    """Create a graph that illustrates scalabiltity."""

    def render(self, raw, processed=None, params=None):

        import pprint
        pprint.pprint(raw)

        data_flattened = flatten(raw)
        data = restructure(data_flattened)

        min_threads     = 1
        max_threads     = 32
        linear          = list(brange(min_threads, max_threads))
        plot_count      = len(linear)
        
        engine_ord  = ['numpy', 'fusion+', 'fusion-']

        #
        # Data is stored as [(1, time), (2, time), (4, time), ... , (32, time)]
        # Where "numbers" are thread-crount and  "time" is elapsed wall-clock.
        #
        for script in data:
            self.graph_title = script
            self.prep()

            #
            # Plot the actual values
            legends = {'plots': [], 'legends':[]}
            for c, engine_lbl in enumerate(engine_ord):
                values      = plots[script][engine_lbl]
                x_values    = [xval for (xval, yval) in values]
                y_values    = [yval for (xval, yval) in values]
                p, = asdf   = plot(x_values, y_values, "-*")
                
                legends['plots'].append(p)
                legends['legends'].append(engine_lbl)

            if bsl_enable:
                # The ideal speedup
                plot(linear, linear, "--")

                yscale("symlog")
                yticks(linear, linear)
                ylim(ymin=min_threads*0.15, ymax=max_threads*1.5)

                self.yaxis_label="In relation to '%s'" % bsl_engine

            #
            # Scale x-axis with a neat border
            xscale("symlog")
            xticks(linear, linear)
            xlim(xmin=min_threads*0.15, xmax=max_threads*1.5)

            #
            # Plot-legends and their positions
            lgd = legend(
                legends['plots'], legends['legends'],
                loc=3, ncol=3,
                bbox_to_anchor=(0.10, 0.95, 0.9, 0.102), borderaxespad=0.0,
            )

            t = title(script)
            t.set_y(1.05)

            tight_layout()
            self.to_file(script)                # Spit them out to file

