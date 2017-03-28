from scipy.ndimage.filters import gaussian_filter
from statsmodels.sandbox.stats.multicomp import multipletests
import numpy as np
import scipy.interpolate as spinterp

def convolve(img, upsample=4, sigma=4):
    '''
    2D Gaussian convolution
    '''

    x = np.arange(16)
    y = np.arange(28)
    g = spinterp.interp2d(y, x, img)
    ZZ_on = g(np.arange(0, 28, 1. / upsample), np.arange(0, 16, 1. / upsample))
    ZZ_on_f = gaussian_filter(ZZ_on, float(sigma), mode='constant')
    z_on_new = np.zeros((16, 28))
    for ii in range(upsample):
        for jj in range(upsample):
            z_on_new += ZZ_on_f[ii::upsample, jj::upsample]

    z_on_new = z_on_new/z_on_new.sum()*img.sum()
    return z_on_new

def plot_fields(data, axes=None, show=True, clim=(0, 1), colorbar=True):

    import matplotlib.pyplot as plt
    from matplotlib import ticker

    data = np.array(data)
    if axes is None:
        _, axes = plt.subplots(1, 2)

    axes[0].imshow(data[:16 * 28].reshape(16, 28), clim=clim, interpolation='none', origin='lower')
    img = axes[1].imshow(data[16 * 28:].reshape(16, 28), clim=clim, interpolation='none', origin='lower')
    if colorbar == True:
        cb = axes[0].figure.colorbar(img, ax=axes[1])
        tick_locator = ticker.MaxNLocator(nbins=5)
        cb.locator = tick_locator
        cb.update_ticks()

    if show == True:
        plt.show()