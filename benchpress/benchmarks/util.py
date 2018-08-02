from __future__ import print_function
import argparse
import time
import sys
import gzip
import operator
import functools

# In order to support runs without bohrium installed, we need some import hacks. The result is:
#   * `np` will point to either Bohrium or Numpy
#   * `numpy` will point to Numpy
#   * `bohrium` will point to either Bohrium or None
import numpy as np

try:
    import numpy_force as numpy

    bh_is_loaded_as_np = True
except ImportError:
    import numpy as numpy

    bh_is_loaded_as_np = False

try:
    import bohrium
except ImportError:
    bohrium = None


class VisualArgs:
    def __init__(self, args):
        self.count = -1
        self.rate = args.visualize_rate
        self.param = args.visualize_param
        self.trace = {'org': [], 'zip': []}
        self.trace_fname = args.visualize_trace  # When None, no tracing
        self.dry = args.visualize_dry


class Benchmark:
    """
    Helper class to aid running Python/NumPy programs with and without Bohrium.

    Use it to sample elapsed time using: start()/stop()
    Pretty-prints results using pprint().
    start()/stop() will send flush signals to npbackend, ensuring that only
    the statements in-between start() and stop() are measured.
    """

    def __init__(self, description, size_pattern):
        self._elapsed = 0.0  # The quantity measured
        self._script = sys.argv[0]  # The script being run

        # Construct argument parser
        p = argparse.ArgumentParser(description=description)
        p.add_argument('size',
                       metavar=size_pattern,
                       help="Tell the script the size of the data to work on."
                       )
        p.add_argument('--dtype',
                       choices=["uint8", "float32", "float64"],
                       default="float64",
                       help="Tell the the script which primitive type to use."
                            " (default: %(default)s)"
                       )
        p.add_argument('--seed',
                       default=42,
                       help="The seed to use when using random data."
                       )
        p.add_argument('--inputfn',
                       default=None,
                       help="Input file to use as data.",
                       metavar="FILE",
                       type=str,
                       )
        p.add_argument('--outputfn',
                       default=None,
                       help="Output file to store results in (.npz extension will "
                            "be appended to the file name if it is not already there).",
                       metavar="FILE",
                       type=str,
                       )
        p.add_argument('--no-extmethods',
                       default=False,
                       action='store_true',
                       help="Disable extension methods."
                       )
        p.add_argument('--visualize',
                       default=False,
                       action='store_true',
                       help="Enable visualization in script."
                       )
        p.add_argument('--visualize-rate',
                       default=1,
                       type=int,
                       help="The rate of visualization (Default: 1, which means all frame)"
                       )
        p.add_argument('--visualize-param',
                       default=None,
                       help="Set visualization parameters."
                       )
        p.add_argument('--visualize-trace',
                       default=None,
                       type=str,
                       help="Dump frames to files instead of showing them"
                       )
        p.add_argument('--visualize-dry',
                       default=False,
                       action='store_true',
                       help="Do the data process but don't show any visualization"
                       )
        p.add_argument('--verbose',
                       default=False,
                       action='store_true',
                       help="Print out misc. information from script."
                       )
        p.add_argument('--no-flush',
                       action='store_true',
                       help="Disable calls to flush within benchmark iterations."
                       )
        p.add_argument('--no-do_while',
                       action='store_true',
                       help="Disable Bohrium's optimized `do_while`."
                       )

        self.args = p.parse_args()  # Parse the arguments
        self.args.size = [int(i) for i in self.args.size.split("*")] if self.args.size else []
        self.dtype = eval("numpy.%s" % self.args.dtype)
        if self.args.visualize:
            self._visual_args = VisualArgs(self.args)
        self.numpy_viz_handle = None  # NumPy visualization handle

    def flush(self, ignore_no_flush_arg=False):
        """Executes the queued instructions when running through Bohrium. Set `ignore_no_flush_arg=True` to flush
           even when the --no-flush argument is used"""
        if bh_is_loaded_as_np:
            if ignore_no_flush_arg or not self.args.no_flush:
                bohrium.flush()

    def start(self):
        """Start the timer"""
        self.flush()
        self._elapsed = time.time()

    def stop(self):
        """Stop the timer"""
        self.flush()
        self._elapsed = time.time() - self._elapsed

    def save_data(self, data_dict):
        """Save `data_dict` as a npz archive when --outputfn is used"""
        assert (isinstance(data_dict, dict))
        if self.args.outputfn is not None:
            # Clean `data_dict` for Bohrium arrays
            nobh_data = {"_bhary_keys": []}
            for k in data_dict.keys():
                if hasattr(data_dict[k], "copy2numpy"):
                    nobh_data[k] = data_dict[k].copy2numpy()
                    nobh_data["_bhary_keys"].append(k)
                else:
                    nobh_data[k] = data_dict[k]
            numpy.savez_compressed(self.args.outputfn, **nobh_data)

    def load_data(self):
        """Load the npz archive specified by --inputfn or None is not set"""
        if self.args.inputfn is None:
            return None
        else:
            nobh_data = numpy.load(self.args.inputfn)
            bhary_keys = nobh_data["_bhary_keys"].tolist()
            ret = {}
            for k in nobh_data.keys():
                if k == "_bhary_keys":
                    continue
                # Convert numpy arrays into bohrium arrays
                if bh_is_loaded_as_np and k in bhary_keys:
                    a = nobh_data[k]
                    ret[k] = bohrium.array(a, bohrium=True)
                else:
                    ret[k] = nobh_data[k]
            return ret

    def pprint(self):
        """Print the elapsed time"""
        print("%s - bohrium: %s, size: %s, elapsed-time: %f" % (
            self._script,
            bh_is_loaded_as_np,
            '*'.join([str(s) for s in self.args.size]),
            self._elapsed
        ))
        self.confirm_exit()

    def random_array(self, shape, dtype=None):
        """Return a random array of the given shape and dtype. If dtype is None, the type is determent by
        the --dtype command line arguments"""

        dtype = self.dtype if dtype is None else dtype
        size = functools.reduce(operator.mul, shape)
        if issubclass(numpy.dtype(dtype).type, numpy.integer):
            if bohrium is not None:
                # If bohrium is installed, we always uses the random123 in Bohrium even when running pure NumPy
                ret = bohrium.random.randint(1, size=size,  bohrium=bh_is_loaded_as_np)
            else:
                ret = numpy.random.randint(1, size=size)
        else:
            if bohrium is not None:
                # If bohrium is installed, we always uses the random123 in Bohrium even when running pure NumPy
                ret = bohrium.random.rand(*shape, bohrium=bh_is_loaded_as_np)
            else:
                ret = numpy.random.rand(*shape)
        return np.array(ret, dtype=dtype)

    def do_while(self, func, niters, *args, **kwargs):
        """Implements `bohrium.do_while()` for regular NumPy"""
        if bh_is_loaded_as_np and not self.args.visualize and not self.args.no_do_while:
            return bohrium.do_while(func, niters, *args, **kwargs)

        i = 0
        func.__globals__['get_iterator'] = lambda x=0: i + x

        def get_grid(*args):
            assert(len(args) > 0)
            grid = args[::-1]
            iterators = ()
            for dim, iterations in enumerate(grid):
                it = int(i/step_delay) % iterations
                step_delay *= iterations
                iterators = (it,) + iterators
            return iterators

        func.__globals__['get_grid'] = lambda args: get_grid(args)

        if niters is None:
            niters = sys.maxsize
        while i < niters:
            cond = func(*args, **kwargs)
            if cond is not None and not cond:
                break
            i += 1
            self.flush()
        return i

    def dump_visualization_trace_file(self, field):
        fname = "%s_%s.npy.gz" % (self._visual_args.trace_fname, field)
        data = np.stack(self._visual_args.trace[field])
        del self._visual_args.trace[field]
        print("Writing visualization trace file: %s (%s)" % (fname, data.shape))
        f = gzip.GzipFile("%s" % fname, "w")
        np.save(f, data)
        del data
        f.close()

    def __del__(self):
        if hasattr(self, "args"):  # If argparse fails, `args` dosn't exist
            if self.args.visualize and self._visual_args.trace_fname is not None and bh_is_loaded_as_np:
                self.dump_visualization_trace_file("org")
                self.dump_visualization_trace_file("zip")
                from bohrium import _bh
                msg = _bh.message("statistics-detail")
                with open("%s_stat.txt" % self._visual_args.trace_fname, "w") as f:
                    f.write(msg)

    def confirm_exit(self, msg="Hit Enter to exit..."):
        if self.args.visualize and self._visual_args.trace_fname is None and not self._visual_args.dry:
            if sys.version_info[0] == 2:
                raw_input(msg)
            else:
                input(msg)

    def plot_surface(self, ary, mode="2d", colormap=0, lowerbound=-200, upperbound=200):
        """Plot the surface `ary` when the --visualize argument is used. """

        def surface2d():
            if not self.numpy_viz_handle:
                import matplotlib.pyplot as plt
                plt.figure()
                img = plt.imshow(ary, interpolation="nearest", cmap=plt.cm.gray)
                plt.show(False)
                self.numpy_viz_handle = {
                    "plt": plt,
                    "img": img
                }
            else:
                plt = self.numpy_viz_handle["plt"]
                img = self.numpy_viz_handle["img"]

            plt.ion()
            img.set_data(ary)
            plt.draw()

        def surface3d():
            import matplotlib.pyplot as plt
            from matplotlib.ticker import LinearLocator, FormatStrFormatter
            from mpl_toolkits.mplot3d import axes3d, Axes3D  # We need this import for projection='3d' to work

            if self.numpy_viz_handle is None:
                self.numpy_viz_handle = {
                    "fig": plt.figure()
                }
                plt.show(False)

            fig = self.numpy_viz_handle["fig"]

            ax = fig.gca(projection='3d')

            H, W = ary.shape
            X = np.arange(0, W, 1)
            Y = np.arange(0, H, 1)
            X, Y = np.meshgrid(X, Y)

            surf = ax.plot_surface(
                X, Y, ary, rstride=1, cstride=1, cmap='winter',
                linewidth=0, antialiased=False
            )
            if "surf" in self.numpy_viz_handle:
                self.numpy_viz_handle["surf"].remove()

            self.numpy_viz_handle["surf"] = surf
            ax.set_zlim(0, 10)
            ax.zaxis.set_major_locator(LinearLocator(10))
            ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
            plt.ion()
            plt.draw()

        if self.args.visualize:
            if bh_is_loaded_as_np:
                from bohrium import visualization

                self._visual_args.count += 1
                if not (self._visual_args.count % self._visual_args.rate == 0):
                    return

                if self._visual_args.dry:  # We force the visualization process on a dry run
                    visualization.compressed_copy(ary, param=self._visual_args.param).copy2numpy()
                else:
                    if self._visual_args.trace_fname is None:  # We don't show visualization when tracing
                        visualization.plot_surface(ary, mode, colormap, lowerbound, upperbound, self._visual_args.param)
                    else:
                        org = ary.copy2numpy()
                        compressed = visualization.compressed_copy(ary, param=self._visual_args.param).copy2numpy()
                        self._visual_args.trace['org'].append(org)
                        self._visual_args.trace['zip'].append(compressed)
                        print("plot_surface %s: %s" % (self._visual_args.count, len(self._visual_args.trace['org'])),
                              file=sys.stderr)
            else:
                if mode.lower() == "2d":
                    surface2d()
                elif mode.lower() == "3d":
                    surface3d()
                else:
                    raise Exception("Invalid mode.")
