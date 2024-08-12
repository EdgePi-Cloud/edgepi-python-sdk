'''
Provides a class for interacting with the GPIO pins through GPIO peripheral
'''

import logging
from typing import Optional

from edgepi.peripherals.gpio import GpioDevice
from edgepi.gpio.gpio_constants import GpioDevPaths
from edgepi.gpio.gpio_configs import DINPins, generate_gpiochip_pin_info

_logger = logging.getLogger(__name__)

class EdgePiGPIOChip(GpioDevice):
    """
    A class to represent the GPIO peripheral using gpiochip device. This class will be imported to
    each module that requires GPIO manipulation.
    """
    # dictionary mapping pin name to CPU gpio pin number
    __pin_name_dict = {
        DINPins.DIN1.value : 26,
        DINPins.DIN2.value : 6,
        DINPins.DIN3.value : 11,
        DINPins.DIN4.value : 9,
        DINPins.DIN5.value : 22,
        DINPins.DIN6.value : 27,
        DINPins.DIN7.value : 10,
        DINPins.DIN8.value : 7
    }
    __din_mapping_array = [26, 6, 11, 9, 22, 27, 10, 7]
    __din_pin_dir  = "in"
    __din_pin_bias = "pull_down"

    def __init__(self):
        super().__init__(GpioDevPaths.GPIO_CIHP_DEV_PATH.value)
        self.gpiochip_pins_dict = generate_gpiochip_pin_info()

    def read_gpio_pin_state(self, pin_name: Optional[str] = None):
        """
        Read current state of GPIO pins. If the GPIO object is instantiated, it will be a unique
        object until close() method is called. So every time the state is read, it will instantiate
        before read and cloase() after read.
        Args:
            pin_name (str): name of the pin
        Returns:
            `bool`: True if state is high, False if state is low
        """
        with self.open_gpio(pin_num=self.__pin_name_dict[pin_name],
                       pin_dir=self.gpiochip_pins_dict[pin_name].dir,
                       pin_bias=self.gpiochip_pins_dict[pin_name].bias):
            state = self.read_state()
        return state

    # TODO: is there a big performance difference if we just use str instead of integers?
    def fast_read_din_state(self, din_pin_num: int):
        """
        Use this function synonymously with `read_gpio_pin_state`, except that
        you should use the pin's number, not it's name.
        
        It is slightly faster than `read_gpio_pin_state` as it combines opening &
        reading into a single operation.
        """
        return self.open_read_state(
            pin_num  = self.__din_mapping_array[din_pin_num-1],
            pin_dir  = self.__din_pin_dir,
            pin_bias = self.__din_pin_bias,
        )

    def fast_read_din_state_batch(self, din_pin_num_list: list[int]) -> list:
        """
        This function efficiently reads from many pins in a row by only opening &
        closing the GPIO port only once.
        """
        pin_num_list = [self.__din_mapping_array[pin_num-1] for pin_num in din_pin_num_list]
        return self.open_read_state_batch(
            pin_num_list = pin_num_list,
            pin_dir      = self.__din_pin_dir,
            pin_bias     = self.__din_pin_bias,
        )

    def write_gpio_pin_state(self, pin_name: str = None, state: bool = None):
        """
        write pin state
        Args:
            pin_name (str): name of the pin to write state to
            state (bool): state to write, True = High, False = Low
        Return:
            N/A
        """
        with self.open_gpio(pin_num=self.__pin_name_dict[pin_name],
                       pin_dir=self.gpiochip_pins_dict[pin_name].dir,
                       pin_bias=self.gpiochip_pins_dict[pin_name].bias):
            self.write_state(state)
            read_back = self.read_state()
        return read_back

    def set_gpio_pin_dir(self, pin_name: str = None, direction: bool = None):
        """
        Set gpio pin direction
        Args:
            pin_name (str): name of the pin
            direction (bool): direction to write, True = Input, False = Output
        """
        with self.open_gpio(pin_num=self.__pin_name_dict[pin_name],
                       pin_dir="in" if direction else "out",
                       pin_bias=self.gpiochip_pins_dict[pin_name].bias):
            return self.gpio.direction

    def toggle_gpio_pin_state(self, pin_name: str = None):
        """
        Toggle pin state
        Args:
            pin_name (str): name of the pin to write state to
        Return:
            N/A
        """
        with self.open_gpio(pin_num=self.__pin_name_dict[pin_name],
                       pin_dir=self.gpiochip_pins_dict[pin_name].dir,
                       pin_bias=self.gpiochip_pins_dict[pin_name].bias):
            state = self.read_state()
            self.write_state(not state)
            