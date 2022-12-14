"""Digital Input Module"""

from edgepi.gpio.gpio_constants import GpioPins
from edgepi.gpio.gpio_configs import DINPins
from edgepi.gpio.edgepi_gpio import EdgePiGPIO

class InvalidPinName(Exception):
    """Raised invalid pin name"""

class EdgePiDigitalInput():
    """handling reading of digital inputs"""
    def __init__(self):
        # To limit access to input functionality, using composition rather than inheritance
        self.gpio = EdgePiGPIO()

    def digital_input_state(self, pin_name: GpioPins = None):
        """
        Read selected GPIO pin
        Args:
            pin_name (GpioPins): GpioPin enums
        Return:
            state (bool): corresponding pin state
        """
        if pin_name is None or pin_name.value not in [pins.value for pins in DINPins]:
            raise InvalidPinName(f'Invalid pin name passed: {pin_name}')
        return self.gpio.read_pin_state(pin_name.value)
