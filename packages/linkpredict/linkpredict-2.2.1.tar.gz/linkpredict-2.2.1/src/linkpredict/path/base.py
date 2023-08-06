

class Geometry:
    """Abstract base class for geometries."""

    def get_slant_range(self, time=None):
        """Distance between transmitter and receiver."""
        raise NotImplementedError

    def get_tx_antenna_angle(self, time=None):
        """Antenna aspect angle of the slant range direction for the
        transmitting antenna."""
        raise NotImplementedError

    def get_rx_antenna_angle(self, time=None):
        """Antenna aspect angle of the slant range direction for the
        receiving antenna."""
        raise NotImplementedError


class MediumLoss:
    """Abstract base class for losses in the propagation medium."""

    def get_loss(self, time):
        """Get total loss from this medium [dB]."""
        raise NotImplementedError
