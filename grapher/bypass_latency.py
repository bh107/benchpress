from graph import *
from pprint import pprint

def bypass_latency(data):

    # Without visualization (just latency)
    proxy_benchmarks = ["Shallow Water 25k", "N-body 25k",  "Heat Equation 25k", "Black Scholes 100m"]
    proxy_data = {}
    for script in proxy_benchmarks:
        proxy_data[script] = data[script]

    #
    #   Classification
    delays  = [0, 50, 100, 200]
    lbl_map = {
        'numpy/cluster/cpu':        'noproxy',
        'numpy/proxy/sleep':        'proxy1',
        'numpy/proxyDCSC/sleep':    'proxy2'
    }

    flattened = []

    #
    # Turn results into a list of something
    for script in proxy_data:
        for label in proxy_data[script]:
            if 'ms' in label:   # Grab those with delays
                exploded = label.split(' ')
                lbl     = lbl_map[exploded[0]]
                delay   = int(exploded[-1].replace('ms',''))
                flattened.append((lbl, script, (
                    delay,
                    proxy_data[script][label]['elapsed']['avg'][0],
                    proxy_data[script][label]['elapsed']['var'][0]
                )))
            else:               # Add a pseudo-delay for baseline
                lbl = lbl_map[label]
                for delay in delays:
                    flattened.append((lbl, script, (
                        delay,
                        proxy_data[script][label]['elapsed']['avg'][0],
                        proxy_data[script][label]['elapsed']['var'][0]
                    )))

    #
    # Then into a dict
    setups = {'noproxy': {}, 'proxy1': {}, 'proxy2':{}}
    for setup, script, sample in flattened:
        if script not in setups[setup]:
            setups[setup][script] = []

        setups[setup][script].append(sample)

    #
    # Sort the samples
    for setup in setups:
        for script in setups[setup]:
            setups[setup][script].sort()

    #
    # Now setup the experiments

    experiments = {
        'overhead': {},
        'octuplets_absolute': {}, 'dcsc_absolute':{},
        'octuplets_relative': {}, 'dcsc_relative':{},
    }

    def baseline_it(dataset, target, baseline):
        experiment = {}
        for script in dataset[target]:

            bsl_ms, bsl_elapsed, bsl_var = dataset[baseline][script][0]
            if bsl_ms != 0:    # Sanity check
                print "AAAAAAAAAAAAAAAAAAAAAHHHHRRR! ", bsl, ms

            for c, sample in enumerate(dataset[target][script]):
                if script not in experiment:
                    experiment[script] = []
                
                ms, elapsed, var = sample
                experiment[script].append((
                    ms,
                    elapsed/bsl_elapsed,
                    var
                ))
        return experiment

    #
    # Overhead
    """
    for script in setups['proxy1']:
        for c, sample in enumerate(setups['proxy1'][script]):
            if script not in experiments['overhead']:
                experiments['overhead'][script] = []
            
            ms, elapsed, var = sample
            bsl_ms, bsl_elapsed, bsl_var = setups['noproxy'][script][c]
            if bsl_ms != ms:    # Sanity check
                print "AAAAAAAAAAAAAAAAAAAAAHHHHRRR! ", bsl, ms

            experiments['overhead'][script].append((
                ms,
                elapsed/bsl_elapsed,
                var
            ))
    """
    experiments['overhead'] = baseline_it(setups, 'proxy1', 'noproxy')

    #
    # Latency absolute
    experiments['octuplets_absolute'] = setups['proxy1']
    experiments['dcsc_absolute']      = setups['proxy2']

    #
    # Latency relative
    experiments['octuplets_relative'] = baseline_it(setups, 'proxy1', 'proxy1')
    experiments['dcsc_relative']      = baseline_it(setups, 'proxy2', 'proxy2')

    return experiments

class Bypass_latency(Graph):
    """Basic plot of x,y values with lgnd and stuff."""

    def render(self, data, order=None, baseline=None, highest=None):

        """
        # With visualization
        viz_benchmarks   = ["Shallow Water 5k",  "N-body 5k",   "Heat Equation 5k",  "Black Scholes  10m"]
        viz_data = {}
        for script in viz_benchmarks:
            viz_data[script] = grouped[script]
        """

        experiments = bypass_latency(data)
        exp_labels = {
            'overhead':             'Proxy Overhead',
            'octuplets_absolute':   'Elapsed wall-clock as a function of latency - Octuplets',
            'octuplets_relative':   'Slowdown as a function network latency - Octuplets',
            'dcsc_absolute':        'Elapsed wall-clock as a function of latency - DCSC',
            'dcsc_relative':        'Slowdown as a function network latency - DCSC'
        }
        y_labels = {
            'overhead':             'Elapsed wall-clock time in seconds.',
            'octuplets_absolute':   'Elapsed wall-clock time in seconds.',
            'octuplets_relative':   'Slowdown',
            'dcsc_absolute':        'Elapsed wall-clock time in seconds.',
            'dcsc_relative':        'Slowdown'
        }
        app_map = {
            "Black Scholes 100m":   "Black Scholes",
            "Heat Equation 25k":    "Heat Equation",
            "N-body 25k":           "N-body",
            "Shallow Water 25k":    "Shallow Water"
        }

        for experiment in experiments:
            self.graph_title = exp_labels[experiment]
            self.yaxis_label = y_labels[experiment]

            self.prep()                         # Prep it / clear the drawing board
            dataset = experiments[experiment]
            for lgnd in dataset:

                if baseline:
                    self.yaxis_label='In relation to "%s"' % baseline

                """
                xticks(linear, linear)
                xlim(xmin=min(linear)*0.85, xmax=max(linear)*1.25)
                yticks(linear, linear)
                ylim(ymin=min(linear)*0.85, ymax=max(linear)*1.25)
                """
                if 'relative' in experiment:
                    ylim(ymin=0.9, ymax=3.0)
                else:
                    ylim(ymin=0.0, ymax=100.0)

                xs = [x for x, y, var in dataset[lgnd]]
                ys = [y for x, y, var in dataset[lgnd]]
                vs = [var for x, y, var in dataset[lgnd]]
                
                xticks([0, 50, 100, 150, 200], [0, 50, 100, 150, 200])
                plot(xs, ys, label=app_map[lgnd], marker='x')
                legend(loc="upper left")

            self.to_file(experiment)                # Spit them out to file

