"""
Module for GPIO devices
"""


from periphery import GPIO


class GpioDevice:
    """Class for representing a GPIO device"""

    def __init__(self, dev_path: str = None):
        self.fd = dev_path
        self.gpio = None

    def open_gpio(self, pin_num: int = None, pin_dir: str = None, pin_bias: str = None):
        """
        Instantiate GPIO device object for reading and writing.
        Args:
            pin_num (int): pin number to instantiate the object with
            pin_dir (str): pin direction
            pin_bias (str): bias direction
        """
        self.gpio = GPIO(self.fd, pin_num, pin_dir, bias=pin_bias)

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

    def close_gpio(self):
        """Close GPIO connection"""
        self.gpio.close()
