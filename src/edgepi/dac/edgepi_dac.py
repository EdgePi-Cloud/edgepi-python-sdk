"""
Module for interacting with the EdgePi DAC via SPI.
"""


import logging
from edgepi.dac.dac_commands import DACCommands
from edgepi.dac.dac_calibration import DAChWCalibConst, DACsWCalibConst
from edgepi.dac.dac_constants import (
    SW_RESET,
    GainMode,
    PowerMode,
    EdgePiDacChannel as CH,
    EdgePiDacCom as COM,
)
from edgepi.peripherals.spi import SpiDevice as spi


_logger = logging.getLogger(__name__)

# TODO: map analog_out number to AO EN pins


class EdgePiDAC(spi):
    """A EdgePi DAC device"""

    def __init__(self):
        _logger.info("Initializing DAC Bus")
        super().__init__(bus_num=6, dev_id=3, mode=1, max_speed=1000000)

        self.dac_ops = DACCommands(DAChWCalibConst, [DACsWCalibConst] * 8)

        self._dac_state = {
            CH.DAC7.value: PowerMode.NORMAL.value,
            CH.DAC6.value: PowerMode.NORMAL.value,
            CH.DAC5.value: PowerMode.NORMAL.value,
            CH.DAC4.value: PowerMode.NORMAL.value,
            CH.DAC3.value: PowerMode.NORMAL.value,
            CH.DAC2.value: PowerMode.NORMAL.value,
            CH.DAC1.value: PowerMode.NORMAL.value,
            CH.DAC0.value: PowerMode.NORMAL.value,
        }

    def write_voltage(self, analog_out: int, voltage: float):
        """
        Write a voltage value to an analog out pin

        Args:
            analog_out (int): the analog out pin number to write a voltage value to

            voltage (float): the voltage value to write
        """
        dac_ch = analog_out - 1
        code = self.dac_ops.voltage_to_code(dac_ch, voltage)
        self.transfer(self.dac_ops.generate_write_and_update_command(dac_ch, code))

    def set_power_mode(self, analog_out: int, power_mode: PowerMode):
        """
        Set power mode for individual DAC channels to either normal power consumption,
        or low power consumption modes.

        Args:
            analog_out (int): the analog out pin whose power mode will be changed

            power_mode (PowerMode): a valid hex code for setting DAC channel power mode
        """
        self.dac_ops.check_range(analog_out, 1, len(CH))
        dac_ch = analog_out - 1  # analog_out pins numbered 1-8, DAC channels 0-7
        self._dac_state[dac_ch] = power_mode.value
        power_code = self.dac_ops.generate_power_code(self._dac_state.values())
        cmd = self.dac_ops.combine_command(
            COM.COM_POWER_DOWN_OP.value, COM.COM_NOP.value, power_code
        )
        self.transfer(cmd)

    def set_gain_mode(self, gain_mode: GainMode):
        """
        Set EdgePi DAC output amplifier gain

        Args:
            gain_mode (GainMode): DAC output amplifier gain setting
        """
        cmd = self.dac_ops.combine_command(COM.COM_GAIN.value, COM.COM_NOP.value, gain_mode.value)
        self.transfer(cmd)

    def reset(self):
        """
        Performs a software reset of the EdgePi DAC to power-on default values.
        """
        cmd = self.dac_ops.combine_command(COM.COM_SW_RESET.value, COM.COM_NOP.value, SW_RESET)
        self.transfer(cmd)

    def read_voltage(self, analog_out: int):
        """
        Read voltage from the DAC channel corresponding to analog out pin

        Args:
            analog_out (int): the analog out pin number to read voltage from

        Returns:
            the voltage value read from the DAC channel corresponding to the
            selected analog out pin.
        """
        self.dac_ops.check_range(analog_out, 1, len(CH))
        dac_ch = analog_out - 1
        # first transfer triggers read mode, second is needed to fetch data
        cmd = self.dac_ops.combine_command(
            COM.COM_READBACK.value, CH(dac_ch).value, COM.COM_NOP.value
        )
        self.transfer(cmd)
        # all zero dummy command to trigger second transfer which
        # contains the DAC register contents.
        read_data = self.transfer([0, 0, 0])
        _logger.debug(f"reading code {read_data}")
        code = self.dac_ops.extract_read_data(read_data)
        return self.dac_ops.code_to_voltage(dac_ch, code)
