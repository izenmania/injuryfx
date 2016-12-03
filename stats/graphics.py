import numpy as np
from matplotlib.figure import Figure
from matplotlib import cm as cm


def generate_heatmap(coords):

    # Number of points
    n = 500

    # Takes a list of coordinate pairs and generates a heatmap, formatted for the site
    # Dummy numbers - placeholders.  In future will be generated from coords.
    x = 6*np.random.randn(n)
    y = 8*np.random.randn(n) + 30

    # Generate the 2d histogram
    # The domain is -24 to 24 inches horizontally and 0 to 60 inches vertically
    z, xedges, yedges = np.histogram2d(x, y, bins=[12,15], range = [[-24,24],[0,60]])

    # We need center coordinates instead of edges coordinates for the contour function
    # We add two because the bins are four inches wide
    xcenter = xedges + 2
    ycenter = yedges + 2
    xcenter = xcenter[:-1]
    ycenter = ycenter[:-1]
    Xcentermesh, Ycentermesh = np.meshgrid(xcenter, ycenter)

    # Create the figure object
    fig = Figure()
    ax = fig.add_subplot(1, 1, 1)

    # Create the contour plot
    CS = ax.contourf(Xcentermesh,Ycentermesh,z.T, 9, cmap = cm.YlOrRd)
    ax.axis([-22,22,2,58])
    ax.set_aspect('equal')
    fig.colorbar(CS)


    # Add the strike zone as a black box
    ax.plot([-12,12],[18,18],'k')
    ax.plot([-12,12],[42,42],'k')
    ax.plot([-12,-12],[18,42],'k')
    ax.plot([12,12],[18,42],'k')

    return fig
