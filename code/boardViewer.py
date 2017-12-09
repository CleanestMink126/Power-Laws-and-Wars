import sys

import numpy as np
import matplotlib.pyplot as plt

from matplotlib import animation
from scipy.signal import convolve2d

import warBuilder
from thinkstats2 import Pmf, Pdf, Cdf, Hist
import thinkplot
import pickle


class War2DViewer:
    """Generates an animated view of an array image."""

    cmap = plt.get_cmap('Greens')
    options = dict(interpolation='nearest', alpha=0.8,
                   vmin=0, vmax=1)

    def __init__(self, viewee):
        self.viewee = viewee
        self.im = None
        self.hlines = None
        self.vlines = None

    # TODO: should this really take iters?
    def step(self, iters=1):
        """Advances the viewee the given number of steps."""
        for i in range(iters):
            self.viewee.step()

    def draw(self, grid=False):
        """Draws the array and any other elements.

        grid: boolean, whether to draw grid lines
        """
        self.draw_array()
        if grid:
            self.draw_grid()

    def draw_array(self, array=None, cmap=None, **kwds):
        """Draws the cells."""
        # Note: we have to make a copy because some implementations
        # of step perform updates in place.
        if array is None:
            a = self.viewee.image
            b = self.viewee.image2
            array = np.concatenate((a,b), axis = 1)
        a = array.copy()
        # cmap = self.cmap if cmap is None else cmap

        # n, m = a.shape
        # plt.axis([0, m, 0, n])
        # plt.xticks([])
        # plt.yticks([])
        #
        # options = self.options.copy()
        # options['extent'] = [0, m, 0, n]
        # options.update(kwds)
        self.im = plt.imshow(a)

    def draw_grid(self):
        """Draws the grid."""
        a = self.viewee.array
        n, m = a.shape
        lw = 2 if m < 10 else 1
        options = dict(color='white', linewidth=lw)

        rows = np.arange(1, n)
        self.hlines = plt.hlines(rows, 0, m, **options)

        cols = np.arange(1, m)
        self.vlines = plt.vlines(cols, 0, n, **options)

    def animate(self, frames=20, interval=200, grid=False):
        """Creates an animation.

        frames: number of frames to draw
        interval: time between frames in ms
        """
        fig = plt.figure()
        self.draw(grid)
        anim = animation.FuncAnimation(fig, self.animate_func,
                                       init_func=self.init_func,
                                       frames=frames, interval=interval)
        return anim

    def init_func(self):
        """Called at the beginning of an animation."""
        pass

    def animate_func(self, i):
        """Draws one frame of the animation."""
        if i > 0:
            self.step()
        a = self.viewee.image
        b = self.viewee.image2
        c = np.concatenate((a,b), axis = 1)
        self.im.set_array(c)
        return (self.im,)
    # Pmf, Pdf, Cdf, Hist

    def plotCDF(self, lst,filename):
        cdf = Cdf(lst)
        thinkplot.Cdf(Cdf(lst), style='.', label='CDF', complement=True)
        thinkplot.config(xscale='log', yscale='log', xlabel='severity', ylabel='CCDF')
        plt.savefig(filename)

if __name__ == "__main__":
    mywar = warBuilder.War2D(200, 100)
    for i in range(500):
        mywar.step()
        print("STEP:"+ str(i))

    plotter = War2DViewer(mywar)
    # pickle.dump(mywar.warDamages, open('data.pickle', 'wb'))
    # loaded_data = pickle.load(open('data.pickle', 'rb'))
    plotter.plotCDF(mywar.warDamages, '1000steps.png')

    animator = War2DViewer(mywar)
    anim = animator.animate (frames = 40, interval = 300)
    plt.show()
