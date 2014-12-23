from graph import *
import numpy as np
from matplotlib.ticker import FormatStrFormatter

class Daily(Graph):

    def render(self, raw, data, order=None, baseline=None, highest=None):

        #Lets handle one benchmark (script) at a time
        for s in set([script for script, bridge, vem, ve, r in data]):

            name = []
            mean = []
            stderr = []
            for script, bridge, vem, ve, r in data:
                if script == s:
                    name.append("%s/%s"%(bridge,ve))
                    filename = r['script']
                    if len(r['elapsed']) > 0:
                        mean.append(np.mean(r['elapsed']))
                        stderr.append(np.std(r['elapsed'])*2)
                    else:
                        mean.append(0)
                        stderr.append(0)

            self.graph_title = s
            self.prep()                         # Prep it / clear the drawing board
            idx = np.arange(len(name))
            bar(idx, mean, align='center', alpha=0.5, ecolor='black', yerr=stderr)
            xticks(idx, name)
            setp(xticks()[1], rotation=25)
            xlabel("")

            fig = gcf()
            fig.tight_layout()
            subplots_adjust()

            self.to_file(filename)                # Spit them out to file

