from graph import *
import pprint

def brange(begin, end):
    c = i = begin
    while i <= end:
        yield i
        i = 2**c
        c += 1

class Cpu(Graph):
    """Create a graph that illustrates scalabiltity."""

    def render(self, raw, processed=None, params=None):

        min_threads     = 1
        max_threads     = 32
        linear          = list(brange(min_threads, max_threads))
        plot_count      = len(linear)

        engine_lbls = {
            'N/A':      'NumPy',
            'omp':      'BH/T+V',
            'fusion':   'BH/T+V+F'
        }
        engine_ord  = ['NumPy', 'BH/T+V', 'BH/T+V+F']

        #
        #   Grab the data from the raw json
        scripts = set([])
        engines = set([])
        data = {}

        #
        # Grab the Baselines
        bsl_enable  = True
        bsl_engine  = 'omp_01'
        bsl_elapsed = {}
        
        for script, bridge, node, engine, samples in raw:
            if bsl_engine == engine and script not in bsl_elapsed:
                elapsed = samples['elapsed']
                bsl_elapsed[script] = sum(elapsed)/float(len(elapsed))

        #
        # Extract remaining
        for script, bridge, node, engine, samples in raw:
            scripts.add(script)
            engines.add(engine)

            if script not in data:
                data[script] = {}

            data[script][engine] = sum(samples["elapsed"]) / len(samples["elapsed"])
        scripts = list(scripts); scripts.sort()
        engines = list(engines); engines.sort()

        #
        # Group it by benchmark and "NumPy / Fusion / OMP"
        #
        # Maps "N/A" to NumPy, "fusion_1" to "fusion" and orders
        # by thread-count.
        plots = {}
        for script in scripts:
            plots[script] = {}
            for engine in engines:
                
                # Compute relative value when using a baseline
                if bsl_enable:
                    value = bsl_elapsed[script] / data[script][engine]
                else:
                    value = data[script][engine]

                if engine == 'N/A':
                    plots[script][engine_lbls[engine]] = zip(
                        linear,
                        [value]*plot_count
                    )
                else:
                    label, nr = engine.split('_')
                    label = engine_lbls[label]

                    if label not in plots[script]:
                        plots[script][label] = []

                    plots[script][label].append((
                        int(nr),
                        value)
                    )

        #
        # Data is stored as [(1, time), (2, time), (4, time), ... , (32, time)]
        # Where "numbers" are thread-crount and  "time" is elapsed wall-clock.
        #
        for script in plots:
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
