import spidev
from gpiozero import LED as pin
from DAC_REG import EDGEPI_DAC_ADDRESS as address
from DAC_REG import EDGEPI_DAC_COM as command

import logging
logging.basicConfig(level=logging.INFO)
_logger=logging.getLogger(__name__)

class EdgePi_DAC():
    def __init__ (self):
        self.spi = spidev.SpiDev()
        self.spi.open(6, 0)
        self.spi.no_cs = True
        self.spi.max_speed_hz = 1000000
        self.spi.mode = 2
        # CS is connected on GPIO18
        self.cs = pin(18)
        self.cs.on()

    def combine_command(self, op_code, ch, value):
        temp = op_code<<20 + ch<<16 + value
        list = [temp>>16, (temp>>8)&0xFF, temp&0xFF]
        return list

    def write_and_update(self, ch, data):
        command = self.combine_command(command.COM_WRITE_UPDATE.value, address(ch).value)
        self.cs.off()
        self.spi.xfer(command)
        self.cs.on()

    def sw_reset(self):
        command = self.combine_command(command.COM_SW_RESET, 0, 4660)
        self.cs.off()
        self.spi.xfer(command)
        self.cs.on()

        

