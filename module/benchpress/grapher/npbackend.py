from graph import *
import numpy as np
from matplotlib.ticker import FormatStrFormatter

class Npbackend(Graph):

    def render(self, raw, data, order=None, baseline=None, highest=None):

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

        native_numpy = {}
        for script, bridge, vem, ve, r in data:
            if script == 'snakes_and_ladders_no_matmul':
                continue
            if bridge == 'NumPy Original':
                native_numpy[script] = np.mean(r['elapsed'])

        res = {}
        for script, bridge, vem, ve, r in data:
            if script == 'snakes_and_ladders_no_matmul':
                continue
            if bridge == 'npbacked-numpy (vcache=0)':
                res[script] = np.mean(r['elapsed'])/native_numpy[script]
                res[script] = (res[script] - 1)*100 #Convert to precent

        names = ['Heat Equation', 'Shallow Water', 'Snakes and Ladders']
        means = [res['Heat 2D'], res['Shallow Water'], res['snakes_and_ladders']]

        self.graph_title = ""
        self.yaxis_label='Overhead in relation to Native NumPy'
        self.prep()                         # Prep it / clear the drawing board
        idx = np.arange(len(names))
        bar(idx, means, align='center', alpha=0.5, ecolor='black')
        xticks(idx, names)
        setp(xticks()[1], rotation=0)
        xlabel("")
        gca().yaxis.set_major_formatter(FormatStrFormatter('%d %%'))

        fig = gcf()
        fig.tight_layout()
        subplots_adjust()

        self.to_file("overhead")                # Spit them out to file

