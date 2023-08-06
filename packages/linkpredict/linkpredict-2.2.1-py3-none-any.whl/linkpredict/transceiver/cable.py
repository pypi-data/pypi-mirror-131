from scipy.interpolate import interp1d

from ..utils import from_db
from .device import Device


# from
# <https://web.archive.org/web/20050729110806/http://www.meteorscatter.net:80/cable.htm>
_CABLE_DATABASE = {
    "Aircom+": {144e+6: 4.5 / 100, 432e+6: 8.2 / 100, 1296e+6: 14.5 / 100},
    "Aircell 7": {50e+6: 4.8 / 100, 144e+6: 7.9 / 100, 432e+6: 14.1 / 100,
                  1296e+6: 26.1 / 100},
    "Ecoflex 10": {144e+6: 4.8 / 100, 432e+6: 8.9 / 100, 1296e+6: 16.5 / 100},
    "Ecoflex 15": {50e+6: 1.96 / 100, 144e+6: 3.4 / 100, 432e+6: 6.1 / 100,
                   1296e+6: 11.4 / 100},
    "H 100": {50e+6: 2.8 / 100, 144e+6: 4.9 / 100, 432e+6: 8.8 / 100,
              1296e+6: 16.0 / 100},
    "H 155": {50e+6: 6.5 / 100, 144e+6: 11.2 / 100, 432e+6: 19.8 / 100,
              1296e+6: 34.9 / 100},
    "H 500": {50e+6: 2.9 / 100, 1296e+6: 17.4 / 100},
    "H 2000 flex": {50e+6: 2.7 / 100, 144e+6: 4.8 / 100, 432e+6: 8.5 / 100,
                    1296e+6: 15.7 / 100},
    "RG 55": {144e+6: 18.5 / 100, 432e+6: 34.0 / 100, 1296e+6: 60.0 / 100},
    "RG 58 CU": {50e+6: 11.0 / 100, 144e+6: 20.0 / 100, 432e+6: 40.0 / 100,
                 1296e+6: 90.0 / 100},
    "RG 174 U": {144e+6: 34.0 / 100, 432e+6: 60.0 / 100, 1296e+6: 110.0 / 100},
    "RG 213 U": {50e+6: 4.3 / 100, 144e+6: 8.2 / 100, 432e+6: 15.0 / 100,
                 1296e+6: 26.0 / 100},
    "RG 223 U": {144e+6: 18.5 / 100, 432e+6: 34.0 / 100, 1296e+6: 60.0 / 100},
    "Cellflex 1/4": {144e+6: 5.5 / 100, 432e+6: 9.0 / 100, 1296e+6: 18.0 / 100},
    "Cellflex 3/8": {144e+6: 3.8 / 100, 432e+6: 6.5 / 100, 1296e+6: 13.0 / 100},
    "Cellflex 1/2": {144e+6: 3.0 / 100, 432e+6: 5.6 / 100, 1296e+6: 10.0 / 100},
    "Cellflex 5/8": {144e+6: 2.5 / 100, 432e+6: 4.0 / 100, 1296e+6: 7.2 / 100},
}


class Cable(Device):
    """Cable specializes the Device class for radio cables.

    Parameters
    ----------
    loss_per_length : Loss per length of the cable [dB/m]
    length : Length of the cable [m]
    ambient_temperature : Ambient temperature or real temperature
                          of the cable [K]
    """
    def __init__(self, loss_per_length, length, ambient_temperature=290):
        loss = loss_per_length * length
        noise_temperature = ambient_temperature * (1 - from_db(-loss))
        super().__init__(gain=-loss, noise_temperature=noise_temperature)

    @classmethod
    def from_database(cls, cable_type, frequency, length,
                      ambient_temperature=290):
        """Create a Cable instance with a loss_per_length from the
        included cable database.

        Parameters
        ----------
        cable_type : Cable type from the database
        frequency : Frequency of the signal [Hz]
        length : Length of the cable [m]
        ambient_temperature : Ambient temperature or real temperature
                              of the cable [K]
        """
        if cable_type not in _CABLE_DATABASE:
            raise ValueError("Cable type not found in database")
        cable_spec = _CABLE_DATABASE[cable_type]
        freq = sorted(cable_spec.keys())
        lpls = [cable_spec[k] for k in freq]
        lpl = interp1d(
            freq, lpls, kind='slinear', fill_value='extrapolate',
            assume_sorted=True)(frequency)
        return cls(
            loss_per_length=lpl, length=length,
            ambient_temperature=ambient_temperature)
