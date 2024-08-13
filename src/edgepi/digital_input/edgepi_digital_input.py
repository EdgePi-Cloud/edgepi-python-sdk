"""Digital Input Module"""

from typing import Optional

from edgepi.digital_input.digital_input_constants import DinPins
from edgepi.gpio.edgepi_gpio import EdgePiGPIO

class InvalidPinName(Exception):
    """Raised invalid pin name"""

class EdgePiDigitalInput():
    """handling reading of digital inputs"""
    def __init__(self):
        # To limit access to input functionality, using composition rather than inheritance
        self.gpio = EdgePiGPIO()

    def digital_input_state(self, pin_name: Optional[DinPins] = None):
        """
        Read selected GPIO pin
        Args:
            pin_name (DinPins): GpioPin enums
        Return:
            state (bool): corresponding pin state
        """
        if pin_name is None or not isinstance(pin_name, DinPins):
            raise InvalidPinName(f'Invalid pin name passed: {pin_name}')

        pin_number = int(pin_name.value[3])
        return self.gpio.fast_read_din_state(pin_number)

    def digital_input_state_batch(self, pin_names: list[DinPins]) -> list:
        """
        Read multiple GPIO pins as digital inputs
        """
        if not pin_names:
            raise ValueError(f'Unexpected value pin_names={pin_names}')

        invalid_pin_types = [False for pin_name in pin_names if not isinstance(pin_name, DinPins)]
        if len(invalid_pin_types) > 0:
            raise InvalidPinName(f'Invalid pin names passed in {pin_names}')

        pin_numbers = [int(pin_name.value[3]) for pin_name in pin_names]
        return self.gpio.fast_read_din_state_batch(pin_numbers)
