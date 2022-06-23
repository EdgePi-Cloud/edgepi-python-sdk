from edgepi.peripherals.gpio import GpioDevice
from edgepi.peripherals.i2c import I2CDevice
from edgepi.gpio.gpio_constants import *

class GPIOCommands(I2CDevice):
    def __init__(self, pinList: list = None):
        self.gpioPinDict = {}
        self.i2cPinList  = {}
        for pin in pinList:
            if GPIOCommands._gpioSettings[pin][0] == 'gpio':
                self.gpioPinList[pin] = GpioDevice(pin_num=GPIOCommands._gpioSettings[pin][1], 
                                                   pin_dir=GPIOCommands._gpioSettings[pin][2],
                                                   pin_bias=GPIOCommands._gpioSettings[pin][3])
            else:
                self.i2cPinList[pin] = GPIOCommands._gpioSettings[pin]
        self.i2cDev = super().__init__(fd='/dev/i2c-10') if self.i2cPinList else None
        self.setDefaults()
            
    def _read_regs_map(self):
        reg_map = {}
        if 'PORTA' in self.i2cPinList
            
    def setDefaults(self):
