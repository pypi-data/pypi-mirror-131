from datetime import timedelta
from enum import Enum, unique

import numpy as np
from scipy.constants import nu2lambda
from scipy.constants import Boltzmann as k_B  # [W*s/K]

from .utils import to_db, make_callable
from .channel import Modulation, AnalogModulation, DigitalModulation


@unique
class LinkBudgetKeys(Enum):
    """The :class:`LinkBudgetKeys` enum contains the keys of the dictionaries that
    are produced by the link budget calculation. Using the keys, one can
    access portion of the generated data as needed.

    >>> result = link.get_link_budget()
    >>> print(result[LinkBudgetKeys.eirp])

    """
    time = ("Time of calculation", "datetime")
    tx_amplifier_power = ("Transmitter amplifier power output", "dBW")
    tx_circuit_loss = ("Total transmitter circuit loss", "dB")
    tx_antenna_angle = ("Antenna angle at transmitter", "deg")
    tx_antenna_gain = ("Transmit antenna gain", "dBi")
    eirp = ("Effective isotropic radiant power", "dBW")
    tx_antenna_pointing_loss = ("Transmit antenna pointing loss", "dB")
    medium_loss = ("Total medium loss", "dB")
    slant_range = ("Slant range", "m")
    power_flux_density = (
        "Power flux density at receiver distance", "dBW/m^2")
    power_flux_density_limit = ("Power flux density limit", "dBW/m^2")
    power_flux_density_margin = (
        "Power flux density margin below limit", "dB")
    free_space_path_loss = ("Free space path loss", "dB")
    total_path_loss = ("Total path loss", "dB")
    received_isotropic_signal_level = (
        "Isotropic signal level at receiver side", "dB")
    rx_antenna_angle = ("Antenna angle at receiver", "deg")
    rx_antenna_gain = ("Receiver antenna gain", "dBi")
    rx_antenna_pointing_loss = ("Receive antenna pointing loss", "dB")
    rx_circuit_loss = ("Total receiver circuit loss", "dB")
    received_power = ("Received signal power", "dBW")
    received_power_threshold = ("Received signal power threshold", "dBW")
    received_power_margin = ("Received signal power margin", "dB")
    rx_antenna_noise_temperature = (
        "Receiver antenna noise temperature", "K")
    rx_system_noise_temperature = (
        "Receiver system noise temperature", "K")
    received_noise_power_density = (
        "Received noise power density", "dBW/Hz")
    g_t_figure_of_merit = ("G/T figure of merit for the receiver", "dB/K")
    rx_elevation = ("Elevation of path to transmitter at receiver", "deg")
    cno_ratio = ("Carrier to noise density ratio", "dB-Hz")
    cno_ratio_threshold = (
        "Carrier to noise density ratio threshold", "dB-Hz")
    cno_ratio_margin = ("Carrier to noise density ratio margin", "dB")
    modulation_loss = (
        "Total additional loss due to modulation schema", "dB")
    bandwidth = ("Bandwidth at receiver", "Hz")
    received_noise_power = ("Received noise power", "dBW")
    snr = ("Signal to noise ratio of the base band", "dB")
    snr_threshold = (
        "Signal to noise ratio of the base band threshold", "dB")
    snr_margin = ("Signal to noise ratio of the base band margin", "dB")
    symbol_rate = ("Symbol rate of data", "sym/s")
    bit_rate = ("Bit rate of data", "bit/s")
    esno_ratio = ("Symbol energy to noise density ratio", "dB")
    esno_ratio_threshold = (
        "Symbol energy to noise density ratio threshold", "dB")
    esno_ratio_margin = (
        "Symbol energy to noise density ratio margin", "dB")
    ebno_ratio = ("Bit energy to noise density ratio", "dB")
    ebno_ratio_threshold = (
        "Bit energy to noise density ratio threshold", "dB")
    ebno_ratio_margin = ("Bit energy to noise density ratio margin", "dB")
    coding_gain = ("Reduction of threshold due to error correction", "dB")

    def __init__(self, description, unit):
        self.description = description
        self.unit = unit

    def __repr__(self):
        return "<{}.{} [{}]>".format(
            self.__class__.__name__, self.name, self.unit)

    def __str__(self):
        return "{} [{}]".format(self.name, self.unit)


