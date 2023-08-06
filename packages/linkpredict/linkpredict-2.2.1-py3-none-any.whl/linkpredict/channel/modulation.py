from math import erfc

import numpy as np
from scipy.optimize import root

from ..utils import make_callable, from_db
from .base import Modulation


def _Q_erf(x):
    return (1 / 2) * erfc(x / 2 ** (1 / 2))


class AnalogModulation(Modulation):
    """Base class for analog modulations.

    Parameters
    ----------
    bandwidth : float or callable
        Bandwidth of the demodulator [Hz]
    snr_threshold : float or callable, optional
        Threshold for the base band signal to noise ratio for the signal to
        be usable [dB]
    cno_ratio_threshold : float or callable, optional
        Threshold for the carrier to noise density for the demodulator to be
        able to demodulate the signal [dB-Hz].
    modulation_loss : float or callable, optional
        Additional loss due to the modulation technique [dB]
    """
    def __init__(
            self,
            bandwidth,
            snr_threshold=None,
            cno_ratio_threshold=None,
            modulation_loss=None):
        super().__init__(
            cno_ratio_threshold=cno_ratio_threshold,
            modulation_loss=modulation_loss)
        self.bandwidth = make_callable(bandwidth)
        self.snr_threshold = make_callable(snr_threshold)

    def get_bandwidth(self, time=None):
        return self.bandwidth(time)

    def get_snr_threshold(self, time=None):
        return self.snr_threshold(time)


class DigitalModulation(Modulation):
    """Base class for digital modulations.

    Parameters
    ----------
    bit_rate : float or callable, optional
        Bit rate of the transmission [bits/sec]
    ebno_ratio_threshold : float or callable, optional
        Eb/No threshold for demodulator to maintain error rate [dB]
    symbol_rate : float or callable, optional
        Symbol rate of the transmission [sym/sec]
    esno_ratio_threshold : float or callable, optional
        Es/No threshold for demodulator to maintain error rate [dB]
    coding_gain : float or callable, optional
        Gain due to error correction [dB]
    cno_ratio_threshold : float or callable, optional
        Threshold for the carrier to noise density for the demodulator to be
        able to demodulate the signal [dB-Hz]
    modulation_loss : float or callable, optional
        Additional loss due to the modulation technique [dB]

    Notes
    -----
    Provide either `bit_rate` and `ebno_ratio_threshold`, or `symbol_rate`
    and `esno_ratio_threshold`.
    """
    def __init__(
            self,
            bit_rate=None, ebno_ratio_threshold=None,
            symbol_rate=None, esno_ratio_threshold=None,
            coding_gain=None,
            cno_ratio_threshold=None,
            modulation_loss=None):
        super().__init__(
            cno_ratio_threshold=cno_ratio_threshold,
            modulation_loss=modulation_loss)
        if bit_rate is None and symbol_rate is None:
            raise ValueError("Bit rate or symbol rate have to be provided.")
        bit_rate = bit_rate if bit_rate is not None else symbol_rate
        self.symbol_rate = make_callable(symbol_rate)
        self.bit_rate = make_callable(bit_rate)
        if coding_gain is not None:
            if ebno_ratio_threshold is not None:
                ebno_ratio_threshold = ebno_ratio_threshold - coding_gain
            if esno_ratio_threshold is not None:
                esno_ratio_threshold = esno_ratio_threshold - coding_gain
        self.ebno_ratio_threshold = make_callable(ebno_ratio_threshold)
        self.esno_ratio_threshold = make_callable(esno_ratio_threshold)
        self.coding_gain = make_callable(coding_gain)

    def get_bit_rate(self, time=None):
        return self.bit_rate(time)

    def get_ebno_ratio_threshold(self, time=None):
        return self.ebno_ratio_threshold(time)

    def get_symbol_rate(self, time=None):
        return self.symbol_rate(time)

    def get_esno_ratio_threshold(self, time=None):
        return self.esno_ratio_threshold(time)

    def get_coding_gain(self, time=None):
        return self.coding_gain(time)


class BinaryDigitalModulation(DigitalModulation):
    """Base class for binary digital modulation.

    Parameters
    ----------
    bit_rate : float or callable, optional
        Bit rate of the data stream [bits/sec]
    bit_error_rate : float or callable, default 1e5
        Highest acceptable bit error rate
    implementation_loss : float or callable, optional
        Loss in SNR caused by the implementation of the demodulator [dB]
    cno_ratio_threshold : float or callable, optional
        Threshold for the carrier to noise density for the demodulator to be
        able to demodulate the signal [dB-Hz]
    modulation_loss : float or callable, optional
        Additional loss due to the modulation technique [dB]

    References
    ----------
    .. [1] Digital Communications, Sklar, ISBN: 0-13-084788-7, p.219
    """
    def __init__(
            self, bit_rate,
            bit_error_rate=1e-5,
            implementation_loss=0,
            cno_ratio_threshold=None,
            modulation_loss=None):
        match = root(
            lambda x: self._bit_error_rate_func(x) - bit_error_rate,
            np.array(0),
            tol=10 ** (np.log10(bit_error_rate) - 5)
        )
        ebno_ratio_threshold = float(match.x)
        ebno_ratio_threshold += implementation_loss
        super().__init__(
            bit_rate=bit_rate,
            ebno_ratio_threshold=ebno_ratio_threshold,
            cno_ratio_threshold=cno_ratio_threshold,
            modulation_loss=modulation_loss
        )

    def _bit_error_rate_func(self, ebno_db):
        raise NotImplementedError


class BPSKNoCoding(BinaryDigitalModulation):

    def _bit_error_rate_func(self, ebno_db):
        return _Q_erf((2 * from_db(ebno_db)) ** (1 / 2))


class FSKCoherentNoCoding(BinaryDigitalModulation):

    def _bit_error_rate_func(self, ebno_db):
        return _Q_erf(from_db(ebno_db) ** (1 / 2))


class FSKNonCoherentNoCoding(BinaryDigitalModulation):

    def _bit_error_rate_func(self, ebno_db):
        return 0.5 * np.exp(-0.5 * from_db(ebno_db))
