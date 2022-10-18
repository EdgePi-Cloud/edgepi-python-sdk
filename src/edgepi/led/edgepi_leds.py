"""EdgePi LED array"""


import logging


from edgepi.gpio.gpio_configs import LEDPins
from edgepi.gpio.edgepi_gpio import EdgePiGPIO


_logger = logging.getLogger(__name__)


class InvalidLEDNameError(Exception):
    """
    Raised if a user attempts to pass an invalid LED name to
    an EdgePiLED method."""


class EdgePiLED:
    """Interact with the EdgePi LED Array"""
    def __init__(self):
        self.gpio_ops = EdgePiGPIO()

    @staticmethod
    def __validate_led_name(led_name: LEDPins):
        """Checks if an LED name is valid"""
        if not isinstance(led_name, LEDPins):
            raise InvalidLEDNameError(
                f"{led_name} is not a valid EdgePi LED name, please use EdgePiLED enums for names."
            )

    def turn_led_on(self, led_name: LEDPins):
        """
        Turn an LED on

        Args:
            `led_name` (LEDPins): name of LED to turn on
        """
        self.__validate_led_name(led_name)
        self.gpio_ops.set_expander_pin(led_name.value)
        _logger.info(f"LED with name {led_name.value} turned on")

    def turn_led_off(self, led_name: LEDPins):
        """
        Turn an LED off

        Args:
            `led_name` (LEDPins): name of LED to turn off
        """
        self.__validate_led_name(led_name)
        self.gpio_ops.clear_expander_pin(led_name.value)
        _logger.info(f"LED with name {led_name.value} turned off")