class Link:
    """Link budget calculations.

    The :class:`Link` class contains all elements that compose a link.

    Parameters
    ----------
    channel : :class:`Channel`
        Physical channel through which the communication takes place
    geometry : :class:`Geometry`
        Geometry between transmitter and receiver
    transmitter : :class:`Transmitter`
        Compound of elements that form a transmitter
    transmit_antenna : :class:`Antenna`
        Antenna used for transmission
    medium_losses: list of :class:`MediumLoss`
        List of losses in the propagation
    receive_antenna : :class:`Antenna`
        Antenna used for reception
    receive_antenna_noise : :class:`AntennaNoise`
        Noise at the receiving antenna
    receiver : :class:`Receiver`
        Compound of elements that form a receiver
    """

    def __init__(
            self,
            channel,
            geometry,
            transmitter,
            transmit_antenna,
            receive_antenna,
            receive_antenna_noise,
            receiver,
            medium_losses=None):
        self.channel = make_callable(channel)
        self.geometry = make_callable(geometry)
        self.transmitter = make_callable(transmitter)
        self.transmit_antenna = make_callable(transmit_antenna)
        if medium_losses is None:
            medium_losses = []
        self.medium_losses = make_callable(medium_losses)

        # Receiver components
        self._reduced_setup = False
        self.receive_antenna = make_callable(receive_antenna)
        self.receiver_antenna_noise = make_callable(receive_antenna_noise)
        self.receiver = make_callable(receiver)

    @classmethod
    def from_g_t_figure(
            cls,
            channel,
            geometry,
            transmitter,
            transmit_antenna,
            rx_g_t_figure,
            is_rx_linear_polarized,
            rx_antenna_pointing_loss,
            medium_losses=None):
        """Construct a :class:`Link` instance using the G/T figure for the
        receiving side instead of specifying the individual receiver
        components.

        Parameters
        ----------
        channel : :class:`Channel`
            Physical channel through which the communication takes place
        geometry : :class:`Geometry`
            Geometry between transmitter and receiver
        transmitter : :class:`Transmitter`
            Compound of elements that form a transmitter
        transmit_antenna : :class:`Antenna`
            Antenna used for transmission
        medium_losses: list of :class:`MediumLoss`
            List of losses in the propagation
        rx_g_t_figure : float or callable
            Receiver station figure of merit [dB/K]
        is_rx_linear_polarized : boolean
            Whether the receiver antenna is linear polarized
        rx_antenna_pointing_loss : float or callable
            Loss due to off pointing of the receive antenna [dB]

        Returns
        -------
        link : :class:`Link`
            An instance of the :class:`Link` class.
        """

        self = cls.__new__(cls)
        self.channel = make_callable(channel)
        self.geometry = make_callable(geometry)
        self.transmitter = make_callable(transmitter)
        self.transmit_antenna = make_callable(transmit_antenna)
        if medium_losses is None:
            medium_losses = []
        self.medium_losses = make_callable(medium_losses)

        self._reduced_setup = True
        self.rx_g_t_figure = make_callable(rx_g_t_figure)
        self.is_rx_linear_polarized = make_callable(is_rx_linear_polarized)
        self.rx_antenna_pointing_loss = make_callable(rx_antenna_pointing_loss)

        return self

    def calculate_link_budget(
            self, time_start=None, time_end=None,
            time_step=timedelta(minutes=1)):
        """Calculate the link budget.

        If only `time_start` is provided, the link budget will be calculated
        for that instance of time and returned as a dict. If there is no
        time-dependent factor in the link budget then `time_start` can be
        ommitted to get a static result.

        To run calculations over a time range, provide `time_start` and
        `time_end`. The return is then a list of results, each computed at
        a time instance in that range, starting from `time_start` and increased
        stepwise increased by `time_step`.

        Parameters
        ----------
        time_start : datetime, optional
            Start time for link budget calculations over a time range
        time_end: datetime, optional
            Start time for link budget calculations over a time range
        time_step: timedelta, optional
            The interval for the calculation time range

        Returns
        -------
        link_budget : dict or list of dict
            The calculated link budget values for each instance of time. The
            index keys of the returned dict are defined
            by :class:`LinkBudgetKeys`.
        """

        if time_start is None:
            return self._calculate_link_budget_instance()
        elif time_end is None:
            return self._calculate_link_budget_instance(time_start)
        else:
            if time_start > time_end:
                raise ValueError("Start time must be before end time.")
            current_time = time_start
            link_budget = []
            while current_time <= time_end:
                link_budget.append(
                    self._calculate_link_budget_instance(current_time)
                )
                current_time += time_step
            return link_budget

    def _calculate_link_budget_instance(self, time=None):
        """Calculate a single instance of the link budget.

        Parameters
        ----------
        time : datetime, optional
            The time to use for the time-dependent factors of
            the link budget. Use `None` if no values are time-dependent.

        Returns
        -------
        result : dict
            A `dict` with the results. The `dict` keys are provided
            by :class:`LinkBudgetKeys`.
        """

        k = LinkBudgetKeys
        result = dict()

        # Time
        result[k.time] = time

        # Transmitter
        tx_amplifier_power = self.transmitter(time).get_amplifier_power(time)
        tx_circuit_gain = self.transmitter(time).get_line_gain(time)
        tx_antenna_angle = self.geometry(time).get_tx_antenna_angle(time)
        tx_antenna_gain = self.transmit_antenna(time).get_gain(0, time)
        tx_antenna_pointing_loss = (tx_antenna_gain
                                    - (self.transmit_antenna(time)
                                       .get_gain(tx_antenna_angle, time))
                                    )
        eirp = tx_amplifier_power + tx_circuit_gain + tx_antenna_gain
        result[k.tx_amplifier_power] = tx_amplifier_power
        result[k.tx_circuit_loss] = -tx_circuit_gain
        result[k.tx_antenna_angle] = tx_antenna_angle
        result[k.tx_antenna_gain] = tx_antenna_gain
        result[k.tx_antenna_pointing_loss] = tx_antenna_pointing_loss
        result[k.eirp] = eirp

        # Propagation
        medium_loss = sum(m.get_loss(time) for m in self.medium_losses(time))
        slant_range = self.geometry(time).get_slant_range(time)
        free_space_spreading = self._free_space_spreading(slant_range)
        pfd = eirp - medium_loss - free_space_spreading
        pfd_limit = self.channel(time).pfd_limit(time)
        result[k.medium_loss] = medium_loss
        result[k.slant_range] = slant_range
        result[k.power_flux_density] = pfd
        result[k.power_flux_density_limit] = pfd_limit

        if pfd_limit is not None:
            pfd_margin = pfd_limit - pfd
            result[k.power_flux_density_margin] = pfd_margin

        free_space_path_loss = self._free_space_path_loss(
            slant_range, self.channel(time).get_frequency(time))
        polarization_mismatch_loss = self._get_polarization_mismatch_loss(time)
        total_path_loss = (
            free_space_path_loss + medium_loss + polarization_mismatch_loss)
        result[k.free_space_path_loss] = free_space_path_loss
        result[k.total_path_loss] = total_path_loss

        # Receiver
        received_isotropic_signal_level = (eirp
                                           - total_path_loss
                                           - tx_antenna_pointing_loss
                                           )
        result[k.received_isotropic_signal_level] = \
            received_isotropic_signal_level

        if not self._reduced_setup:
            rx_antenna_angle = self.geometry(time).get_rx_antenna_angle(time)
            rx_antenna_gain = self.receive_antenna(time).get_gain(0, time)
            rx_antenna_pointing_loss = (rx_antenna_gain
                                        - (self.receive_antenna(time)
                                           .get_gain(rx_antenna_angle, time))
                                        )
            rx_circuit_gain = self.receiver(time).get_line_gain(time)
            received_power = (received_isotropic_signal_level
                              - rx_antenna_pointing_loss
                              + rx_antenna_gain
                              + rx_circuit_gain
                              )
            received_power_threshold = \
                self.channel(time).get_received_power_threshold(time)
            result[k.rx_antenna_angle] = rx_antenna_angle
            result[k.rx_antenna_gain] = rx_antenna_gain
            result[k.rx_antenna_pointing_loss] = rx_antenna_pointing_loss
            result[k.rx_circuit_loss] = -rx_circuit_gain
            result[k.received_power] = received_power
            result[k.received_power_threshold] = received_power_threshold

            if received_power_threshold is not None:
                received_power_margin = (received_power
                                         - received_power_threshold
                                         )
                result[k.received_power_margin] = received_power_margin

            rx_antenna_noise_temp = \
                self.receiver_antenna_noise(time).get_noise_temperature(time)
            result[k.rx_antenna_noise_temperature] = rx_antenna_noise_temp
            rx_circuit_temp = \
                self.receiver(time).get_system_noise_temperature(time)
            rx_system_noise_temp = rx_antenna_noise_temp + rx_circuit_temp
            result[k.rx_system_noise_temperature] = rx_system_noise_temp
            received_noise_power_density = \
                self._noise_power_density(rx_system_noise_temp)
            result[k.received_noise_power_density] = \
                received_noise_power_density
            rx_g_t = (rx_antenna_gain
                      + rx_circuit_gain
                      - to_db(rx_system_noise_temp)
                      )

        else:
            rx_g_t = self.rx_g_t_figure(time)
            rx_antenna_pointing_loss = self.rx_antenna_pointing_loss(time)
            result[k.rx_antenna_pointing_loss] = rx_antenna_pointing_loss
            received_noise_power_density = None

        result[k.g_t_figure_of_merit] = rx_g_t

        # C/No
        cno_r = (received_isotropic_signal_level
                 - rx_antenna_pointing_loss
                 + rx_g_t
                 - to_db(k_B)
                 )
        result[k.cno_ratio] = cno_r

        # Modulation and coding
        modulation = self.channel(time).modulation(time)
        if modulation is not None:
            if not isinstance(modulation, Modulation):
                TypeError(
                    "Modulation must be an instance of the Modulation class")
            modulation_loss = modulation.get_modulation_loss(time)
            result[k.modulation_loss] = modulation_loss
            if modulation_loss is not None:
                cno_r = cno_r - modulation_loss
                result[k.cno_ratio] = cno_r
                if result.get(k.received_power) is not None:
                    received_power = result[k.received_power] - modulation_loss
                    result[k.received_power] = received_power
                    if result.get(k.received_power_threshold) is not None:
                        received_power_margin = (
                                received_power
                                - result[k.received_power_threshold]
                        )
                        result[k.received_power_margin] = received_power_margin
            cno_r_threshold = modulation.get_cno_ratio_threshold(time)
            result[k.cno_ratio_threshold] = cno_r_threshold
            if cno_r_threshold is not None:
                cno_r_margin = cno_r - cno_r_threshold
                result[k.cno_ratio_margin] = cno_r_margin
            # Analog modulation
            if isinstance(modulation, AnalogModulation):
                bandwidth = modulation.get_bandwidth(time)
                result[k.bandwidth] = bandwidth
                if bandwidth is not None:
                    if received_noise_power_density is not None:
                        received_noise_power = (
                            received_noise_power_density + to_db(bandwidth))
                        result[k.received_noise_power] = received_noise_power
                    snr = cno_r - to_db(bandwidth)
                    result[k.snr] = snr
                    snr_threshold = modulation.get_snr_threshold(time)
                    result[k.snr_threshold] = snr_threshold
                    if snr_threshold is not None:
                        snr_margin = snr - snr_threshold
                        result[k.snr_margin] = snr_margin
            # Digital modulation
            elif isinstance(modulation, DigitalModulation):
                symbol_rate = modulation.get_symbol_rate(time)
                result[k.symbol_rate] = symbol_rate
                if symbol_rate is not None:
                    esno_ratio = cno_r - to_db(symbol_rate)
                    result[k.esno_ratio] = esno_ratio
                    esno_ratio_threshold = \
                        modulation.get_esno_ratio_threshold(time)
                    result[k.esno_ratio_threshold] = esno_ratio_threshold
                    if esno_ratio_threshold is not None:
                        esno_ratio_margin = esno_ratio - esno_ratio_threshold
                        result[k.esno_ratio_margin] = esno_ratio_margin
                bit_rate = modulation.get_bit_rate(time)
                result[k.bit_rate] = bit_rate
                ebno_ratio = cno_r - to_db(bit_rate)
                result[k.ebno_ratio] = ebno_ratio
                ebno_ratio_threshold = \
                    modulation.get_ebno_ratio_threshold(time)
                result[k.ebno_ratio_threshold] = ebno_ratio_threshold
                if ebno_ratio_threshold is not None:
                    ebno_ratio_margin = ebno_ratio - ebno_ratio_threshold
                    result[k.ebno_ratio_margin] = ebno_ratio_margin
                result[k.coding_gain] = modulation.get_coding_gain(time)
        return result

    @staticmethod
    def _free_space_spreading(slant_range):
        """Calculate the free space spreading for a given slant range.

        Parameters
        ----------
        slant_range: float
            Slant range of the path

        Returns
        -------
        Logarithmic spreading factor [dBm^2]
        """

        return to_db(4 * np.pi * slant_range ** 2)

    @staticmethod
    def _free_space_path_loss(slant_range, frequency):
        """Calculate the free space path loss.

        Parameters
        ----------
        slant_range : float
            Slant range of the path [m]
        frequency : float
            Frequency of the radio link [Hz]

        Returns
        -------
        Signal strength loss [dB]
        """

        wavelength = nu2lambda(frequency)
        return 2 * to_db(4 * np.pi * slant_range / wavelength)

    def _get_polarization_mismatch_loss(self, time):
        """Determine mismatch loss due to a transition from linear to
        circular polarization (or vice versa).

        Returns
        -------
        Polarization loss [dB]

        Notes
        -----
        Currently this implementation is rather crude and simply returns 3 dB
        for a polarization mismatch and 0 dB otherwise.
        """

        tx_linear = self.transmit_antenna(time).is_linear_polarized()
        if not self._reduced_setup:
            rx_linear = self.receive_antenna(time).is_linear_polarized()
        else:
            rx_linear = self.is_rx_linear_polarized(time)
        if (tx_linear and not rx_linear) or (rx_linear and not tx_linear):
            polarization_mismatch_loss = 3
        else:
            polarization_mismatch_loss = 0
        return polarization_mismatch_loss

    @staticmethod
    def _noise_power_density(system_temperature):
        """Calculate noise power density from systemtemperature.

        Parameters
        ----------
        system_temperature: float
            System temperature [K]

        Returns
        -------
        Noise power density [dBW/Hz]
        """

        return to_db(system_temperature * k_B)
