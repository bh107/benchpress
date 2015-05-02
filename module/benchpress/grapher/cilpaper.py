from graph import *
import numpy as np
from matplotlib.ticker import FormatStrFormatter

def escape_latex_controls(s):
    return s.replace('_', '\\_')

def sane_label_name(bridge, ve):
    if ve == 'cpu_t01':
        ve = '1 thread'
    elif ve == 'cpu_t02':
        ve = '2 threads'
    elif ve == 'cpu_t04':
        ve = '4 threads'
    elif ve == 'cpu_t08':
        ve = '8 threads'
    elif ve == 'cpu_t16':
        ve = '16 threads'
    elif ve == 'cpu_t32':
        ve = '32 threads'
    elif ve == 'NA':
        ve = ''

    if bridge == 'Python/NP':
        bridge = 'Numpy'
    elif bridge == 'Mono/Unsafe':
        bridge = 'Unsafe'
    elif bridge == 'Mono/Managed':
        bridge = 'Managed'
    elif bridge == 'Mono/Bohrium':
        bridge = ve
        ve = ''
    elif bridge == 'Python/BH':
        bridge = 'Python bh'

    if ve == '':
        return bridge
    else:
        return "%s - %s" % (bridge,ve)


def filter_results(bridge, ve):
    if bridge == 'Python/BH':
        return False

    return True


class Cilpaper(Graph):

    def render(self, raw, data, order=None, baseline=None, highest=None):
        self.file_formats = ['pdf']

        #Lets handle one benchmark (script) at a time
        for s in set([script for script, bridge, vem, ve, r in data]):

            name = []
            mean = []
            stderr = []
            for script, bridge, vem, ve, r in data:
                print bridge, ve
                if script == s and filter_results(bridge, ve):
                    name.append(escape_latex_controls(sane_label_name(bridge, ve)))
                    filename = r['script']
                    if len(r['elapsed']) > 0:
                        mean.append(np.mean(r['elapsed']))
                        stderr.append(np.std(r['elapsed'])*2)
                    else:
                        mean.append(0)
                        stderr.append(0)


            self.graph_title = ''
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

