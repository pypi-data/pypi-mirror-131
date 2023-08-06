from ..utils import make_callable


class Transmitter:
    """A transmitter is composed of all the devices on the sending side,
    excluding the antenna.

    Parameters
    ----------
    amplifier_power : float or callable
        The output power of the amplifier [dbW]
    devices : `Device` or callable
        List of devices in the transmitter chain

    Notes
    -----
    The order of the `devices` list should be from amplifier towards
    antenna.
    """
    def __init__(self, amplifier_power, devices=None):
        self.amplifier_power = make_callable(amplifier_power)
        self.devices = make_callable(devices)

    def get_amplifier_power(self, time=None):
        return self.amplifier_power(time)

    def get_line_gain(self, time=None):
        """Total gain of the line devices [dB]."""
        if self.devices(time) is not None:
            return sum(ld.get_gain(time) for ld in self.devices(time))
        else:
            return 0
