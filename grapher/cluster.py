from graph import *
import pprint
import re


class Cluster(Graph):
    """Create a graph that illustrates scalabiltity."""

    def render(self, data, order=None, baseline=None, highest=None):

        for script in data:

            if baseline:
                self.yaxis_label='In relation to "%s"' % baseline

            self.graph_title = script
            self.prep()                         # Prep it / clear the drawing board

            pprint.pprint(data)

            values = []
            for label, samples in data[script]:
                N, P, T = re.search("N(\d+)P(\d+)T(\d+)", label).groups()
                N = int(N)
                P = int(P)
                T = int(T)
                values.append((N*P*T, samples['elapsed']['avg'], "%d (N%dP%02dT%03d)"%(N*P*T, N, P, T)))
            values.sort()

            sizes   = []
            speedup = []
            ticks = []
            for nthreads, times, tick in values:
                sizes.append(nthreads)
                speedup.append(times)
                ticks.append(tick)

            linear = [2**x for x in range(0, len(sizes))]

            print linear

            xscale("log")   # Scale with a neat border
            yscale("log")
            xticks(linear, ticks, rotation="vertical")
            xlim(xmin=min(linear)*0.85, xmax=max(linear)*1.25)
            yticks(linear, linear)
            ylim(ymin=min(linear)*0.85, ymax=max(linear)*1.25)

            plot(linear, linear)
            plot(linear, speedup)

            self.to_file(script)                # Spit them out to file

