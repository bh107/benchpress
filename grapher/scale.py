from graph import *

class Scale(Graph):
    """Create a graph that illustrates scalabiltity."""

    def render(self, script, data, order=None, baseline=None, highest=None):

        if baseline:
            self.yaxis_label='In relation to "%s"' % baseline

        self.prep()                         # Prep it / clear the drawing board

        values = []
        for label, samples in data:
            if not 'omp' in label:
                continue

            lbl, threads = label.split('omp')
            values.append((int(threads), samples['elapsed']['avg'].pop()))
        values.sort()

        sizes   = []
        speedup = []
        for nthreads, times in values:
            sizes.append(nthreads)
            speedup.append(times)

        linear = [2**x for x in range(0, len(sizes))]
        xscale("log")   # Scale with a neat border
        yscale("log")
        xticks(linear, linear)
        xlim(xmin=min(linear)*0.85, xmax=max(linear)*1.25)
        yticks(linear, linear)
        ylim(ymin=min(linear)*0.85, ymax=max(linear)*1.25)

        plot(linear, linear)
        plot(linear, speedup)

        self.to_file(script)                # Spit them out to file

