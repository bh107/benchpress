#!/usr/bin/env python
import argparse
import textwrap
import Cheetah
import fnmatch
import pprint
import os
import re

from benchpress.version import implementations

lang_labels = {
    'c':    'C',
    'cpp':  'C++',
    'py':   'Python',
    'cs':   'C#'
}
lang_pygment = {
    'c':    'c',
    'cpp':  'cpp',
    'py':   'python',
    'cs':   'csharp'
}
lang_order  = ['py', 'c', 'cpp', 'cs']

benchmarks_relpath = os.sep.join(["..", "..", "..", "benchmarks"])

def pretty_name(text):
    """Returns a rewrite like: "snakes_and_ladders" -> "Snakes And Ladders"."""

    return text.replace('_', ' ').title()

def flatten(benchmarks):
    """Flattens the benchmarks into a specific ordering."""

    meta    = benchmarks["__meta__"]
    impls   = benchmarks["impls"]
    flat    = []

    for bench in meta["benchs"]:
        entry = [bench]

        for lang in lang_order:
            for tool in meta["tools_by_lang"][lang]:
                if lang in impls[bench] and tool in impls[bench][lang]:
                    #entry_info = "+"
                    entry_info = section_ref("* <%s_%s>" % (bench, tool))
                    if impls[bench][lang][tool]["issues"]:
                        entry_info += " [ISU]_"
                    if impls[bench][lang][tool]["bohrium"]:
                        entry_info += " [BH]_"
                    if not impls[bench][lang][tool]["dogma"] and tool == "python_numpy":
                        entry_info += " [IBNP]_"
                    entry.append(entry_info)
                else:
                    entry.append(" ")
        flat.append(entry)

    return flat

class RstTable(object):

    def __init__(self, headers, rows):
        self.headers = headers
        self.rows = rows

        self.col_widths = [0]*len(rows[0])  # Determine widts of columns
        for ridx, row in enumerate(rows):
            for cidx, col in enumerate(row):
                col_len = len(col)
                if col_len > self.col_widths[cidx]:
                    self.col_widths[cidx] = col_len

    def draw_row(self, row, widths=None):
        if not widths:
            widths = self.col_widths

        cols = []
        for cidx, cwidth in enumerate(widths):
            cols.append(row[cidx].ljust(cwidth))
        return "| %s |" % " | ".join(cols)

    def draw_sep(self, widths=None, sep='-'):
        if not widths:
            widths = self.col_widths

        seps = []
        for cidx, cwidth in enumerate(widths):
            seps.append(sep*(cwidth+2))
        return "+%s+" % "+".join(seps)

    def render(self):
        first = True 
        rows = []
        sepper = "-"
        for row in self.rows:
            rows.append(self.draw_sep(sep=sepper))
            rows.append(self.draw_row(row))
            stuffing = [entry.lower() for entry in row]
            if ("numpy" in stuffing or "python" in stuffing) and first:
                sepper = "="
                first = False
            else:
                sepper = "-"

        rows.append(self.draw_sep())

        return "\n".join(rows)

def modify_column(func, rows):
    """Apply 'func' to the first column in all of the supplied rows."""

    delta = []
    for columns in rows:
        delta.append([func(columns[0])] + columns[1:])
    return delta

def section_ref(text):
    
    return ":ref:`%s`" % text if text.strip() else text

