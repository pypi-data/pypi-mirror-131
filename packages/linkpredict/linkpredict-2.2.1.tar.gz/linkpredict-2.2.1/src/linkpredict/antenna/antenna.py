import numpy as np
from scipy.interpolate import interp1d

from ..utils import make_callable
from .base import Antenna


class OmniDirectionalAntenna(Antenna):
    """An antenna with uniform gain in all directions.

    Parameters
    ----------
    gain : float or callable
        The gain w.r.t. an ideal isotropic antenna [dBi].
    linear_polarized : boolean or callable
        Whether antenna is linear or circular polarized.
    """
    def __init__(self, gain, linear_polarized=False):
        self.gain = make_callable(gain)
        self.linear_polarized = make_callable(linear_polarized)

    def is_linear_polarized(self, time=None):
        return self.linear_polarized(time)

    def get_gain(self, angle=None, time=None):
        return self.gain(time)


class MeasuredAntenna(Antenna):
    """An antenna with a radiation pattern based on multiple measured values.

    Parameters
    ----------
    measured_gains : dict
        A dict with aspect angles [deg] as keys and gains [dBi] w.r.t
        an isotropic antenna as values.
    symetric : boolean, default False
        Set to True to create a mirrored pattern for angles > 180 deg
    linear_polarized : boolean or callable, default False
        Whether antenna is linear or circular polarized

    Notes
    -----
    The radiation pattern is interpolated between measured values.

    Examples
    --------
    Produce a symetric pattern from gains measured in steps of 45 degree:

    >>> gains = {0: 1.6, 45: -0.5, 90: 1.8, 135: -0.6, 180: 1.5}
    >>> MeasuredAntenna(measured_gains=gains, symetric=True)
    """
    def __init__(self, measured_gains, symetric=False, linear_polarized=False):
        if not isinstance(measured_gains, dict):
            raise TypeError("Must provide gains as a dict.")
        if not all(isinstance(x, (int, float))
                   for x in measured_gains.keys()):
            raise TypeError("The dict keys must be int or float.")
        if symetric and any(a > 180 for a in measured_gains.keys()):
            raise ValueError("Do not supply gain measurements for angles "
                             " > 180 deg if symetric pattern is used.")
        if any(a < 0 or a > 360 for a in measured_gains.keys()):
            raise ValueError("Pattern angles must be between 0 and 360 deg.")
        gains = {}
        for angle, gain in measured_gains.items():
            gains[angle] = gain
            if symetric:
                gains[360 - angle] = gain
        self.angles = sorted(gains.keys())
        self.gains = [gains[a] for a in self.angles]
        self.spline = interp1d(
            self.angles, self.gains, kind="cubic", fill_value="extrapolate")
        self.linear_polarized = make_callable(linear_polarized)

    def is_linear_polarized(self, time=None):
        return self.linear_polarized(time)

    def get_gain(self, angle=0, time=None):
        return float(self.spline(angle))


class MainLobeAntenna(Antenna):
    """An antenna with a pattern consisting of a main lobe (and some smaller
    side lobes).

    Parameters
    ----------
    peak_gain : float or callable
        Gain of the main lobe [dBi] w.r.t. an isotropic antenna.
    beam_3db_width : float
        Angle [deg] between the two points on either side
        of the main lobe, where the gain is 3 dB lower than the peak gain.
    linear_polarized : boolean or callable, default False
        Whether antenna is linear or circular polarized.

    Notes
    -----
    This pattern model is a simplified model and should only be used for
    antenna angles around +/- 3 * beamwidth.
    """
    def __init__(self, peak_gain, beam_3db_width, linear_polarized=False):
        self.peak_gain = make_callable(peak_gain)
        self.beamwidth = beam_3db_width
        self.linear_polarized = make_callable(linear_polarized)

    def is_linear_polarized(self, time=None):
        return self.linear_polarized(time)

    def _pattern_func(self, a):
        # a is assumed in radians
        if a == 0:
            return 0
        halfvalue = 1.38935
        t = a * halfvalue / np.radians(self.beamwidth/2)
        return 10 * np.log10((np.sin(t)**2)/(t**2))

    def get_gain(self, angle=0, time=None):
        angle = angle % 360
        if angle > 180:
            angle = angle - 360
        gain = self._pattern_func(np.radians(angle)) + self.peak_gain(time)
        return gain
