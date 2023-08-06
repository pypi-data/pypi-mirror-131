from ..utils import make_callable
from .base import AntennaNoise


class SimpleAntennaNoise(AntennaNoise):
    """Antenna noise as a constant or time-dependent value.

    Parameters
    ----------
    noise_temperature : float or callable
        Antenna noise temperature [K]

    """
    def __init__(self, noise_temperature):
        self.noise_temperature = make_callable(noise_temperature)

    def get_noise_temperature(self, time=None):
        return self.noise_temperature(time)
