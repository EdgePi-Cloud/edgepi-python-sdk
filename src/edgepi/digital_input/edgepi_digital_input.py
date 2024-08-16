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

    def digital_input_state(self, pin: Optional[DinPins] = None):
        """
        Read selected GPIO pin
        Args:
            pin_name (DinPins): GpioPin enums
        Return:
            state (bool): corresponding pin state
        """
        if not isinstance(pin, DinPins):
            raise InvalidPinName(f'Invalid pin={pin}')

        return self.gpio.read_din_state(pin)

    def digital_input_state_batch(self, pin_list: list[DinPins]) -> list:
        """
        Read multiple GPIO pins as digital inputs
        """
        if not pin_list:
            raise ValueError(f'Unexpected pin_list={pin_list}')

        if any(not isinstance(pin, DinPins) for pin in pin_list):
            raise InvalidPinName(
                f'Got invalid pin names {pin for pin in pin_list if not isinstance(pin, DinPins)}'
            )

        return self.gpio.batch_read_din_state(pin_list)
