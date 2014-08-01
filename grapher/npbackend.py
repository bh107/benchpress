from graph import *
import numpy as np

class Npbackend(Graph):

    def render(self, data, order=None, baseline=None, highest=None):

        #Lets generate the vcache=10 graphs and with matmul

        for s in set([script for script, bridge, vem, ve, r in data]):

            res = {}
            for script, bridge, vem, ve, r in data:
                if script == s:
                    res[bridge + ve] = (np.mean(r['elapsed']), np.std(r['elapsed'])*2)

            means = []
            stderr = []
            for r in [res['NumPy OriginalN/A'],
                      res['npbacked-numpy (vcache=10)N/A'],
                      res['npbacked-numexpr (vcache=10)N/A'],
                      res['BohriumCPU'],
                      res['npbacked-pygpu (vcache=10)N/A'],
                      res['BohriumGPU']]:
                means.append(r[0])
                stderr.append(r[1])
            names = ['Native', 'NumPy', 'Numexpr', 'Bohrium-CPU', 'libgpuarray', 'Bohrium-GPU']

            self.graph_title = ""
            self.prep()                         # Prep it / clear the drawing board
            idx = np.arange(len(names))
            bar(idx, means, align='center', alpha=0.5, ecolor='black', yerr=stderr)
            xticks(idx, names)
            setp(xticks()[1], rotation=25)
            xlabel("")

            fig = gcf()
            fig.tight_layout()
            subplots_adjust()

            self.to_file(s)                # Spit them out to file

