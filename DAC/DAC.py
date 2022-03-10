import spidev
from gpiozero import LED as pin
from DAC_REG import EDGEPI_DAC_ADDRESS as address
from DAC_REG import EDGEPI_DAC_COM as command

import logging
logging.basicConfig(level=logging.INFO)
_logger=logging.getLogger(__name__)

VOLTAGE_REF = 2.047
RANGE = 65536

class EdgePi_DAC():
    def __init__ (self):
        self.spi = spidev.SpiDev()
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
        self.spi.open(6, 0)
        self.cs.off()
        self.spi.xfer(command)
        self.cs.on()
        self.spi.close()

    def sw_reset(self):
        command = self.combine_command(command.COM_SW_RESET, 0, 4660)
        self.spi.open(6, 0)
        self.cs.off()
        self.spi.xfer(command)
        self.cs.on()
        self.spi.close()

    def write_voltage_channel(self, ch, voltage):
        code = self.voltage_to_code(voltage)
        self.write_and_update(ch, code)

#ToDo: change the formula according to calibration if needed
    def voltage_to_code(self, expected):
        code = expected * (RANGE/VOLTAGE_REF)
        return code