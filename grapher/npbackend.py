from graph import *
import numpy as np

class Npbackend(Graph):

    def render(self, data, order=None, baseline=None, highest=None):

        #Lets generate the vcache=10 graphs and with matmul

        for s in set([script for script, bridge, vem, ve, r in data]):

            self.prep()                         # Prep it / clear the drawing board
            means = []
            names = []

            for script, bridge, vem, ve, r in data:
                if script == s and bridge.find("vcache=0") == -1 and bridge.find("no-matmul") == -1:
                    n = bridge.replace(" (vcache=10)", "")+ve
                    n = n.replace("N/A", "")
                    names.append(n)
                    means.append(np.mean(r['elapsed']))

                    if n == 'NumPy Original':
                        names = [names[-1]] + names[:-1]
                        means = [means[-1]] + means[:-1]

            self.graph_title = s
            self.prep()                         # Prep it / clear the drawing board
            idx = np.arange(len(names))
            bar(idx, means, align='center')
            xticks(idx, names)
            setp(xticks()[1], rotation=90)
            xlabel("")

            fig = gcf()
            fig.tight_layout()
            subplots_adjust()

            self.to_file(s)                # Spit them out to file

