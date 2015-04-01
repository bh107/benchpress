import inspect
import os

APP_NAME = 'benchpress'
APP_VERSION = '0.5'

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

