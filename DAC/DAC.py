from DAC.DAC_Methods import DAC_Methods
from periphery import SPI

import logging
_logger=logging.getLogger(__name__)

class EdgePi_DAC():
    def __init__ (self):
        _logger.info(f'Initializing DAC Bus')
        # Todo: SPI needs to have separate class and inherited
        self.spi = self.initialize_spi(SPI)
        # CS is connected on GPIO18
        self.dac_ops = DAC_Methods()

    def initialize_spi(self, spi):
        # Bus 6 dev 2, mode 1, max_freq = 1MHz
        return SPI("/dev/spidev6.2", 1, 1000000)

    def write_voltage_channel(self, ch, voltage):
        code = self.dac_ops.voltage_to_code(voltage)
        self.spi.tranfer(self.dac_ops.generate_write_and_update_command(ch, code))

    def close_spi(self,):
        self.spi.close()