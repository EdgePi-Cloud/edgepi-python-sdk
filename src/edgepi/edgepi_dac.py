from edgepi.dac.dac_commands import DACCommands
from edgepi.dac.dac_calibration import DACHwCalib_const, DACSwCalib_const
from edgepi.peripherals.spi import SpiDevice as spi

import logging
_logger=logging.getLogger(__name__)

class EdgePiDAC(spi):
    def __init__ (self):
        _logger.info(f'Initializing DAC Bus')
        super().__init__(bus_num=6, dev_ID=3, mode = 1, max_speed=1000000)

        self.dac_ops = DACCommands(DACHwCalib_const, [DACSwCalib_const]*8)

    def write_voltage_channel(self, ch, voltage):
        code = self.dac_ops.voltage_to_code(voltage)
        self.transfer(self.dac_ops.generate_write_and_update_command(ch, code))