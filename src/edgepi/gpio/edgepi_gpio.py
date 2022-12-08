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
        if pin_name is None:
            raise PinNameError(f'The following pin name: {pin_name} is not found')
        if pin_name in self.expander_pin_dict:
            return self.read_expander_pin(pin_name)
        if pin_name in self.gpiochip_pins_dict:
            return self.read_gpio_pin_state(pin_name)

        raise PinNameError(f'The following pin name: {pin_name} is not found')


    def set_pin_state(self, pin_name: str = None):
        """
        Set corresponding pin state to high
        Args:
            pin_name(str): name of the pin will be passed as Enum
        return:
            N/A
        """
        if pin_name is None:
            raise PinNameError(f'The following pin name: {pin_name} is not found')
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
        if pin_name is None:
            raise PinNameError(f'The following pin name: {pin_name} is not found')
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
        if pin_name is None:
            raise PinNameError(f'The following pin name: {pin_name} is not found')
        if pin_name in self.expander_pin_dict:
            return self.get_expander_pin_direction(pin_name)
        if pin_name in self.gpiochip_pins_dict:
            return bool(self.gpiochip_pins_dict[pin_name].dir == "in")

        raise PinNameError(f'The following pin name: {pin_name} is not found')

    def set_pin_direction_in(self, pin_name: str = None):
        """
        Set GPIO pin direction to input
        Args:
            pin_name(str): name of the pin
        Return:
            N/A
        """
        if pin_name is None:
            raise PinNameError(f'The following pin name: {pin_name} is not found')
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
        if pin_name is None:
            raise PinNameError(f'The following pin name: {pin_name} is not found')
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
        if pin_name is None:
            raise PinNameError(f'The following pin name: {pin_name} is not found')
        if pin_name in self.expander_pin_dict:
            self.toggle_expander_pin(pin_name)
        if pin_name in self.gpiochip_pins_dict:
            self.toggle_gpio_pin_state(pin_name)
