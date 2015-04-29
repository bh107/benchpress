from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np

def plot_surface(data):

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    H, W = data.shape
    X = np.arange(0, W, 1)
    Y = np.arange(0, H, 1)
    X, Y = np.meshgrid(X, Y)

    surf = ax.plot_surface(X, Y, data, rstride=1, cstride=1, cmap='winter',
    linewidth=0, antialiased=False)
    ax.set_zlim(0, 10)

    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()
