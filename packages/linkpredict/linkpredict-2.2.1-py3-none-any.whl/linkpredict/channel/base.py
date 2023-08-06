from ..utils import make_callable


class Channel:
    """A channel contains the properties of the radio link.

    Parameters
    ----------
    frequency : float or callable
        Carrier frequency [Hz]
    pfd_limit : float or callable, optional
        Power flux density limit [dBW/m^2] for power flux density margin
    received_power_threshold : float or callable, optional
        Threshold [dBW] for received power margin
    modulation: `Modulation` or callable, optional
        The modulation of the radio link
    """
    def __init__(
            self, frequency, pfd_limit=None,
            received_power_threshold=None, modulation=None):
        self.frequency = make_callable(frequency)
        self.pfd_limit = make_callable(pfd_limit)
        self.received_power_threshold = make_callable(received_power_threshold)
        self.modulation = make_callable(modulation)

    def get_frequency(self, time=None):
        return self.frequency(time)

    def get_pdf_limit(self, time=None):
        return self.pfd_limit(time)

    def get_received_power_threshold(self, time=None):
        return self.received_power_threshold(time)


class Modulation:
    """Base class for modulations.

    Parameters
    ----------
    cno_ratio_threshold: float or callable
        Threshold for the carrier to noise density for the demodulator to be
        able to demodulate the signal [dB-Hz]
    modulation_loss: float or callable
        Additional loss due to the modulation technique [dB]
    """
    def __init__(self, cno_ratio_threshold=None, modulation_loss=None):
        self.cno_ratio_threshold = make_callable(cno_ratio_threshold)
        self.modulation_loss = make_callable(modulation_loss)

    def get_cno_ratio_threshold(self, time=None):
        return self.cno_ratio_threshold(time)

    def get_modulation_loss(self, time=None):
        return self.modulation_loss(time)
