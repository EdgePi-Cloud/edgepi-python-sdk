"""Digital Input Module"""

from edgepi.digital_input.digital_input_constants import DinPins, DIN_MIN_NUM, DIN_MAX_NUM
from edgepi.gpio.edgepi_gpio import EdgePiGPIO

class InvalidPinName(Exception):
    """Raised invalid pin name"""

class EdgePiDigitalInput():
    """handling reading of digital inputs"""
    def __init__(self):
        # To limit access to input functionality, using composition rather than inheritance
        self.gpio = EdgePiGPIO()

    def digital_input_state(self, pin_name: DinPins):
        """
        Read selected GPIO pin
        Args:
            pin_name (DinPins): GpioPin enums
        Return:
            state (bool): corresponding pin state
        """
        if pin_name is None:
            raise InvalidPinName(f'Invalid pin name passed: {pin_name}')

        pin_number = int(pin_name.value[3])
        if pin_number > DIN_MAX_NUM or pin_number < DIN_MIN_NUM:
            raise InvalidPinName(f'Invalid pin name passed: {pin_name}')
        else:
            return self.gpio.fast_read_din_state(pin_number)
