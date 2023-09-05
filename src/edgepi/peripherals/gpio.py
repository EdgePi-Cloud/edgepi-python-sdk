"""
Module for GPIO devices
"""

from contextlib import contextmanager
from periphery import GPIO


class GpioDevice:
    """Class for representing a GPIO device"""

    def __init__(self, dev_path: str = None):
        self.gpio_fd = dev_path
        self.gpio = None

    @contextmanager
    def open_gpio(self, pin_num: int = None, pin_dir: str = None, pin_bias: str = None):
        """
        Instantiate GPIO device object for reading and writing.
        Args:
            pin_num (int): pin number to instantiate the object with
            pin_dir (str): pin direction
            pin_bias (str): bias direction
        """
        try:
            self.gpio = GPIO(self.gpio_fd, pin_num, pin_dir, bias=pin_bias)
            yield self.gpio
        finally:
            self.gpio.close()

    def read_state(self):
        """
        Read the GPIO pin state
        Args:
            N/A
        Return:
            bool: True if high else False
        """
        return self.gpio.read()

    def write_state(self, state: bool = None):
        """
        Write state to GPIO pin
        Args:
            state (bool): High if True else LOW
        Return:
            N/A
        """
        self.gpio.write(state)
