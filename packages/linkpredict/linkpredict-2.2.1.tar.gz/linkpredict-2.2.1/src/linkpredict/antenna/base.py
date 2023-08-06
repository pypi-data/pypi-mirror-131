

class Antenna:
    """Abstract base class for antennas."""

    def is_linear_polarized(self):
        """Returns True if antenna is linear polarized, otherwise False."""
        raise NotImplementedError

    def get_gain(self, angle, time):
        """Returns the gain of the antenna with respect to a perfect isotropic
        radiating antenna [dBi].

        Parameters
        ----------
        angle : float, optional
            The angle in [deg] from boresight direction at which to evaluate
            the gain.
        time : datetime, optional
            The instance of time at which to evaluate the expression.
        """
        raise NotImplementedError


class AntennaNoise:
    """Abstract base class for antenna noise."""

    def get_noise_temperature(self, time):
        """Returns the effective noise temperature of the antenna [K]."""
        raise NotImplementedError
