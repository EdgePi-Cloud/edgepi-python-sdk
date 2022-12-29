'''
Provides a class for interacting with the GPIO pins through GPIO peripheral
'''

import logging
from edgepi.peripherals.gpio import GpioDevice
from edgepi.gpio.gpio_constants import GpioDevPaths
from edgepi.gpio.gpio_configs import DOUTPins, DINPins, generate_gpiochip_pin_info

_logger = logging.getLogger(__name__)

class EdgePiGPIOChip(GpioDevice):
    """
    A class to represent the GPIO peripheral using gpiochip device. This class will be imported to
    each module that requires GPIO manipulation.
    """
    # dictionary mapping pin name to CPU gpio pin number
    __pin_name_dict = {DINPins.DIN1.value : 26,
                       DINPins.DIN2.value : 6,
                       DINPins.DIN3.value : 11,
                       DINPins.DIN4.value : 9,
                       DINPins.DIN5.value : 22,
                       DINPins.DIN6.value : 27,
                       DINPins.DIN7.value : 3,
                       DINPins.DIN8.value : 2,
                       DOUTPins.DOUT1.value : 13,
                       DOUTPins.DOUT2.value : 12}

    def __init__(self):
        super().__init__(GpioDevPaths.GPIO_CIHP_DEV_PATH.value)
        self.gpiochip_pins_dict = generate_gpiochip_pin_info()

    def read_gpio_pin_state(self, pin_name: str = None):
        """
        Read current state of GPIO pins. If the GPIO object is instantiated, it will be a unique
        object until close() method is called. So every time the state is read, it will instantiate
        before read and cloase() after read.
        Args:
            pin_name (str): name of the pin
        Returns:
            `bool`: True if state is high, False if state is low
        """
        self.open_gpio(pin_num=self.__pin_name_dict[pin_name],
                       pin_dir=self.gpiochip_pins_dict[pin_name].dir,
                       pin_bias=self.gpiochip_pins_dict[pin_name].bias)
        state = self.read_state()
        self.close_gpio()
        return state

    def write_gpio_pin_state(self, pin_name: str = None, state: bool = None):
        """
        write pin state
        Args:
            pin_name (str): name of the pin to write state to
            state (bool): state to write, True = High, False = Low
        Return:
            N/A
        """
        self.open_gpio(pin_num=self.__pin_name_dict[pin_name],
                       pin_dir=self.gpiochip_pins_dict[pin_name].dir,
                       pin_bias=self.gpiochip_pins_dict[pin_name].bias)
        self.write_state(state)
        read_back = self.read_state()
        self.close_gpio()
        return read_back

    def set_gpio_pin_dir(self, pin_name: str = None, direction: bool = None):
        """
        Set gpio pin direction
        Args:
            pin_name (str): name of the pin
            direction (bool): direction to write, True = Input, False = Output
        """
        self.open_gpio(pin_num=self.__pin_name_dict[pin_name],
                       pin_dir="in" if direction else "out",
                       pin_bias=self.gpiochip_pins_dict[pin_name].bias)
        self.close_gpio()

    def toggle_gpio_pin_state(self, pin_name: str = None):
        """
        Toggle pin state
        Args:
            pin_name (str): name of the pin to write state to
        Return:
            N/A
        """
        self.open_gpio(pin_num=self.__pin_name_dict[pin_name],
                       pin_dir=self.gpiochip_pins_dict[pin_name].dir,
                       pin_bias=self.gpiochip_pins_dict[pin_name].bias)
        state = self.read_state()
        if state:
            self.write_state(False)
        else:
            self.write_state(True)
        self.close_gpio()
