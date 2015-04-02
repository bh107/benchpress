from graph import *
from benchpress.result_parser import standard_deviation, avg

def max_deviation(samples):
    return max(samples)-min(samples)

class Bypass_bwo(Graph):
    """Basic plot of x,y values with lgnd and stuff."""

    def render(self, raw, data, order=None, baseline=None, highest=None):

        self.prep()                         # Prep it / clear the drawing board

        # These are the applications we want data from
        applications = [
            "Black Scholes",
            "Heat Equation",
            "N-body",
            "Shallow Water"
        ]

        app_map = {
            "Black Scholes  10m":   "Black Scholes",
            "Heat Equation  5k":    "Heat Equation",
            "N-body  5k":           "N-body",
            "Shallow Water  5k":    "Shallow Water"
        }

        # In these setups
        setups = [
            "With Visualization",
            "Without Visualization"
        ]

        # Map the key to a more understandable name
        setup_mapping = {
            "numpy/proxyViz/sleep    0ms":  "With Visualization",
            "numpy/proxy/sleep    0ms":     "Without Visualization",
        }
        
        # Now grab the above from data and create the data-set
        datasets = {app: {setup: {'elapsed':None,'std':None} for setup in setups} for app in applications}
        for app, bridge, key1, key2, sample in data:
            key = "%s/%s/%s" % (bridge, key1, key2)
            if key not in setup_mapping or app not in app_map:
                continue

            setup = setup_mapping[key]
            app_m = app_map[app]
            datasets[app_m][setup]['elapsed'] = avg(sample['elapsed']) 
            datasets[app_m][setup]['std']     = standard_deviation(sample['elapsed']) * 2
            #datasets[app_m][setup]['std']     = max_deviation(sample['elapsed']) 

        # Dataset needed

        
        # Now this what we need to create the graph.
        N       = len(datasets.keys())
        ind     = np.arange(N)  # the x locations for the groups
        width   = 0.35          # the width of the bars

        with_proxy_means  = [datasets[app]['With Visualization']['elapsed'] for app in applications]
        with_proxy_std    = [datasets[app]['With Visualization']['std'] for app in applications]

        without_proxy_means = [datasets[app]['Without Visualization']['elapsed'] for app in applications]
        without_proxy_std = [datasets[app]['Without Visualization']['std'] for app in applications]

        fig, ax = plt.subplots()

        rects1 = ax.bar(ind, 
                        with_proxy_means, width, color='r', 
                        yerr=with_proxy_std
        )

        rects2 = ax.bar(ind+width, 
                        without_proxy_means, width, color='y',
                        yerr=without_proxy_std
        )

        # add some
        ax.set_ylabel('Wall-clock time in seconds')

        ax.set_xticks(ind+width)
        ax.set_xticklabels( applications )

        ax.legend( (rects1[0], rects2[0]), setups, 
                    bbox_to_anchor=(0., 1.02, 1.,.102), 
                    loc=2, ncol=2, mode="expand", borderaxespad=0.
        )

        def autolabel(rects):
            # attach some text labels
            for rect in rects:
                height = rect.get_height()
                ax.text(rect.get_x()+rect.get_width()/2.,
                        1.05*height, 
                        '%0.2f'%height,ha='center',
                        va='bottom'
                )

        autolabel(rects1)
        autolabel(rects2)
        #plt.tight_layout()
        self.to_file('bandwidth_octuplets')                # Spit them out to file

