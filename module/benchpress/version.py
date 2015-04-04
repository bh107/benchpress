import inspect
import pprint
import os
import re

APP_NAME = 'benchpress'
APP_VERSION = '0.9'

ignore      = ["_utils", "_doc"]

def module_path():
    return os.path.dirname(__file__)

def get_paths():
    """Get a dict of paths for the various things in benchpress."""

    paths = {                                   # Construct the path dict
        'mod': "",
        'mod_parent': "",
        'docsrc': "",
        'benchmarks': "",
        'suites': "",
        'hooks': "",
        'commands': "" 
    }

    mod = module_path()
    mod_parent = os.sep.join(mod.split(os.sep)[:-1])
    dirs = mod.split(os.sep) 

    paths["mod"] = mod
    paths["mod_parent"] = mod_parent

    if len(dirs) > 2             and \
        dirs[-1] == "benchpress" and \
        dirs[-2] == "module":           # Running from clone/tarball
        root = os.sep.join(dirs[:-2])
        paths["docsrc"] = os.sep.join([root, "doc"])
        paths["benchmarks"] = os.sep.join([root, "benchmarks"])
        paths["suites"] = os.sep.join([root, "suites"])
        paths["hooks"] = os.sep.join([root, "hooks"])
        paths["commands"] = os.sep.join([root, "bin"])
    else:                               # Running from pip-install
        while(len(dirs) > 2):
            dirs.pop()
            path = os.sep.join(dirs)
            ls = os.listdir(path)
            if 'share' in ls and 'bin' in ls:
                #paths["docsrc"] = Doc source is not installed
                paths["benchmarks"] = os.sep.join([path, "benchmarks"])
                paths["suites"] = os.sep.join([path, "suites"])
                paths["hooks"] = os.sep.join([path, "bin"])
                paths["commands"] = os.sep.join([path, "bin"])
                break
    for entity in paths:                # Check that they actually exist
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

