import numpy as np

import scipy.signal as scs
from scipy.ndimage import convolve1d

from . import utils

def norm_gauss_window(bin_length, std):
    """
    Gaussian window with its mass normalized to 1

    Parameters
    ----------
    bin_length : float
        binning length of the array we want to smooth in ms
    std : float
        standard deviation of the window
        use hw_to_std to calculate std based from half-width

    Returns
    -------
    win : 1D np.array
        Gaussian kernel with
            length: 10*std/bin_length
            mass normalized to 1
    """
    win = scs.gaussian(int(10*std/bin_length), std/bin_length)
    return win / np.sum(win)


def hw_to_std(hw):
    """
    Convert half-width to standard deviation for a Gaussian window.
    """
    return hw / (2 * np.sqrt(2 * np.log(2)))


def smooth_data(mat, dt=None, std=None, hw=None, win=None):
    """
    Smooth a 1D array or every column of a 2D array

    Parameters
    ----------
    mat : 1D or 2D np.array
        vector or matrix whose columns to smooth
        e.g. recorded spikes in a time x neuron array
    dt : float
        length of the timesteps in seconds
    std : float (optional)
        standard deviation of the smoothing window
    hw : float (optional)
        half-width of the smoothing window
    win : 1D array-like (optional)
        smoothing window to convolve with

    Returns
    -------
    np.array of the same size as mat
    """
    assert only_one_is_not_None((win, hw, std))

    if win is None:
        assert dt is not None, "specify dt if not supplying window"

        if std is None:
            std = hw_to_std(hw)

        win = norm_gauss_window(dt, std)

    if mat.ndim == 1 or mat.ndim == 2:
        return convolve1d(mat, win, axis=0, output=np.float32, mode='reflect')
    else:
        raise ValueError("mat has to be a 1D or 2D array")


def only_one_is_not_None(args):
    return sum([arg is not None for arg in args]) == 1


@utils.copy_td
def smooth_signals(trial_data, signals, std=None, hw=None):
    """
    Smooth signal(s)

    Parameters
    ----------
    trial_data: pd.DataFrame
        trial data
    signals: list of strings
        signals to be smoothed
    std : float (optional)
        standard deviation of the smoothing window
        default 0.05 seconds
    hw : float (optional)
        half-width of the smoothing window

    Returns
    -------
    trial_data: DataFrame with the appropriate fields smoothed
    """
    bin_size = trial_data.iloc[0]['bin_size']

    if hw is None:
        if std is None:
            std = 0.05
    else:
        assert (std is None), "only give hw or std"

        std = hw_to_std(hw)

    win = norm_gauss_window(bin_size, std)

    if isinstance(signals, str):
        signals = [signals]

    for (i, trial) in trial_data.iterrows():
        for sig in signals:
            trial_data.at[i, sig] = smooth_data(trial[sig], win=win)

    return trial_data
