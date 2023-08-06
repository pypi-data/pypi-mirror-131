from ..utils import make_callable, from_db


class Receiver:
    """A receiver is composed of all the devices on the receiving side,
    excluding the antenna.

    Parameters
    ----------
    noise_temperature : float or callable
        Noise temperature of the receiver backend [K]
    devices : `Device` or callable
        List of devices in the transmitter chain

    Notes
    -----
    The order of the `devices` list should be from antenna side towards
    receiver backend.
    """
    def __init__(self, noise_temperature=None, devices=None):
        self.devices = make_callable(devices)
        self.noise_temperature = make_callable(noise_temperature)
        self.noise_figure = lambda t: None
        self.reference_temperature = lambda t: None

    @classmethod
    def from_noise_figure(cls, noise_figure, reference_temperature=290,
                          devices=None):
        """Create a Receiver instance using the noise_figure instead of
        noise temperature.

        Parameters
        ----------
        noise_figure : float or callable
            Noise figure of the receiver backend [dB]
        reference_temperature : float or callable
            Reference temperature for conversion between `noise_figure` and
            `noise_temperature` [K]. (Defaults to 290 K)
        devices : List of devices in the receiver chain.

        Notes
        -----
        The order of the `devices` list should be from antenna towards
        receiver backend.
        """
        self = cls.__new__(cls)
        self.devices = make_callable(devices)
        self.noise_temperature = lambda t: None
        self.noise_figure = make_callable(noise_figure)
        self.reference_temperature = make_callable(reference_temperature)
        return self

    def get_line_gain(self, time=None):
        """Total gain of the line devices [dB]."""
        if self.devices(time) is not None:
            return sum(ld.get_gain(time) for ld in self.devices(time))
        else:
            return 0

    def get_noise_temperature(self, time=None):
        """Noise temperature of the receiver backend [K]."""
        noise_temperature = self.noise_temperature(time)
        if noise_temperature is None:
            # convert from noise figure to noise temperature
            noise_figure = self.noise_figure(time)
            if noise_figure is None:
                return 0
            else:
                reftemp = self.reference_temperature(time)
                return reftemp * (from_db(noise_figure) - 1)
        return noise_temperature

    def get_system_noise_temperature(self, time=None):
        """Total noise temperature of the receiver chain [K]."""
        noise_temp = 0
        gains = 1
        if self.devices(time) is not None:
            for ld in self.devices(time):
                device_noise_temp = ld.get_noise_temperature(time)
                noise_temp += device_noise_temp / gains
                gains = gains * from_db(ld.gain(time))
        receiver_noise_temp = self.get_noise_temperature(time)
        noise_temp += receiver_noise_temp / gains
        return noise_temp
