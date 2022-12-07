'''
Provides a class for interacting with the GPIO pins through I2C and GPIO peripheral
'''


import logging
from edgepi.gpio.edgepi_gpio_expander import EdgePiGPIOExpander
from edgepi.gpio.edgepi_gpio_chip import EdgePiGPIOChip

_logger = logging.getLogger(__name__)

class PinNameError(Exception):
    """Raised when
        1. pin name doesn't exists
        2. pin name not passeds
    """

class EdgePiGPIO(EdgePiGPIOExpander, EdgePiGPIOChip):
    '''
    A class used to represent the GPIO Expander configuration for an I2C Device.
    This class will be imported to each module that requires GPIO manipulation.
    It is not intended for users.
    '''
    def __init__(self):
        _logger.info("GPIO initializing")
        EdgePiGPIOExpander.__init__(self)
        EdgePiGPIOChip.__init__(self)

    def read_pin_state(self, pin_name: str = None):
        """
        Read corresponding pin state
        Args:
            pin_name (str): name of the pin will be passed as Enum
        return
            state (bool): True/False depending on High/Low
        """

        if pin_name in self.expander_pin_dict:
            return self.read_expander_pin(pin_name)
        if pin_name in self.gpiochip_pins_dict:
            return self.read_gpio_pin_state(pin_name)

        raise PinNameError(f'The following pin name: {pin_name} is not found')


    def write_pin_state(self, pin_name: str = None, state: bool = None):
        """
        Write pin state to corresponding pin
        Args:
            pin_name(str): name of the pin will be passed as Enum
            state (bool): state to write to the pin. True = High, False = Low
        return:
            pin_state (bool): written state of the pin True = High, False = Low
        """
        if pin_name in self.expander_pin_dict:
            return self.set_expander_pin(pin_name)
        if pin_name in self.gpiochip_pins_dict:
            return self.read_gpio_pin_state(pin_name)

        raise PinNameError(f'The following pin name: {pin_name} is not found')