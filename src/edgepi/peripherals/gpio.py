"""
Module for GPIO devices
"""

import threading
from contextlib import contextmanager
from periphery import GPIO


class GpioDevice:
    """Class for representing a GPIO device"""
    lock_gpio=threading.Lock()
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
            GpioDevice.lock_gpio.acquire()
            self.gpio = GPIO(self.gpio_fd, pin_num, pin_dir, bias=pin_bias)
            yield self.gpio
        finally:
            try:
                self.gpio.close()
            except Exception as exc:
                raise OSError(f"Failed to close {self.gpio_fd}") from exc
            finally:
                GpioDevice.lock_gpio.release()

    def read_state(self):
        """
        Read the GPIO pin state
        Args:
            N/A
        Return:
            bool: True if high else False
        """
        return self.gpio.read()

    def open_read_state(self, pin_num:int, pin_dir:str, pin_bias:str):
        '''
        To minimize issues with the lock, we open & read in a single function call
        '''
        try:
            # pylint: disable=consider-using-with
            GpioDevice.lock_gpio.acquire()
            gpio   = GPIO(self.gpio_fd, pin_num, pin_dir, bias=pin_bias)
            result = gpio.read()

        finally:
            try:
                gpio.close()
            except Exception as exc:
                raise OSError(f"Failed to close {self.gpio_fd}") from exc
            finally:
                GpioDevice.lock_gpio.release()

        return result

    def open_read_state_batch(self, pin_num_list:list[int], pin_dir:str, pin_bias:str) -> list:
        '''
        Batch several gpio reads into a single lock / unlock. We can also take advantage of the fact we're accessing
        the gpio only from different pins, and so we can open & close just a single time.
        '''
        results = []
        try:
            # pylint: disable=consider-using-with
            GpioDevice.lock_gpio.acquire()
            gpio = None
            try:
                for pin_num in pin_num_list:
                    if gpio is None:
                        gpio = GPIO(self.gpio_fd, pin_num, pin_dir, bias=pin_bias)
                    else:
                        # NOTE: we'll need to be careful when we update periphery, since we depend on a
                        # private functionality

                        # pylint: disable=protected-access
                        gpio._line = pin_num
                        # pylint: disable=protected-access
                        gpio._reopen(pin_dir, edge="none", bias=pin_bias, drive="default", inverted=False)
                    results += [gpio.read()]

            finally:
                try:
                    gpio.close()
                except Exception as exc:
                    raise OSError(f"Failed to close {self.gpio_fd}") from exc

        finally:
            GpioDevice.lock_gpio.release()

        return results

    def write_state(self, state: bool = None):
        """
        Write state to GPIO pin
        Args:
            state (bool): High if True else LOW
        Return:
            N/A
        """
        self.gpio.write(state)