def benchmark_index(benchmarks):
    rows = flatten(benchmarks)

    tool_header = [" "]+[ " ".join(tool.split('_')[1:]).title() for lang in lang_order for tool in benchmarks["__meta__"]["tools_by_lang"][lang] ]

    rows.insert(0, tool_header)
    rows = modify_column(section_ref, rows)

    rerow = []
    for ridx, row in enumerate(rows):
        rerow.append(row)   
        if ((ridx+1) % 15) == 0:
            rerow.append(tool_header)
    rows = rerow

    table= RstTable([], rows)

    header_row      = ["%d Benchmarks "% benchmarks["__meta__"]["nbenchs"]]
    header_widths   = [table.col_widths[0]]

    cidx = 1
    for lang in lang_order:
        ntools = benchmarks["__meta__"]["ntools_by_lang"][lang]
        width = 0
        if ntools>1:
            width = (ntools-1)*3
        for idx in xrange(cidx, cidx+ntools):
            width += table.col_widths[idx]
        cidx += ntools
        header_row.append(lang_labels[lang])
        header_widths.append(width)
    
    row = []
    for col, width in zip(header_row, header_widths):
        row.append(col.ljust(width))
    
    matrix = table.draw_sep(header_widths)+"\n"
    matrix += table.draw_row(header_row, header_widths)+"\n"
    matrix += table.render()

    matrix += """

.. [ISU] The implementation has issues... such as not using of Benchpress, segfaults, or does not run with Bohrium.
.. [BH] The implementation makes use of Bohrium specific features, which means that Bohrum is required to run it.
.. [IBNP] The implementation does `import bohrium as np`, which breaks the Bohrium dogma "High-Performance NumPy without changing a single line of code.
    """

    return matrix

def benchmark_sections(benchmarks):

    meta = benchmarks["__meta__"]
    benchs = benchmarks["impls"]

    sections = {}
    for bench_lbl in meta["benchs"]:
        section = ""
        section_title = pretty_name(bench_lbl)
        section_label = bench_lbl
        section = "\n".join([
            "",
            "",
            ".. _%s:" % bench_lbl,
            "",
            section_title,
            "="*len(section_title),
            ""
        ])

        bench_path = os.sep.join([benchmarks_relpath, bench_lbl])

        # Add readme.rst to the section
        bench_readme_path = os.sep.join([bench_path, "readme.rst"])
        #print bench_readme_path[4:]
        if os.path.exists(bench_readme_path[4:]):
            section += "\n.. include:: %s\n" % bench_readme_path

        bench = benchs[bench_lbl]
        for lang in (lang for lang in lang_order if lang in bench):
            tools = bench[lang].keys()
            tools.sort()
            for tool in tools:
                bench_tool_lbl = "%s_%s" % (bench_lbl, tool)
                subsection_title = pretty_name(tool)
                subsection = [
                    "",
                    "",
                    ".. _%s:" % bench_tool_lbl,
                    "",
                    subsection_title,
                    "-"*len(subsection_title),
                    ""
                ]
                # Include issues
                issues_path = bench[lang][tool]["issues"]
                if issues_path:

                    issues_txt = []
                    for line in open(issues_path).readlines():
                        issues_txt.append(" "*4+line)
                    issues_txt = "\n".join(issues_txt)

                    subsection.append("\n.. error:: There are issues with the implementation.\n\n%s"%issues_txt)

                # Include bohrium specifics
                bohrium_path = bench[lang][tool]["bohrium"]
                if bohrium_path:
                    bohrium_txt = []
                    for line in open(bohrium_path).readlines():
                        bohrium_txt.append(" "*4+line)
                    bohrium_txt = "\n".join(bohrium_txt)

                    subsection.append("\n.. note:: There is Bohrium-specific code this implementation, this means Bohrium is required to run it.\n\n%s"%bohrium_txt)

                # Include the source
                src_path = os.sep.join([benchmarks_relpath] + bench[lang][tool]['src'].split(os.sep))
                subsection.append("\n.. literalinclude:: %s" % src_path)
                subsection.append("   :language: %s" % lang_pygment[lang])
                subsection.append("")
                section += "\n".join(subsection)

        sections[bench_lbl] = section

    return sections

def main():
    benchmarks = implementations(".."+os.sep+"benchmarks")
  
    index = benchmark_index(benchmarks)
    with open(os.sep.join(["source", "benchmarks", "autodoc_index.rst"]), 'w') as fd:
        fd.write("==========\n")
        fd.write("Benchmarks\n")
        fd.write("==========\n")
        fd.write("\n")
        fd.write(index)

    sections = benchmark_sections(benchmarks)
    bench_lbl_listing = []
    bench_labels = [lbl for lbl in sections]
    bench_labels.sort()
    for bench_lbl in bench_labels:
        with open(os.sep.join(["source", "benchmarks", "%s.rst" % bench_lbl]), 'w') as fd:
            fd.write(sections[bench_lbl])
            bench_lbl_listing.append(bench_lbl)

if __name__ == "__main__":
    main()
