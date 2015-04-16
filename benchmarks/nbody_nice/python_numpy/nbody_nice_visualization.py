def gfx_init(xm, ym, zm):
    """Init plot"""

    from mpl_toolkits.mplot3d import Axes3D  # pylint: disable=W0611
    import matplotlib.pyplot as plt

    plt.ion()
    fig = plt.figure()
    sub = fig.add_subplot(111, projection='3d')
    sub.xm = xm
    sub.ym = ym
    sub.zm = zm
    return plt, sub

def gfx_show(plt, sub, solarsystem, bodies):
    """Show plot"""
    
    sub.clear()
    sub.scatter(                # Sun
        solarsystem['x'][0],
        solarsystem['y'][0],
        solarsystem['z'][0],
        s=100,
        marker='o',
        c='yellow',
    )
    sub.scatter(                # Planets
        [solarsystem['x'][1:]],
        [solarsystem['y'][1:]],
        [solarsystem['z'][1:]],
        s=5,
        marker='o',
        c='blue',
    )
    sub.scatter(                # Astoroids
        [bodies['x']],
        [bodies['y']],
        [bodies['z']],
        s=.1,
        marker='.',
        c='green',
    )

    sub.set_xbound(-sub.xm, sub.xm)
    sub.set_ybound(-sub.ym, sub.ym)
    try:
        sub.set_zbound(-sub.zm, sub.zm)
    except AttributeError:
        print("Warning: correct 3D plots may require matplotlib-1.1 or later")

    plt.draw()
