import os
import re

ignore      = ["_utils", "_doc"]

def implementations(search_path=".."+os.sep+"benchmarks"):
    """Walks through the filesystem looking for benchmark implementations."""

    meta = {
        "langs": [], "tools":[], "benchs":[],
        "nlangs": 0, "ntools": 0, "nbenchs": 0,
        "tools_by_lang": {},
        "ntools_by_lang": {},
        "tool_to_lang": {}
    }
    benchmarks = {}

    for root, dirnames, filenames in os.walk(search_path):
        if [x for x in ignore if x in root]:    # Ignore some...
            continue

        for filename in filenames:              # Group the rest
            match = re.match(".*\.((cpp$)|(py$)|(c$)$)", filename)
            if match:
                dirs        = [x for x in root.split(os.sep) if x not in search_path.split(os.sep)]
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
                    dogma_rst_path      = os.sep.join([search_path, benchmark, tool, "dogma.rst"])
                    bohrium_rst_path    = os.sep.join([search_path, benchmark, tool, "bohrium.rst"])
                    issues_rst_path     = os.sep.join([search_path, benchmark, tool, "issues.rst"])
                    benchmarks[benchmark][lang][tool] = {
                        'src':      os.sep.join(dirs)+os.sep+filename,
                        'dogma':    dogma_rst_path if os.path.exists(dogma_rst_path) else "",
                        'bohrium':  bohrium_rst_path if os.path.exists(bohrium_rst_path) else "",
                        'issues':   issues_rst_path if os.path.exists(issues_rst_path) else "",
                    }
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

