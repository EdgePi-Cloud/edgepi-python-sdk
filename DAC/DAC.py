import spidev
from gpiozero import LED as pin
from DAC_REG import EDGEPI_DAC_ADDRESS as ADDRESS
from DAC_REG import EDGEPI_DAC_COM as COMMAND

import logging
logging.basicConfig(level=logging.INFO)
_logger=logging.getLogger(__name__)

VOLTAGE_REF = 2.047
RANGE = 65536

class EdgePi_DAC():
    def __init__ (self):
        _logger.info(f'Initializing DAC Bus')
        self.spi = spidev.SpiDev()
        self.spi.open(6, 0)
        self.spi.no_cs = True
        self.spi.max_speed_hz = 1000000
        self.spi.mode = 2
        # CS is connected on GPIO18
        self.cs = pin(18)
        self.cs.on()

    def combine_command(self, op_code, ch, value):
        temp = (op_code<<20) + (ch<<16) + value
        list = [temp>>16, (temp>>8)&0xFF, temp&0xFF]
        _logger.debug(f'Combined Command is: {list}')
        return list

    def write_and_update(self, ch, data):
        command = self.combine_command(COMMAND.COM_WRITE_UPDATE.value, ADDRESS(ch).value, data)
        _logger.info(f'Write and update')
        self.cs.off()
        self.spi.xfer(command)
        self.cs.on()
        _logger.debug(f'Written and updated with {command}')

    def sw_reset(self):
        command = self.combine_command(COMMAND.COM_SW_RESET.value, 0, 4660)
        _logger.info(f'SW Reset')
        self.cs.off()
        self.spi.xfer(command)
        self.cs.on()

    def write_voltage_channel(self, ch, voltage):
        code = self.voltage_to_code(voltage)
        self.write_and_update(ch, code)

#ToDo: change the formula according to calibration if needed
    def voltage_to_code(self, expected):
        code = expected * (RANGE/VOLTAGE_REF)
        return code