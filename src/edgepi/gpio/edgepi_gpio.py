'''
Provides a class for interacting with the GPIO pins through I2C and GPIO peripheral
'''


import logging
from edgepi.gpio.edgepi_gpio_expander import EdgePiGPIOExpander
from edgepi.gpio.edgpio_gpio_chip import EdgePiGPIOChip
from edgepi.gpio.gpio_configs import GpioConfigs

_logger = logging.getLogger(__name__)

# pylint: disable=logging-too-many-args
class EdgePiGPIO(EdgePiGPIOExpander, EdgePiGPIOChip):
    '''
    A class used to represent the GPIO Expander configuration for an I2C Device.
    This class will be imported to each module that requires GPIO manipulation.
    It is not intended for users.
    '''
    def __init__(self, config: GpioConfigs = None):
        if config is None:
            raise ValueError(f'Missing Config {config}')
        _logger.debug(f'{config.name} Configuration Selected: {config}')
        if config is not None and 'i2c' in config.dev_path:
            EdgePiGPIOExpander.__init__(self, config=config)
        if config is not None and 'gpiochip0'in config.dev_path:
            EdgePiGPIOChip.__init__(self, config=config)
