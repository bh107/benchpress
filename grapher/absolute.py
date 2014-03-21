from graph import *

class Absolute(Graph):
    """Basic plot of x,y values with lgnd and stuff."""

    def render(self, data, order=None, baseline=None, highest=None):

        self.prep()                         # Prep it / clear the drawing board
        for lgnd in data:

            if baseline:
                self.yaxis_label='In relation to "%s"' % baseline

            """
            xticks(linear, linear)
            xlim(xmin=min(linear)*0.85, xmax=max(linear)*1.25)
            yticks(linear, linear)
            ylim(ymin=min(linear)*0.85, ymax=max(linear)*1.25)
            """
            xs = [x for x, y, var in data[lgnd]]
            ys = [y for x, y, var in data[lgnd]]
            vs = [var for x, y, var in data[lgnd]]
            
            xticks([0, 50, 100, 150, 200], [0, 50, 100, 150, 200])
            plot(xs, ys, label=lgnd, marker='x')
            legend(loc="upper left")

        self.to_file(self.graph_title)                # Spit them out to file

