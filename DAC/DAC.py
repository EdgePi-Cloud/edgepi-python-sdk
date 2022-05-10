from DAC.DAC_Methods import DAC_Methods
import spidev
from gpiozero import LED as pin

import logging
_logger=logging.getLogger(__name__)

class EdgePi_DAC():
    def __init__ (self):
        _logger.info(f'Initializing DAC Bus')
        # Todo: SPI needs to have separate class and inherited
        self.spi = self.initialize_spi(spidev.SpiDev())
        # CS is connected on GPIO18
        self.cs = pin(18)
        self.cs.on()
        self.dac_ops = DAC_Methods()

    def initialize_spi(self, spi):
        spi.open(6, 0)
        spi.no_cs = True
        spi.max_speed_hz = 1000000
        spi.mode = 2
        return spi

    def write_voltage_channel(self, ch, voltage):
        code = self.dac_ops.voltage_to_code(voltage)
        self.cs.off()
        self.spi.tranfer(self.dac_ops.write_and_update(ch, code))
        self.cs.on()

    def close_spi(self,):
        self.spi.close()