
"""Digital Output Module"""

from edgepi.gpio.gpio_constants import GpioPins
from edgepi.gpio.gpio_configs import DOUTPins
from edgepi.gpio.edgepi_gpio import EdgePiGPIO

class InvalidPinName(Exception):
    """Raised invalid pin name"""

class EdgePiDigitalOutput():
    """handling digital output"""
    def __init__(self):
        # To limit access to input functionality, using composition rather than inheritance
        self.gpio = EdgePiGPIO()

    def digital_output_state(self, pin_name: GpioPins = None, state: bool = None):
        """
        change the output state of the pin to the state passed as argument
        Args:
            pin_name (GpioPins): GpioPin enums
            state (bool): True = output high, False, output low
        """
        if state is None:
            raise ValueError(f'Invalid state passed: {state}')
        if pin_name is None or pin_name.value not in [pins.value for pins in DOUTPins]:
            raise InvalidPinName(f'Invalid pin name passed: {pin_name}')
        if state:
            self.gpio.set_pin_state(pin_name.value)
        else:
            self.gpio.clear_pin_state(pin_name.value)

    def digital_output_direction(self, pin_name: GpioPins = None, direction: bool = None):
        """
        change the output state of the pin to the state passed as argument
        Args:
            pin_name (GpioPins): GpioPin enums
            state (bool): True = direction input, False = direction output
        """
        if direction is None:
            raise ValueError(f'Invalid direction passed: {direction}')
        if pin_name is None or pin_name.value not in [pins.value for pins in DOUTPins]:
            raise InvalidPinName(f'Invalid pin name passed: {pin_name}')
        if direction:
            self.gpio.set_pin_direction_in(pin_name.value)
        else:
            self.gpio.set_pin_direction_out(pin_name.value)
