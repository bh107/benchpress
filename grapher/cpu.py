import logging
from graph import *
import pprint
from matplotlib import rcParams

rcParams['axes.labelsize'] = 14
rcParams['axes.titlesize'] = 16
rcParams['xtick.labelsize'] = 14
rcParams['ytick.labelsize'] = 14
rcParams['legend.fontsize'] = 14
rcParams['font.family'] = 'serif'
rcParams['font.serif'] = ['Computer Modern Roman']
rcParams['text.usetex'] = True

from parser import standard_deviation, variance, avg

env_types = {
    "BH_VE_CPU_JIT_FUSION": int,
    "OMP_NUM_THREADS": int
}

engine_ord  = ['numpy', 'fusion', 'sij']
sample_size = 3
data_points = 6

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

    # Extract script size-args from cmd
    script_sizes = list(set([
        (result["script_alias"], cmd) for cmd in result["cmd"]
                                      for result in data
                                      if 'size' in cmd
    ]))
    if len(script_sizes) != len(script_aliases):
        print "NO GOOD! Erroneous benchmark results!"
    script_sizes = dict(script_sizes)

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
        "script_sizes": script_sizes,
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
            print("Result discarded elapsed time missing.")
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


    labels = ["numpy", "sij", "fusion"]

    structured = {}
    for data in data_flattened:

        script, bridge, engine, fusion, nthreads, average, var, std_dev = data
        if script not in structured:
            structured[script] = {
                'avg': {'fusion': [], 'sij': [], 'numpy': []},
                'dev': {'fusion': [], 'sij': [], 'numpy': []},
                'var': {'fusion': [], 'sij': [], 'numpy': []},

                'rel_first': {
                    'numpy':    {'fusion': [], 'sij': [], 'numpy': []},
                    'sij':      {'fusion': [], 'sij': [], 'numpy': []},
                    'fusion':   {'fusion': [], 'sij': [], 'numpy': []}
                },
                'rel_all': {
                    'numpy':    {'fusion': [], 'sij': [], 'numpy': []},
                    'sij':      {'fusion': [], 'sij': [], 'numpy': []},
                    'fusion':   {'fusion': [], 'sij': [], 'numpy': []}
                },
                'max': {},
                'min': {}
            }

        # Sort the results
        if 'fusion' in engine:
            structured[script]['avg']['fusion'].append(average)
            structured[script]['var']['fusion'].append(var)
            structured[script]['dev']['fusion'].append(std_dev)
        elif 'omp' in engine:
            structured[script]['avg']['sij'].append(average)
            structured[script]['var']['sij'].append(var)
            structured[script]['dev']['sij'].append(std_dev)
        else:
            # Create pseudo-samples for NumPy
            for _ in xrange(data_points):
                structured[script]['avg']['numpy'].append(average)
                structured[script]['var']['numpy'].append(var)
                structured[script]['dev']['numpy'].append(std_dev)

    discarded_results = {}
    for script in structured:   # Verify that we have all absolute numbers
        for label in labels:
            if len(structured[script]["avg"][label]) != data_points:
                if script not in discarded_results:
                    discarded_results[script] = []

                discarded_results[script].append(label)

    for script in discarded_results:    # Discard missing script
        print(
            "Dropping '%s' data-points are missing, culprit=%s." % (
            script,
            ','.join(discarded_results[script])
        ))
        del structured[script]

    for script in structured:       # Compute relative numbers, min, max

        for bsl_label in labels:    # To first value
            baseline = [structured[script]["avg"][bsl_label][0]]*data_points

            structured[script]['rel_first'][bsl_label] = {}

            for other_label in labels:
                other = structured[script]["avg"][other_label]
                structured[script]["rel_first"][bsl_label][other_label] = [
                    bsl / oth for bsl, oth in zip(baseline, other)
                ]

        for bsl_label in labels:    # To each value
            baseline = structured[script]["avg"][bsl_label]

            structured[script]['rel_all'][bsl_label] = {
                bsl_label: [1.0 for _ in baseline]
            }

            for other_label in (label for label in labels if label != bsl_label):
                other = structured[script]["avg"][other_label]
                structured[script]["rel_all"][bsl_label][other_label] = [
                    bsl / oth for bsl, oth in zip(baseline, other)
                ]

        for bsl_label in labels:    # Min, max speedup
            structured[script]['min'][bsl_label] = {}
            structured[script]['max'][bsl_label] = {}
            for other_label in labels:
                numbers = structured[script]['rel_first'][bsl_label][other_label]
                structured[script]['max'][bsl_label][other_label] = max(numbers)
                structured[script]['min'][bsl_label][other_label] = min(numbers)

    return structured

