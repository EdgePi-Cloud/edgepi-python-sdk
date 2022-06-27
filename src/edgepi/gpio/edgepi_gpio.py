'''
Provides a class for interacting with the GPIO pins through I2C and GPIO peripheral
'''

import logging
import time

from edgepi.peripherals.gpio import GpioDevice
from edgepi.peripherals.i2c import I2CDevice
from edgepi.gpio.gpio_commands import *

_logger = logging.getLogger(__name__)

class EdgePiGPIO(I2CDevice):
    ''' 
    A class used to represent the GPIO. This class will be imported to each module
    that requires GPIO manipulation. It is not intended for user.
    '''
    
    def __init__(self, config: str = None):
        if config is None:
            _logger.error(f'Config is not chosen, please choose a configuration')
        self.config = getPeriphConfig(config)
        _logger.debug(f'{self.config.name} Configuration Selected: {self.config}')
        if self.config is not None and 'i2c' in self.config.dev_path:
            super().__init__(self.config.dev_path)
            _logger.info(f'GPIO expander up and running')
            self.pinList = generate_pin_info(self.config.name)