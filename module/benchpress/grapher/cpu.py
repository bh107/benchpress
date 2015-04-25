#!/usr/bin/env python
# -*- coding: utf8 -*-
import pprint
from benchpress.cpu_result_parser import flatten, group_by_script, datasetify
from benchpress.cpu_result_parser import datasets_rename, ident_mapping, extract_parameters
from graph import Grapher, Graph, texsafe, brange, pylab, matplotlib
from relative import Relative
from absolute import Absolute

class Cpu(Grapher):
    """Create a graph that illustrates scalabiltity."""

    def __init__(
        self, output_path, file_formats, postfix,
        graph_title, xaxis_label,  yaxis_label
    ):
        super(Cpu, self).__init__(
            output_path, file_formats, postfix,
            graph_title, xaxis_label, yaxis_label
        )

    def render_html(self, filenames, data, meta, parameters):

        scripts = [script for script in filenames]
        scripts.sort()

        table = "<center><table><tr>" 

        for i, bsl_engine in enumerate(engine_ord):
            table += "<td>"
            table += """
            <table style="border: 1px solid gray;">
            <thead>
            <tr>
            <td></td>
            """
            for engine in engine_ord:
                table += """
                <td colspan="2" style="text-align: center;">%s</td>
                """ % engine
            table += """
            </tr>
            </thead>
            """

            table += "<colgroup>"
            table += "<col>" * (len(engine_ord)*2+1)
            table += "</colgroup>"
            table += """
            <tbody>
            """

            for script in scripts:
                
                table += """
                <tr>
                <td>%s</td>
                """ % script 
                for engine in engine_ord:
                    smax = data[script]['max'][bsl_engine][engine]
                    smin = data[script]['min'][bsl_engine][engine]

                    table += """
                    <td>%.1f</td>
                    <td style="text-align: right;">%.1f</td>
                    """ % (
                        smin,
                        smax
                    )
                table += """
                </tr>"""
            table += """
            </tbody>
            <tfoot>
            <td colspan="%s" style="text-align: center;">%s</td>
            </tfoot>
            </table>""" % (
                len(engine_ord)*2+1,
                "<b>Min/Max speedup in relation to %s</b>" % bsl_engine
            )
            table += "</td>"
        table += "</tr></table></center>"

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
            text-align: center;
        }
        col:nth-child(2n+3) {background: #CCC}
        h3 {
            margin: 0;
        }
        .anchor {
            margin-bottom: 80px;
        }
        #header {
            margin-top: 80px;
            background-color: white;
        }
        #navbar {
            position: fixed;
            z-index: 10;
            top: 0px;
            background-color: white;
            padding: 20px;
            margin: auto;
        }
        </style>
        </head>
        <body>

        <div id="navbar">
        __LINKS__
        </div>
 
        <div id="header">
        <h1>Benchmark Suite CPU</h1>
        <h2>Repos revision: %s</h2>
        </div>       
        <h2>Results</h2>
        __TABLE__
        __RESULTS__
        </div>

        </div>
        </body>
        </html>""" % (meta["rev"], meta["rev"])

        doc = doc.replace("__TABLE__", table)
        doc = doc.replace("__LINKS__", " | ".join(links))

        results = ""
        for script in scripts:
            results += '<div class="anchor" id="%s"></div><h3>%s %s</h3>' % (
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
                os.path.basename(filenames[script][0]),
                os.path.basename(filenames[script][1]),
                os.path.basename(filenames[script][2]),
                os.path.basename(filenames[script][3])
            )
            results += "</table>\n"

        html = doc.replace("__RESULTS__", results)
        with open('%s%sindex.html' % (self.output, os.sep), 'w') as fd:
            fd.write(html)

    def render(self, raw, data, order, baseline):

        # Extract parameters to use for bounds-checking
        parameters = extract_parameters(raw)

        # Extract datasets
        runs_flattened = flatten(raw["runs"])
        runs_grouped = group_by_script(runs_flattened)
        datasets = datasets_rename(
            datasetify(runs_grouped),
            ident_mapping
        )

        scripts = sorted([script for script in datasets])
        for script in scripts:
            Relative(title=script).render(datasets[script])
            Absolute(title=script).render(datasets[script])
