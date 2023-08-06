from ..utils import make_callable, from_db


class Device:
    """Active or passive devices in the transmitter or receiver chain.

    Parameters
    ----------
    gain : float or callable
        Gain of the device (negative for loss) [dB]
    noise_temperature : float or callable
        Noise temperature of the device [K]
    """
    def __init__(self, gain=0, noise_temperature=None):
        self.gain = make_callable(gain)
        self.noise_temperature = make_callable(noise_temperature)
        self.noise_figure = lambda t: None
        self.reference_temperature = lambda t: None

    @classmethod
    def from_noise_figure(cls, gain, noise_figure, reference_temperature=290):
        """Create a Device instance using the noise_figure instead of
        noise temperature.

        Parameters
        ----------
        gain : float or callable
            Gain of the device (negative for loss) [dB]
        noise_figure : float or callable
            Noise figure of the device [dB]
        reference_temperature : float or callable
            Reference temperature for conversion between `noise_figure` and
            `noise_temperature` [K]. (Defaults to 290 K)
        """
        self = cls.__new__(cls)
        self.gain = make_callable(gain)
        self.noise_temperature = lambda t: None
        self.noise_figure = make_callable(noise_figure)
        self.reference_temperature = make_callable(reference_temperature)
        return self

    def get_gain(self, time=None):
        return self.gain(time)

    def get_noise_temperature(self, time=None):
        """Noise temperature of the device [K]."""
        noise_temperature = self.noise_temperature(time)
        if noise_temperature is None:
            noise_figure = self.noise_figure(time)
            if noise_figure is None:
                return 0
            reftemp = self.reference_temperature(time)
            return reftemp * (from_db(noise_figure) - 1)
        return noise_temperature