class Cpu(Graph):
    """Create a graph that illustrates scalabiltity."""

    def render_rel(self, data, parameters, script, rel_type, rel_engine):
        self.graph_title = script
        self.prep()

        min_threads     = 1
        max_threads     = max(parameters["env_values"]["OMP_NUM_THREADS"])
        linear          = list(brange(min_threads, max_threads))
        plot_count      = len(linear)

        legends = {'plots': [], 'legends': []}
        for i, engine in enumerate(engine_ord):
            legend_txt = r"%s: \textbf{%.1f} - \textbf{%.1f}" % (
                engine,
                data[script]['min'][rel_engine][engine],
                data[script]['max'][rel_engine][engine]
            )
            elapsed = data[script][rel_type][rel_engine][engine]
            p, = plot(
                linear,
                elapsed,
                "-*",
                label=engine,
                color=colors[i]
            )
            legends['plots'].append(p)
            legends['legends'].append(legend_txt)

        plot(linear, linear, "--", color='gray')  # Linear speedup

        script_max = 0.0
        for engine in engine_ord:
            for r_eng in engine_ord:
                script_max = max(script_max, data[script]['max'][r_eng][engine])

        #
        # Scale y-axis with a neat border
        ylabel(r"Speedup in relation to \textbf{%s}" % rel_engine)
        yscale("symlog")
        yt_range = list(brange(min_threads, max(script_max, max_threads)))
        yticks(yt_range, yt_range)
        ylim(
            ymin=min_threads*0.15,
            ymax=max(script_max, max_threads)*1.5
        )

        #
        # Scale x-axis with a neat border
        xlabel("Threads")
        xscale("symlog")
        xticks(linear, linear)
        xlim(xmin=min_threads*0.75, xmax=max_threads*1.5)

        #
        # Plot-legends and their positions
        lgd = legend(
            legends['plots'],
            legends['legends'],
            loc=3,
            ncol=3,
            bbox_to_anchor=(0.015, 0.95, 0.9, 0.102),
            borderaxespad=0.0,
        )

        t = title(script)
        t.set_y(1.05)
        
        tight_layout()                  # Spit them out to file
        return self.to_file("%s_%s_%s" % (script, rel_type, rel_engine))

    def render_absolute(self, data, parameters, script):

        self.graph_title = r"\textbf{%s}" % script
        self.prep()

        min_threads     = 1
        max_threads     = max(parameters["env_values"]["OMP_NUM_THREADS"])
        linear          = list(brange(min_threads, max_threads))
        plot_count      = len(linear)

        max_runtime = max(
            [max(data[script]['avg'][engine]) for engine in engine_ord]
        )

        elapsed = data[script]['avg']
        dev = data[script]['dev']
        var = data[script]['var']

        ind = range(data_points)                # Group start locations
        width = 0.3                             # Width of the bars
        group_width = width * (len(engine_ord)) # Width of the group
        group_center = group_width / 2.0        # Center of groups

        fig, ax = plt.subplots()

        rects = {}                          # Draw the bars
        for i, engine in enumerate(engine_ord):
            rects[engine] = ax.bar(
                [x+width*i for x in ind],
                elapsed[engine],
                width,
                color=colors[i],
                yerr=dev[engine]
            )

        # add some text for labels, title and axes ticks
        ax.set_ylabel(r"Elapsed wall-clock time in \textbf{seconds}")
        ax.set_title(script)
        ax.set_xticks([x+group_center for x in ind])
        ax.set_xticklabels([str(x) for x in linear])

        ax.legend(
            [rects[engine] for engine in engine_ord],
            [engine for engine in engine_ord],
            loc=3,
            ncol=3,
            bbox_to_anchor=(0.01, 0.95, 0.9, 0.102),
            borderaxespad=0.0
        )

        def autolabel(rectangles):
            # attach some text labels
            for rect in rectangles:
                height = rect.get_height()
                ax.text(
                    rect.get_x()+rect.get_width()/2.,
                    1.015 * height,
                    '%d'%int(height),
                    ha='center',
                    va='bottom'
                )

        for engine in engine_ord:
            autolabel(rects[engine])

        xlabel("Threads")
        t = title(script)
        t.set_y(1.05)

        ylim(ymin=0, ymax=max_runtime*1.13)

        tight_layout()                  # Spit them out to file
        return self.to_file("%s_%s" % (script, 'absolute'))

    def render_html(self, filenames, meta, parameters):

        scripts = [script for script in filenames]
        scripts.sort()

        links = []
        for script in scripts:
            links.append('<a href="#%s">%s</a>' % (
                script.replace(" ", ""),
                script
            ))

        doc = """<html>
        <head>
        <title>Benchmark Suite CPU Results - REV: %s</title>
        <style>
        body {
          padding: 0;
          margin: auto;
          height: 1400px;
          text-align: center;
        }
        html {
          background: #400101;
        }
        body {
          padding: 0;
          width: 960px;
          background: #bf0404;
        }
        #page {
          min-height: 100%;
          height: 100%;
          position: relative;
        }
        #main {
          padding-bottom: 150px;
        }
        /* HEADER */
        #header {
          /* BASE CODE */
          top: 0px;
            height: 50px;
          width: 100%;
          /* STYLING */
          background: #590202;
          color: #f2f2f2;
          display: table;
          position: absolute;
        }
        /* NAVBAR */
        #navbar {
          /* BASE CODE */
          position: fixed;
             margin-top: 50px;    
          z-index: 10;
          width: 960px;
          height: 10px;
          /* STYLING */
          background: yellow;
        }
        /* CONTENT */
        #main {
          padding-top: 20px;
        }
        /* FOOTER */
        #footer {
          /* BASE CODE */
          position: absolute;
          width: 100%;
          bottom: 0;
          height: 150px;
          /* STYLING */
          background: #590202;
          display: table;
        }
        </style>
        </head>
        <body>
        <div id="page">
          <div id="header">
          <h1>Benchmark Suite CPU</h1>
          <h2>Repos revision: %s</h2>
          </div>
          <div id="navbar">
          __LINKS__
          </div>
          <div id="main">
          <h2>Results</h2>
          __RESULTS__
          </div>
          <div id="footer"></div>
        </div>
        </body>
        </html>""" % (meta["rev"], meta["rev"])

        doc = doc.replace("__LINKS__", " | ".join(links))

        results = ""

        for script in scripts:
            results += '<h3 id="%s">%s %s</h3>' % (
                script.replace(" ", ""),
                script,
                parameters["script_sizes"][script]
            )
            results += "<table>"
            results += """
            <tr>
            <td><img src="%s" /></td>
            <td><img src="%s" /></td>
            </tr>
            <tr>
            <td><img src="%s" /></td>
            <td><img src="%s" /></td>
            </tr>
            """ % (
                filenames[script][0].replace(self.output+os.sep, ""),
                filenames[script][1].replace(self.output+os.sep, ""),
                filenames[script][2].replace(self.output+os.sep, ""),
                filenames[script][3].replace(self.output+os.sep, "")
            )
            results += "</table>\n"

        html = doc.replace("__RESULTS__", results)
        with open('%s%scpu.html' % (self.output, os.sep), 'w') as fd:
            fd.write(html)

    def render(self, raw, data, processed=None, params=None):

        meta = raw["meta"]
        raw = raw["runs"]

        data_flattened = flatten(raw)
        parameters = extract_parameters(raw)
        data = restructure(data_flattened)

        graph_filenames = {}
        for script in data:
            graph_filenames[script] = []
            fns = self.render_absolute(data, parameters, script)    # Absolute
            graph_filenames[script].extend(fns)
            for engine in engine_ord:                               # Relative
                fns = self.render_rel(
                    data,
                    parameters,
                    script,
                    'rel_first',
                    engine
                )
                graph_filenames[script].extend(fns)

        self.render_html(graph_filenames, meta, parameters)          # HTML
