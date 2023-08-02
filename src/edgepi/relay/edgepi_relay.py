"""Relay Module"""

import logging
from edgepi.gpio.gpio_constants import GpioPins
from edgepi.gpio.edgepi_gpio import EdgePiGPIO

_logger = logging.getLogger(__name__)

class EdgePiRelay():
    """A class to control the relay"""
    def __init__(self):
        # To limit access to input functionality, using composition rather than inheritance
        self.gpio = EdgePiGPIO()

    def get_state_relay(self):
        """
        Method to get the current state of the relay
        Arg:
            N/A
        Return:
            state (bool): True - closed, False - open
        """
        state = self.gpio.read_pin_state(GpioPins.RELAY.value)
        return state

    def toggle_relay(self):
        """
        Method to toggle the relay
        Arg:
            N/A
        Return:
            N/A
        """
        self.gpio.toggle_pin(GpioPins.RELAY.value)

    def close_relay(self):
        """
        Method to close the relay
        Arg:
            N/A
        Return:
            N/A
        """
        self.gpio.set_pin_state(GpioPins.RELAY.value)

    def open_relay(self):
        """
        Method to open the relay
        Arg:
            N/A
        Return:
            N/A
        """
        self.gpio.clear_pin_state(GpioPins.RELAY.value)
