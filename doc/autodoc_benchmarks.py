#!/usr/bin/env python
import argparse
import Cheetah
import fnmatch
import pprint
import os
import re

lang_labels = {
    'c':    'C',
    'cpp':  'C++',
    'py':   'Python'
}
lang_order  = ['py', 'c', 'cpp']
ignore      = ["_utils", "_doc"]

def pretty_name(text):
    """Returns a rewrite like: "snakes_and_ladders" -> "Snakes And Ladders"."""

    return text.replace('_', ' ').title()

def implementations(pathi=".."+os.sep+".."):
    """Walks through the filesystem looking for benchmark implementations."""

    meta = {
        "langs": [], "tools":[], "benchs":[],
        "nlangs": 0, "ntools": 0, "nbenchs": 0,
        "tools_by_lang": {},
        "ntools_by_lang": {},
        "tool_to_lang": {}
    }
    benchmarks = {}

    for root, dirnames, filenames in os.walk("../benchmarks/"):
        if [x for x in ignore if x in root]:    # Ignore some...
            continue

        for filename in filenames:              # Group the rest
            match = re.match(".*\.((cpp)|(py)|(c)$)", filename)
            if match:
                dirs        = [x for x in root.split(os.sep) if x not in ["..", "benchmarks"]]
                benchmark   = dirs[0]
                tool        = dirs[1]
                lang        = match.group(1)

                # Check that the basename matches the benchmark
                bn = ''.join(os.path.basename(filename).split('.')[:-1])
                if not bn == benchmark:
                    continue

                if benchmark not in benchmarks:
                    benchmarks[benchmark] = {}
                    meta["benchs"].append(benchmark)
                    meta["nbenchs"] += 1

                if lang not in benchmarks[benchmark]:
                    benchmarks[benchmark][lang] = {}
                    if lang not in meta["langs"]:
                        meta["langs"].append(lang)
                        meta["nlangs"] += 1

                if tool not in benchmarks[benchmark][lang]:
                    benchmarks[benchmark][lang][tool] = os.sep.join(dirs)+os.sep+filename
                    if tool not in meta["tools"]:
                        meta["tools"].append(tool)
                        meta["ntools"] += 1

                if lang not in meta["tools_by_lang"]:
                    meta["tools_by_lang"][lang] = []
                    meta["ntools_by_lang"][lang] = 0

                if tool not in meta["tools_by_lang"][lang]:
                    meta["tools_by_lang"][lang].append(tool)
                    meta["tools_by_lang"][lang].sort()
                    meta["ntools_by_lang"][lang] += 1

                if tool not in meta["tool_to_lang"]:
                    meta["tool_to_lang"][tool] = lang

    meta["benchs"].sort()

    return {"__meta__": meta, "impls": benchmarks}

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
                    entry.append("+")
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

    def draw_sep(self, widths=None):
        if not widths:
            widths = self.col_widths

        seps = []
        for cidx, cwidth in enumerate(widths):
            seps.append("-"*(cwidth+2))
        return "+%s+" % "+".join(seps)

    def render(self):

        rows = []
        for row in self.rows:
            rows.append(self.draw_sep())
            rows.append(self.draw_row(row))
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

def benchmark_matrix(benchmarks):
    rows = flatten(benchmarks)

    rows.insert(0, [" "]+[ " ".join(tool.split('_')[1:]).title() for lang in lang_order for tool in benchmarks["__meta__"]["tools_by_lang"][lang] ])
    rows = modify_column(section_ref, rows)
    table= RstTable([], rows)

    header_row      = [" "]
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
        header_row.append(lang)
        header_widths.append(width)
    
    row = []
    for col, width in zip(header_row, header_widths):
        row.append(col.ljust(width))
    
    matrix = table.draw_sep(header_widths)+"\n"
    matrix += table.draw_row(header_row, header_widths)+"\n"
    matrix += table.render()

    return matrix

def sections(benchmarks):

    meta = benchmarks["__meta__"]
    benchs = benchmarks["impls"]

    sections = ""
    for bench_lbl in meta["benchs"]:
        section_title = pretty_name(bench_lbl)
        section_label = bench_lbl
        section = [
            "",
            "",
            ".. _%s:" % bench_lbl,
            "",
            section_title,
            "="*len(section_title),
            ""
        ]
        sections += "\n".join(section)

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
                src_path = os.sep.join([
                    "..","..","benchmarks"
                ]+bench[lang][tool].split(os.sep))
                subsection.append("\n.. literalinclude:: %s" % src_path)
                subsection.append("   :language: %s" % lang)
                subsection.append("")
                sections += "\n".join(subsection)

    return sections

def main():
    benchmarks = implementations()
  
    print ""
    print "=========="
    print "Benchmarks"
    print "=========="
    print ""
    print benchmark_matrix(benchmarks)
    print ""
    print sections(benchmarks)

if __name__ == "__main__":
    main()
