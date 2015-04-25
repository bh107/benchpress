#!/usr/bin/env python
# -*- coding: utf8 -*-
import pprint
import os
from benchpress.cpu_result_parser import flatten, group_by_script, datasetify, order_idents, ident_ordering
from benchpress.cpu_result_parser import datasets_rename, ident_mapping, extract_parameters, datasets_baselinify
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

    def html_index(self, raw, datasets, paths, parameters):

        meta = raw["meta"]
        scripts = [script for script in datasets]
        scripts.sort()

        table = "<center><table><tr>" 

        unordered_idents = sorted(list(set([ident for script in scripts for ident in datasets[script]])))
        idents = order_idents(unordered_idents, ident_ordering)

        for idx, bsl_ident in enumerate(idents):
            table += "<td>"
            table += """
            <table style="border: 1px solid gray;">
            <thead>
            <tr>
            <td></td>
            """
            for ident in idents:
                table += """
                <td colspan="2" style="text-align: center;">%s</td>
                """ % ident
            table += """
            </tr>
            </thead>
            """

            table += "<colgroup>"
            table += "<col>" * (len(idents)*2+1)
            table += "</colgroup>"
            table += """
            <tbody>
            """

            for script in scripts:
                
                table += """
                <tr>
                <td>%s</td>
                """ % script 
                (global_max, data) = datasets_baselinify(datasets[script])
                for ident in idents:
                    smax = data[bsl_ident][ident]['max']
                    smin = data[bsl_ident][ident]['min']

                    table += """
                    <td>%.1f</td>
                    <td style="text-align: right;">%.1f</td>
                    """ % (smin, smax)
                table += """
                </tr>"""
            table += """
            </tbody>
            <tfoot>
            <td colspan="%s" style="text-align: center;">%s</td>
            </tfoot>
            </table>""" % (
                len(idents)*2+1,
                "<b>Min/Max speedup in relation to %s</b>" % bsl_ident
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
            results += '<div class="anchor" id="%s"></div><h3>%s (%s)</h3>' % (
                script.replace(" ", ""),
                script,
                parameters["script_args"][script]
            )
            results += "<table>"
            results += "<tr>"

            for pidx, path in enumerate(paths[script]):
                results += """<td><img src="%s" /></td>""" % os.path.basename(path)
            results += "</tr>"
            results += "</table>\n"

        html = doc.replace("__RESULTS__", results)
        with open('%s%sindex.html' % (self.output_path, os.sep), 'w') as fd:
            fd.write(html)

    def render(self, raw, data, order, baseline):

        parameters = extract_parameters(raw)                # Extract parameters
        
        runs_flattened = flatten(raw["runs"])               # Extract datasets
        runs_grouped = group_by_script(runs_flattened)
        datasets = datasets_rename(
            datasetify(runs_grouped),
            ident_mapping
        )

        paths = {} # script_alias -> [fn1, ..., fnn]
        scripts = sorted([script for script in datasets])
        for script in scripts:
            paths[script] = []  

            paths[script] += Absolute(                      # Absolute graphs
                title=script,
                output_path=self.output_path
            ).render(datasets[script])

            paths[script] += Relative(                      # Speedup graphs
                title=script,
                output_path=self.output_path
            ).render(datasets[script])
                                        
        self.html_index(raw, datasets, paths, parameters)   # Index them
