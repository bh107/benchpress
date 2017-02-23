import numpy as np
from benchpress import result_parser
from graph import Graph, filter_list, translate_dict
import json
import re

def get_stack_name(stack):

    names = [comp[0] for comp in stack][1:]
    ret = ""
    for name in names:
        ret += "%s/"%name
    return ret[:-1]


class Row_per_script(Graph):

    def render(self):

        raw = json.load(open(self.args.results))
        data = result_parser.from_file(self.args.results)

        # Extract result data
        res = {}
        scripts = list(set([script for script, _, _ in data]))
        comps = set()
        for s in scripts:
            for script, _, r in data:
                if script == s:
                    comp = get_stack_name(r['stack'])
                    try:
                        avg = result_parser.avg(r[self.args.data_to_display])
                        err = result_parser.standard_deviation(r[self.args.data_to_display])
                        value = (avg, err)
                    except KeyError:
                        print "WARNING - couldn't find '%s' in output of '%s'"%(self.args.data_to_display, comp)
                        value = (0,0)
                    comps.add(comp)
                    if s in res:
                        res[s][comp] = value
                    else:
                        res[s] = {comp: value}

        # Filter scripts and component stacks
        comps = filter_list(comps, self.args.stacks_to_display, self.args.stacks_not_to_display)
        scripts = filter_list(scripts, self.args.scripts_to_display, self.args.scripts_not_to_display)
        comps.sort()
        scripts.sort()

        # Get translation of components
        comp_dict = translate_dict(comps, self.args.stack_map)


        table = """<center><table style="border: 1px solid gray;">"""
        table += """
        <thead>
        <tr>
        <td></td>
        """
        for stack in comps:
            table += """
            <td colspan="1" style="text-align: center;">%s</td>
            """ % comp_dict[stack]
        table += """
        </tr>
        </thead>
        """

        table += "<colgroup>"
        table += "<col>" * (len(comps) + 1)
        table += "</colgroup>"
        table += """
        <tbody>
        """

        for script in scripts:
            table += """
            <tr>
            <td>%s</td>
            """ % script

            for stack in comps:
                avg, err = res[script][stack]
                table += """
                <td style="text-align: right;">%4.1f</td>
                """ % (avg)

            table += """</tr>"""
        table += """
        </tbody>
        <tfoot>
        <td colspan="%s" style="text-align: center;">%s</td>
        </tfoot>
        </table>""" % (
            len(comps)+1,
            "<b>Wall clock</b>"
        )
        table += "</td>"
        table += "</tr></table></center>"

        doc = """<html>
        <head>
        <title>__TITLE__</title>
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
        </style>
        </head>
        <body>
        <div id="header">
        <h1>__TITLE__</h1>
        </div>
        __TABLE__
        </div>
        </div>
        </body>
        </html>"""

        doc = doc.replace("__TABLE__", table)
        doc = doc.replace("__TITLE__", self.args.title)
        print doc