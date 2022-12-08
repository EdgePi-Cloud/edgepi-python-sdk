'''
Provides a class for interacting with the GPIO pins through I2C and GPIO peripheral
'''


import logging
from edgepi.gpio.edgepi_gpio_expander import EdgePiGPIOExpander
from edgepi.gpio.edgepi_gpio_chip import EdgePiGPIOChip

_logger = logging.getLogger(__name__)

class PinNameNoneError(Exception):
    """Raised when None is passed"""

class PinNameNotFound(Exception):
    """"Raised when name doesn't exist"""


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

    def __pin_name_check(self, pin_name: str = None):
        if pin_name is None:
            raise PinNameNoneError(f'Missing Pin name: {pin_name}')
        if pin_name not in self.expander_pin_dict and pin_name not in self.gpiochip_pins_dict:
            raise PinNameNotFound(f'The following pin name: {pin_name} is not found')

    def read_pin_state(self, pin_name: str = None):
        """
        Read corresponding pin state
        Args:
            pin_name (str): name of the pin will be passed as Enum
        return
            state (bool): True/False depending on High/Low
        """
        state = None
        self.__pin_name_check(pin_name)
        if pin_name in self.expander_pin_dict:
            state = self.read_expander_pin(pin_name)
        if pin_name in self.gpiochip_pins_dict:
            state = self.read_gpio_pin_state(pin_name)
        return state


    def set_pin_state(self, pin_name: str = None):
        """
        Set corresponding pin state to high
        Args:
            pin_name(str): name of the pin will be passed as Enum
        return:
            N/A
        """
        self.__pin_name_check(pin_name)
        if pin_name in self.expander_pin_dict:
            self.set_expander_pin(pin_name)
        if pin_name in self.gpiochip_pins_dict:
            self.write_gpio_pin_state(pin_name, True)

    def clear_pin_state(self, pin_name: str = None):
        """
        Clearcorresponding pin state to high
        Args:
            pin_name(str): name of the pin will be passed as Enum
        return:
            N/A
        """
        self.__pin_name_check(pin_name)
        if pin_name in self.expander_pin_dict:
            self.clear_expander_pin(pin_name)
        if pin_name in self.gpiochip_pins_dict:
            self.write_gpio_pin_state(pin_name, False)

    def get_pin_direction(self, pin_name: str = None):
        """
        Get GPIO pin direction
        Args:
            pin_name(str): name of the pin
        Return:
            direction (bool): True if direction is input, False if direction is output
        """
        direction = None
        self.__pin_name_check(pin_name)
        if pin_name in self.expander_pin_dict:
            direction = self.get_expander_pin_direction(pin_name)
        if pin_name in self.gpiochip_pins_dict:
            direction = bool(self.gpiochip_pins_dict[pin_name].dir == "in")
        return direction

    def set_pin_direction_in(self, pin_name: str = None):
        """
        Set GPIO pin direction to input
        Args:
            pin_name(str): name of the pin
        Return:
            N/A
        """
        self.__pin_name_check(pin_name)
        if pin_name in self.expander_pin_dict:
            self.set_expander_pin_direction_in(pin_name)
        if pin_name in self.gpiochip_pins_dict:
            self.set_gpio_pin_dir(pin_name, True)

    def set_pin_direction_out(self, pin_name: str = None):
        """
        Set GPIO pin direction to output
        Args:
            pin_name(str): name of the pin
        Return:
            N/A
        """
        self.__pin_name_check(pin_name)
        if pin_name in self.expander_pin_dict:
            self.set_expander_pin_direction_out(pin_name)
        if pin_name in self.gpiochip_pins_dict:
            self.set_gpio_pin_dir(pin_name, False)

    def toggle_pin(self, pin_name: str = None):
        """
        Toggle GPIO pin
        Args:
            pin_name (str): name of the pin
        Return:
            N/A
        """
        self.__pin_name_check(pin_name)
        if pin_name in self.expander_pin_dict:
            self.toggle_expander_pin(pin_name)
        if pin_name in self.gpiochip_pins_dict:
            self.toggle_gpio_pin_state(pin_name)
