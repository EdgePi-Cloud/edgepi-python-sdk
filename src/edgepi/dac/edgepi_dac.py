"""
Module for interacting with the EdgePi DAC via SPI.
"""


import logging
from edgepi.dac.dac_commands import DACCommands
from edgepi.dac.dac_calibration import DAChWCalibConst, DACsWCalibConst
from edgepi.peripherals.spi import SpiDevice as spi


_logger = logging.getLogger(__name__)


class EdgePiDAC(spi):
    ''' A EdgePi DAC device '''
    def __init__(self):
        _logger.info("Initializing DAC Bus")
        super().__init__(bus_num=6, dev_id=3, mode=1, max_speed=1000000)

        self.dac_ops = DACCommands(DAChWCalibConst, [DACsWCalibConst] * 8)

    def write_voltage_channel(self, ch, voltage):
        ''' Write a voltage value to a DAC channel '''
        # TODO: fix missing expected arg
        # pylint: disable=no-value-for-parameter
        code = self.dac_ops.voltage_to_code(voltage)
        self.transfer(self.dac_ops.generate_write_and_update_command(ch, code))
