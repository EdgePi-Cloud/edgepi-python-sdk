
"""PWM Module"""

import logging

from edgepi.peripherals.pwm import PwmDevice

from edgepi.gpio.edgepi_gpio import EdgePiGPIO
from edgepi.gpio.gpio_constants import GpioPins
from edgepi.pwm.pwm_constants import (
    PWMCh,
    PWMPins,
    Polarity,
    PWM_MAX_FREQ,
    PWM_MIN_FREQ,
    PWM_MAX_DUTY_CYCLE,
    PWM_MIN_DUTY_CYCLE,
)

class PwmDeviceError(Exception):
    """Raised when PWM device doesn't exist"""

class EdgePiPWM():
    """PWM module to provide PWM signal"""
    __pwm_pin_to_channel = {PWMPins.PWM1 : PWMCh.PWM_1,
                            PWMPins.PWM2 : PWMCh.PWM_2}

    """handling PWM output"""
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.gpio = EdgePiGPIO()
        self.__pwm_devs = {PWMPins.PWM1 : None,
                  PWMPins.PWM2 : None}

    def __check_range(self, target, range_min, range_max) -> bool:
        """Validates target is in range between a min and max value"""
        if range_min <= target <= range_max:
            return True

        raise ValueError(f"Target {target} is out of range: {range_min} <-> {range_max} ")

    def __set_frequency(self, pwm_num: PWMPins, frequency: float):
        """
        Set frequency
        Args:
            pwm_num (PWMPins): target pwm device
            frequency (float): frequency value
        Returns:
            N/A
        """
        if pwm_num is None or pwm_num not in self.__pwm_devs:
            raise ValueError(f"__set_frequency: PWM number is missing {pwm_num}")
        self.__check_range(frequency, PWM_MIN_FREQ, PWM_MAX_FREQ)
        self.__pwm_devs[pwm_num].set_frequency_pwm(frequency)

    def get_frequency(self, pwm_num: PWMPins):
        """
        Get frequency
        Args:
            pwm_num (PWMPins): target pwm device
        Returns:
            frequency (float): frequency value
        """
        if pwm_num is None or pwm_num not in self.__pwm_devs:
            raise ValueError(f"get_frequency: PWM number is missing {pwm_num}")
        return self.__pwm_devs[pwm_num].get_frequency_pwm()

    def __set_duty_cycle(self, pwm_num: PWMPins, duty_cycle: float):
        """
        Set duty_cycle
        Args:
            pwm_num (PWMPins): target pwm device
            duty_cycle (float): duty_cycle value in percentage, this is divided by 100 and sent to
            the PWM device file
        Returns:
            N/A
        """
        if pwm_num is None or pwm_num not in self.__pwm_devs:
            raise ValueError(f"__set_duty_cycle: PWM number is missing {pwm_num}")
        self.__check_range(duty_cycle, PWM_MIN_DUTY_CYCLE, PWM_MAX_DUTY_CYCLE)
        self.__pwm_devs[pwm_num].set_duty_cycle_pwm(duty_cycle)

    def get_duty_cycle(self, pwm_num: PWMPins):
        """
        Get duty_cycle
        Args:
            pwm_num (PWMPins): target pwm device
        Returns:
            duty_cycle (float): duty_cycle value in percentage
        """
        if pwm_num is None or pwm_num not in self.__pwm_devs:
            raise ValueError(f"get_duty_cycle: PWM number is missing {pwm_num}")
        return self.__pwm_devs[pwm_num].get_duty_cycle_pwm()

    def __set_polarity(self, pwm_num: PWMPins, polarity: Polarity):
        """
        Set polarity
        Args:
            pwm_num (PWMPins): target pwm device
            polarity (Polarity): polarity enum
        Returns:
            N/A
        """
        if pwm_num is None or pwm_num not in self.__pwm_devs:
            raise ValueError(f"__set_polarity: PWM number is missing {pwm_num}")
        self.__pwm_devs[pwm_num].set_polarity_pwm(polarity)

    def get_polarity(self, pwm_num: PWMPins):
        """
        Get polarity
        Args:
            pwm_num (PWMPins): target pwm device
        Returns:
            polarity (Polarity): polarity enum
        """
        if pwm_num is None or pwm_num not in self.__pwm_devs:
            raise ValueError(f"get_polarity: PWM number is missing {pwm_num}")
        return self.__pwm_devs[pwm_num].get_polarity_pwm()


    def enable(self, pwm_num: PWMPins):
        """
        Enable pwm output
        Args:
            pwm_num (PWMPins): target pwm device
        Returns:
            N/A
        """
        if pwm_num is None or pwm_num not in self.__pwm_devs:
            raise ValueError(f"enable: PWM number is missing {pwm_num}")
        if self.get_enabled(pwm_num):
            self.disable(pwm_num)
        self.gpio.set_pin_state(GpioPins.AO_EN1.value if pwm_num==PWMPins.PWM1 else\
                                GpioPins.AO_EN2.value)
        self.gpio.clear_pin_state(GpioPins.DOUT1.value if pwm_num==PWMPins.PWM1 else\
                                GpioPins.DOUT2.value)
        self.gpio.clear_pin_state(pwm_num.value)
        self.log.info("enable: Enabling PWM")
        self.__pwm_devs[pwm_num].enable_pwm()

    def disable(self, pwm_num: PWMPins):
        """
        Disable pwm output
        Args:
            pwm_num (PWMPins): target pwm device
        Returns:
            N/A
        """
        if pwm_num is None or pwm_num not in self.__pwm_devs:
            raise ValueError(f"disable: PWM number is missing {pwm_num}")
        self.__pwm_devs[pwm_num].disable_pwm()
        self.gpio.set_pin_state(GpioPins.AO_EN1.value if pwm_num==PWMPins.PWM1 else\
                                GpioPins.AO_EN2.value)
        self.gpio.clear_pin_state(GpioPins.DOUT1.value if pwm_num==PWMPins.PWM1 else\
                                GpioPins.DOUT2.value)
        self.gpio.clear_pin_state(pwm_num.value)

    def get_enabled(self, pwm_num: PWMPins):
        """
        Get enabled state
        Args:
            N/A
        Returns:
            enabled (bool): True enabled, False Disabled
        """
        if pwm_num is None or pwm_num not in self.__pwm_devs:
            raise ValueError(f"get_enabled: PWM number is missing {pwm_num}")
        return self.__pwm_devs[pwm_num].get_enabled_pwm()

    def close(self, pwm_num: PWMPins):
        """
        Close PWM connection
        Args:
            pwm_num (PWMPins): target pwm device
        Returns:
            N/A
        """
        if pwm_num is None or pwm_num not in self.__pwm_devs:
            raise ValueError(f"get_enabled: PWM number is missing {pwm_num}")
        self.__pwm_devs[pwm_num].close_pwm()
        self.__pwm_devs[pwm_num] = None

    def __init_pwm_dev(self, pwm_num: PWMPins):
        self.__pwm_devs[pwm_num]=PwmDevice(channel=self.__pwm_pin_to_channel[pwm_num].value.channel,
                                           chip=self.__pwm_pin_to_channel[pwm_num].value.chip)
        self.__pwm_devs[pwm_num].open_pwm()
        self.log.debug(f"init_pwm: Instantiating PWM Device for the first time "
                       f"{self.__pwm_devs[pwm_num].chip}"
                       f",{self.__pwm_devs[pwm_num].channel}")


    def init_pwm(self, pwm_num: PWMPins):
        """
        Initializing and opening PWM device
        Args:
            pwm_num (PWMPins): PWM number enum
        Return:
            N/A
        """
        if pwm_num is None or pwm_num not in self.__pwm_devs:
            raise ValueError(f"init_pwm: PWM number is missing {pwm_num}")
        if self.__pwm_devs[pwm_num] is None:
            self.__init_pwm_dev(pwm_num)
            return

        self.log.debug("init_pwm: PWM device is already open")

    def set_config(self, pwm_num: PWMPins,
                   frequency: float = None,
                   duty_cycle: int = None,
                   polarity: Polarity = None
                   ):
        """
        Setting PWM configuration
        Args:
            pwm_num (PWMPins): PWM number enum
            frequency (int): in Hz, from 1000~10000
            duty_cycle (int): in %, from 0~100
            polarity (Polarity): enum, "Normal" or "Inversed"
        Return:
            N/A
        """
        if pwm_num is None:
            raise ValueError(f"set_config: PWM number is missing {pwm_num}")
        if self.__pwm_devs[pwm_num] is None:
            raise PwmDeviceError(f"set_config: PWM device doesn't exist {pwm_num},"
                                 f"initialize the device first")
        if frequency is not None:
            self.__set_frequency(pwm_num, frequency)
        if  duty_cycle is not None:
            self.__set_duty_cycle(pwm_num, duty_cycle)
        if polarity is not None:
            self.__set_polarity(pwm_num, polarity)
