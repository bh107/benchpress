gfx_handle = None

def render(world, stop=False):
    global gfx_handle
    if not gfx_handle:
        import matplotlib.pyplot as plt
        plt.figure()
        img = plt.imshow(world, interpolation="nearest", cmap = plt.cm.gray)
        plt.show(False)
        gfx_handle = {
            "plt": plt,
            "img": img
        }
    else:
        plt = gfx_handle["plt"]
        img = gfx_handle["img"]

    if stop:
        plt.ioff()
        plt.show()
    else:
        plt.ion()
        img.set_data(world)
        plt.draw()

