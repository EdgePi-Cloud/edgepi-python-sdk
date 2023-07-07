"""EdgePi LED array"""


import logging


from edgepi.led.led_constants import LEDPins
from edgepi.gpio.edgepi_gpio import EdgePiGPIO


class InvalidLEDNameError(Exception):
    """
    Raised if a user attempts to pass an invalid LED name to
    an EdgePiLED method."""


class EdgePiLED:
    """Interact with the EdgePi LED Array"""

    def __init__(self):
        self.gpio_ops = EdgePiGPIO()
        self.log = logging.getLogger(__name__)

    @staticmethod
    def __validate_led_name(led_name: LEDPins):
        """Checks if an LED name is valid"""
        if not isinstance(led_name, LEDPins):
            raise InvalidLEDNameError(
                f"{led_name} is not a valid EdgePi LED name, use LEDPins enums for names."
            )

    def turn_led_on(self, led_name: LEDPins):
        """
        Turn an LED on

        Args:
            `led_name` (LEDPins): name of LED to turn on
        """
        self.__validate_led_name(led_name)
        self.gpio_ops.set_pin_state(led_name.value)
        self.log.info(f"LED with name {led_name.value} has been turned on")

    def turn_led_off(self, led_name: LEDPins):
        """
        Turn an LED off

        Args:
            `led_name` (LEDPins): name of LED to turn off
        """
        self.__validate_led_name(led_name)
        self.gpio_ops.clear_pin_state(led_name.value)
        self.log.info(f"LED with name {led_name.value} has been turned off")

    def toggle_led(self, led_name: LEDPins):
        """
        Toggle an LED to its opposite state

        Args:
            `led_name` (LEDPins): name of LED to toggle
        """
        self.__validate_led_name(led_name)
        self.gpio_ops.toggle_pin(led_name.value)
        self.log.info(f"LED with name {led_name.value} has been toggled to opposite state")

    def get_led_state(self, led_name: LEDPins) -> bool:
        """
        Read an LED's current state (on/off)

        Args:
            `led_name` (LEDPins): name of LED whose state is to be read

        Returns:
            `bool`: True if LED is on, False if LED is off
        """
        self.__validate_led_name(led_name)
        state = self.gpio_ops.read_pin_state(led_name.value)
        msg = "ON" if state else "OFF"
        self.log.info(f"LED with name {led_name.value} is currently {msg}")
        return state
