"""EdgePi LED array"""


import logging


from edgepi.gpio.gpio_configs import LEDPins
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
        self.log.info("LED with name '%s' turned on", led_name.value)

    def turn_led_off(self, led_name: LEDPins):
        """
        Turn an LED off

        Args:
            `led_name` (LEDPins): name of LED to turn off
        """
        self.__validate_led_name(led_name)
        self.gpio_ops.clear_expander_pin(led_name.value)
        self.log.info("LED with name '%s' turned off", led_name.value)

    def toggle_led(self, led_name: LEDPins):
        """
        Toggle an LED to its opposite state

        Args:
            `led_name` (LEDPins): name of LED to toggle
        """
        self.__validate_led_name(led_name)
        self.gpio_ops.toggle_expander_pin(led_name.value)
        self.log.info("LED with name '%s' toggled to opposite state", led_name.value)

    def get_led_state(self, led_name: LEDPins) -> bool:
        """
        Read an LED's current state (on/off)

        Args:
            `led_name` (LEDPins): name of LED whose state is to be read

        Returns:
            `bool`: True if LED is on, False if LED is off
        """
        self.__validate_led_name(led_name)
        state = self.gpio_ops.read_expander_pin_state(led_name.value)
        msg = "ON" if state else "OFF"
        self.log.info("LED with name '%s' is currently %s", led_name.value, msg)
        return state
