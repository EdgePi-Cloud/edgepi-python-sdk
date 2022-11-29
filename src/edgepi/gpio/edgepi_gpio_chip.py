'''
Provides a class for interacting with the GPIO pins through GPIO peripheral
'''

import logging
from edgepi.peripherals.gpio import GpioDevice
from edgepi.gpio.gpio_configs import DOUTPins, DINPins, generate_pin_info, GpioConfigs

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

    def __init__(self, config: GpioConfigs = None):
        #pylint: disable=super-init-not-called
        self.dict_gpiochip_pins = generate_pin_info(config)

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
        super().__init__(pin_num=self.__pin_name_dict[pin_name],
                         pin_dir=self.dict_gpiochip_pins[pin_name].dir,
                         pin_bias=self.dict_gpiochip_pins[pin_name].bias)
        state = self.read_state()
        self.close()
        return state
