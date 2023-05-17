
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
    __pwm_1 = None
    __pwm_2 = None

    """handling PWM output"""
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.gpio = EdgePiGPIO()

    def __check_range(self, target, range_min, range_max) -> bool:
        """Validates target is in range between a min and max value"""
        if range_min <= target <= range_max:
            return True

        raise ValueError(f"Target {target} is out of range: {range_min} <-> {range_max} ")

    def __set_frequency(self, pwm_num: PWMPins, frequency: int):
        """
        Set frequency
        Args:
            pwm_num (PWMPins): target pwm device
            frequency (int): frequency value
        Returns:
            N/A
        """
        if pwm_num is None:
            raise ValueError(f"__set_frequency: PWM number is missing {pwm_num}")
        self.__check_range(frequency, PWM_MIN_FREQ, PWM_MAX_FREQ)
        if pwm_num == PWMPins.PWM1:
            self.__pwm_1.set_frequency_pwm(frequency)
        else:
            self.__pwm_2.set_frequency_pwm(frequency)

    def get_frequency(self, pwm_num: PWMPins):
        """
        Get frequency
        Args:
            pwm_num (PWMPins): target pwm device
        Returns:
            frequency (int): frequency value
        """
        if pwm_num is None:
            raise ValueError(f"get_frequency: PWM number is missing {pwm_num}")
        return self.__pwm_1.get_frequency_pwm() if pwm_num == PWMPins.PWM1 else\
               self.__pwm_2.get_frequency_pwm()

    def __set_duty_cycle(self, pwm_num: PWMPins, duty_cycle: int):
        """
        Set duty_cycle
        Args:
            pwm_num (PWMPins): target pwm device
            duty_cycle (int): duty_cycle value in percentage, this is divided by 100 and sent to the
            PWM device file
        Returns:
            N/A
        """
        if pwm_num is None:
            raise ValueError(f"__set_duty_cycle: PWM number is missing {pwm_num}")
        self.__check_range(duty_cycle, PWM_MIN_DUTY_CYCLE, PWM_MAX_DUTY_CYCLE)
        if pwm_num == PWMPins.PWM1:
            self.__pwm_1.set_duty_cycle_pwm(duty_cycle/100)
        else:
            self.__pwm_2.set_duty_cycle_pwm(duty_cycle/100)

    def get_duty_cycle(self, pwm_num: PWMPins):
        """
        Get duty_cycle
        Args:
            pwm_num (PWMPins): target pwm device
        Returns:
            duty_cycle (int): duty_cycle value in percentage
        """
        if pwm_num is None:
            raise ValueError(f"get_duty_cycle: PWM number is missing {pwm_num}")
        return self.__pwm_1.get_duty_cycle_pwm()*100 if pwm_num == PWMPins.PWM1 else\
               self.__pwm_2.get_duty_cycle_pwm()*100

    def __set_polarity(self, pwm_num: PWMPins, polarity: Polarity):
        """
        Set polarity
        Args:
            pwm_num (PWMPins): target pwm device
            polarity (int): polarity value
        Returns:
            N/A
        """
        if pwm_num is None:
            raise ValueError(f"__set_polarity: PWM number is missing {pwm_num}")
        if pwm_num == PWMPins.PWM1:
            self.__pwm_1.set_polarity_pwm(polarity.value)
        else:
            self.__pwm_2.set_polarity_pwm(polarity.value)


    def get_polarity(self, pwm_num: PWMPins):
        """
        Get polarity
        Args:
            pwm_num (PWMPins): target pwm device
        Returns:
            polarity (int): polarity value
        """
        if pwm_num is None:
            raise ValueError(f"get_polarity: PWM number is missing {pwm_num}")
        return self.__pwm_1.get_polarity_pwm() if pwm_num == PWMPins.PWM1 else\
               self.__pwm_2.get_polarity_pwm()


    def enable(self, pwm_num: PWMPins):
        """
        Enable pwm output
        Args:
            pwm_num (PWMPins): target pwm device
        Returns:
            N/A
        """
        if pwm_num is None:
            raise ValueError(f"enable: PWM number is missing {pwm_num}")
        if self.get_enabled(pwm_num):
            self.disable(pwm_num)
        self.gpio.set_pin_state(GpioPins.AO_EN1.value if pwm_num==PWMPins.PWM1 else\
                                GpioPins.AO_EN2.value)
        self.gpio.clear_pin_state(GpioPins.DOUT1.value if pwm_num==PWMPins.PWM1 else\
                                GpioPins.DOUT2.value)
        self.gpio.clear_pin_state(pwm_num.value)
        self.log.info("enable: Enabling PWM")
        if pwm_num == PWMPins.PWM1:
            self.__pwm_1.enable_pwm()
        else:
            self.__pwm_2.enable_pwm()

    def disable(self, pwm_num: PWMPins):
        """
        Disable pwm output
        Args:
            pwm_num (PWMPins): target pwm device
        Returns:
            N/A
        """
        if pwm_num is None:
            raise ValueError(f"disable: PWM number is missing {pwm_num}")
        if pwm_num == PWMPins.PWM1:
            self.__pwm_1.disable_pwm()
        else:
            self.__pwm_2.disable_pwm()
        self.gpio.set_pin_state(pwm_num.value)

    def get_enabled(self, pwm_num: PWMPins):
        """
        Get enabled state
        Args:
            N/A
        Returns:
            enabled (bool): True enabled, False Disabled
        """
        if pwm_num is None:
            raise ValueError(f"get_enabled: PWM number is missing {pwm_num}")
        return self.__pwm_1.get_enabled_pwm() if pwm_num == PWMPins.PWM1 else\
               self.__pwm_2.get_enabled_pwm()

    def close(self, pwm_num: PWMPins):
        """
        Close PWM connection
        Args:
            pwm_num (PWMPins): target pwm device
        Returns:
            N/A
        """
        if pwm_num is None:
            raise ValueError(f"close: PWM number is missing {pwm_num}")
        return self.__pwm_1.close_pwm() if pwm_num == PWMPins.PWM1 else\
               self.__pwm_2.close_pwm()

    def __check_pwm_device_and_instantiate(self, pwm_num: PWMPins):
        # Check if it is first time being called, __pwm
        if pwm_num == PWMPins.PWM1 and self.__pwm_1 is None:
            return PwmDevice(channel=self.__pwm_pin_to_channel[PWMPins.PWM1].value.channel,
                                chip=self.__pwm_pin_to_channel[PWMPins.PWM1].value.chip)
        if pwm_num == PWMPins.PWM2 and self.__pwm_2 is None:
            return PwmDevice(channel=self.__pwm_pin_to_channel[PWMPins.PWM2].value.channel,
                                chip=self.__pwm_pin_to_channel[PWMPins.PWM2].value.chip)
        return None

    def init_pwm(self, pwm_num: PWMPins):
        """
        Initializing and opening PWM device
        Args:
            pwm_num (PWMPins): PWM number enum
        Return:
            N/A
        """
        if pwm_num is None:
            raise ValueError(f"init_pwm: PWM number is missing {pwm_num}")
        pwm_dev = self.__check_pwm_device_and_instantiate(pwm_num)
        if pwm_dev is not None:
            pwm_dev.open_pwm()
            self.log.debug(f"init_pwm: Instantiating PWM Device for the first time {pwm_dev.chip}"
                           f",{pwm_dev.channel}")
            if pwm_num == PWMPins.PWM1:
                self.__pwm_1 = pwm_dev
            else:
                self.__pwm_2 = pwm_dev
        self.log.debug("init_pwm: PWM device is already open")

    def set_config(self, pwm_num: PWMPins,
                   frequency: int = PWM_MIN_FREQ,
                   duty_cycle: int = PWM_MIN_DUTY_CYCLE,
                   polarity: Polarity = Polarity.NORMAL
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
        if self.__check_pwm_device_and_instantiate(pwm_num) is not None:
            raise PwmDeviceError(f"set_config: PWM device doesn't exist {pwm_num},"
                                 f"initialize the device first")
        if self.get_frequency(pwm_num) != frequency:
            self.__set_frequency(pwm_num, frequency)
        if self.get_duty_cycle(pwm_num) != duty_cycle:
            self.__set_duty_cycle(pwm_num, duty_cycle)
        if self.get_polarity(pwm_num) != polarity.value:
            self.__set_polarity(pwm_num, polarity)
