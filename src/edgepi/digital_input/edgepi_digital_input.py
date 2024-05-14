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

    def digital_input_state_batch(self, pin_names: list[DinPins]) -> list:
        """
        Read multiple GPIO pins as digital inputs
        """
        if pin_names is None:
            raise InvalidPinName('pin_names cannot be None')
        elif pin_names is []:
            # TODO: what is the correct exception to raise?
            raise Exception('pin_names cannot be empty')

        pin_numbers = [int(pin_name.value[3]) for pin_name in pin_names]
        invalid_pin_numbers = [num for num in pin_numbers if (num > DIN_MAX_NUM) or (num < DIN_MIN_NUM)]
        if len(invalid_pin_numbers) > 0:
            raise InvalidPinName(f'Invalid pin names passed: {invalid_pin_numbers}')
        else:
            return self.gpio.fast_read_din_state_batch(pin_numbers)
