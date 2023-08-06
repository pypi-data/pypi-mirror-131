import json
from functools import lru_cache
from urllib.request import urlopen

from skyfield.api import EarthSatellite, load, wgs84, utc
from sgp4.api import Satrec
from sgp4 import omm

from ..utils import make_callable
from .base import Geometry


class SimpleGeometry(Geometry):
    """A simple geometry that allows to specify the distance between transmitter
    and receiver, and the aspect (or alignment) of both to each other.

    Parameters
    ----------
    slant_range : float or callable
        Distance between transmitter and receiver
    tx_antenna_angle : float, optional
        Offset of the transmitter-receiver line from the transmit antenna
        boresight
    rx_antenna_angle : float, optional
        Offset of the transmitter-receiver line from the receive antenna
        boresight
    """
    def __init__(self, slant_range, tx_antenna_angle=0, rx_antenna_angle=0):
        self.slant_range = make_callable(slant_range)
        self.tx_antenna_angle = make_callable(tx_antenna_angle)
        self.rx_antenna_angle = make_callable(rx_antenna_angle)

    def get_slant_range(self, time=None):
        return self.slant_range(time)

    def get_tx_antenna_angle(self, time=None):
        return self.tx_antenna_angle(time)

    def get_rx_antenna_angle(self, time=None):
        return self.rx_antenna_angle(time)


class GroundstationSatelliteGeometry(Geometry):
    """A commonly used geometry that assumes a groundstation tracking a
    satellite.

    Parameters
    ----------
    gs_lat, gs_lon, gs_alt : float
        Groundstation latitude, longitude, and altitude above sea level
    cat_number : int, optional
        The TLE catalogue number of the satellite. If provided, the TLE will
        be fetched from Celestrak.
    tle1, tle2 : str, optional
        The two lines of an TLE set.
    omm_json : str, optional
        The OMM in JSON format as a string.
    """
    CELESTRAK_URL = "https://celestrak.com/NORAD/elements/gp.php"

    def __init__(
            self, gs_lat, gs_lon, gs_alt,
            cat_number=None, tle=None, omm_json=None):

        self.ts = load.timescale()
        if cat_number:
            with urlopen(
                    self.CELESTRAK_URL +
                    "?CATNR={}&FORMAT=TLE".format(cat_number)) as response:
                tle = response.read().decode().strip().split('\r\n')
                self.satellite = EarthSatellite(tle[1], tle[2], None, self.ts)
        elif tle:
            self.satellite = EarthSatellite(tle[1], tle[2], tle[0], self.ts)

        elif omm_json:
            json_data = json.loads(omm_json)
            sat = Satrec()
            omm.initialize(sat, json_data)
            self.satellite = EarthSatellite.from_satrec(sat, self.ts)

        else:
            raise ValueError("Provide either catalogue number, TLE or OMM")

        self.groundstation = wgs84.latlon(gs_lat, gs_lon, gs_alt)
        self.range = self.satellite - self.groundstation

    @lru_cache()
    def get_range_vector(self, time):
        t = self.ts.from_datetime(time.replace(tzinfo=utc))
        return self.range.at(t)

    @lru_cache()
    def get_slant_range(self, time):
        return self.get_range_vector(time).distance().m

    def get_tx_antenna_angle(self, time):
        return 0

    def get_rx_antenna_angle(self, time):
        return 0

    @lru_cache()
    def get_elevation_azimuth(self, time):
        elevation, azimuth, distance = self.get_range_vector(time).altaz()
        return elevation.degrees, azimuth.degrees

    def get_elevation(self, time):
        elevation, azimuth = self.get_elevation_azimuth(time)
        return elevation

    def get_azimuth(self, time):
        azimuth = self.get_elevation_azimuth(time)
        return azimuth
