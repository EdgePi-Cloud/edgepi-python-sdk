"""
Module for interacting with the EdgePi DAC via SPI.
"""


import logging
from edgepi.dac.dac_commands import DACCommands
from edgepi.dac.dac_calibration import DAChWCalibConst, DACsWCalibConst
from edgepi.dac.dac_constants import PowerMode, EdgePiDacChannel as CH, EdgePiDacCom as COM
from edgepi.peripherals.spi import SpiDevice as spi


_logger = logging.getLogger(__name__)


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

    def write_voltage_channel(self, ch, voltage):
        """Write a voltage value to a DAC channel"""
        # TODO: fix missing expected arg
        # pylint: disable=no-value-for-parameter
        code = self.dac_ops.voltage_to_code(voltage)
        self.transfer(self.dac_ops.generate_write_and_update_command(ch, code))

    def set_power_mode(self, analog_out, power_mode: PowerMode):
        """
        Set power mode for individual DAC channels to either normal power consumption,
        or low power consumption modes.

        Args:
            analog_out (int): the analog out pin number to write a voltage value to

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
