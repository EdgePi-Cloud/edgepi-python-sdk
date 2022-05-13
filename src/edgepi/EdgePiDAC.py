from edgepi.dac.DAC_Commands import DACCommands
from edgepi.peripherals.Peripherals import SpiDevice as spi

import logging
_logger=logging.getLogger(__name__)

class EdgePiDAC(spi):
    def __init__ (self):
        _logger.info(f'Initializing DAC Bus')
        super().__init__(dev_path='/dev/spidev6.3', mode = 1, max_speed=1000000)
        self.dac_ops = DACCommands()

    def write_voltage_channel(self, ch, voltage):
        code = self.dac_ops.voltage_to_code(voltage)
        self.transfer(self.dac_ops.generate_write_and_update_command(ch, code))

    def close_spi(self,):
        self.close()