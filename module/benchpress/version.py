import inspect
import os
import re

APP_NAME = 'benchpress'
APP_VERSION = '0.7'

ignore      = ["_utils", "_doc"]

def module_path():
    return os.path.dirname(__file__)

def get_paths():
    """Get a dict of paths for the various things in benchpress."""

    home = module_path()
    dirs = home.split(os.sep) 

    share_path = os.sep.join(dirs[:-1])         # When running from checkout
    bin_path = share_path
    from_checkout = len(dirs) > 2 and \
                    dirs[-1] == "benchpress" and \
                    dirs[-2] == "benchpress"

    # Find the share folder and bin folders when not running from checkout
    while(len(dirs) > 2 and not from_checkout):
        dirs.pop()
        path = os.sep.join(dirs)
        ls = os.listdir(path)
        if 'share' in ls and 'bin' in ls:
            share_path = os.sep.join([path, "share", "benchpress"])
            bin_path = os.sep.join([path, "bin"])
            break
    
    paths = {                                   # Construct the path dict
        'module': home,
        'benchmarks': os.sep.join([share_path, "benchmarks"]),
        'suites': os.sep.join([share_path, "suites"]),
        'hooks': bin_path,
        'bins': bin_path
    }

    for entity in paths:                        # Validate it
        if not os.path.exists(paths[entity]):
            raise IOError("Path for %s (%s) does not exist" % (entity, paths[entity]))

    return paths

def implementations(search_path=None):
    """Walks through the filesystem looking for benchmark implementations."""

    paths = get_paths()
    if not search_path:
        search_path = paths["benchmarks"]

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

