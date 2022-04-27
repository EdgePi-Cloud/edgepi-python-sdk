from DAC.DAC_Methods import DAC_Methods
import spidev
from gpiozero import LED as pin
from DAC_methods import DAC_methods

import logging
logging.basicConfig(level=logging.INFO)
_logger=logging.getLogger(__name__)

VOLTAGE_REF = 2.047
RANGE = 65536

class EdgePi_DAC():
    def __init__ (self):
        _logger.info(f'Initializing DAC Bus')
        self.spi = self.initialize_spi(spidev.SpiDev())
        # CS is connected on GPIO18
        self.cs = pin(18)
        self.cs.on()
        dac_ops = DAC_Methods()

    def initialize_spi(self, spi):
        spi.open(6, 0)
        spi.no_cs = True
        spi.no_cs = True
        spi.max_speed_hz = 1000000
        spi.mode = 2
        return spi

    def write_voltage_channel(self, ch, voltage):
        code = self.voltage_to_code(voltage)
        self.write_and_update(ch, code)
