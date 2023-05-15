
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

class EdgePiPWM():
    """PWM module to provide PWM signal"""
    __pwm_pin_to_channel = {PWMPins.PWM1 : PWMCh.PWM_1,
                            PWMPins.PWM2 : PWMCh.PWM_2}

    """handling PWM output"""
    def __init__(self, pwm_num: PWMPins):
        self.log = logging.getLogger(__name__)
        # Control internal mux to enable/disable PWM
        self.pwm_num = pwm_num
        self.gpio = EdgePiGPIO()
        self.pwm = PwmDevice(channel=self.__pwm_pin_to_channel[pwm_num].value.channel,
                         chip=self.__pwm_pin_to_channel[pwm_num].value.chip)
        self.channel = self.__pwm_pin_to_channel[pwm_num].value.channel
        self.chip = self.__pwm_pin_to_channel[pwm_num].value.chip
        self.pwm.open_pwm()

    def __check_range(self, target, range_min, range_max) -> bool:
        """Validates target is in range between a min and max value"""
        if range_min <= target <= range_max:
            return True

        raise ValueError(f"Target {target} is out of range: {range_min} <-> {range_max} ")

    def set_frequency(self, frequency: int):
        """
        Set frequency
        Args:
            frequency (int): frequency value
        Returns:
            N/A
        """
        self.__check_range(frequency, PWM_MIN_FREQ, PWM_MAX_FREQ)
        self.pwm.set_frequency_pwm(frequency)

    def get_frequency(self):
        """
        Get frequency
        Args:
            N/A
        Returns:
            frequency (int): frequency value
        """
        return self.pwm.get_frequency_pwm()

    def set_duty_cycle(self, duty_cycle: int):
        """
        Set duty_cycle
        Args:
            duty_cycle (int): duty_cycle value in percentage, this is divided by 100 and sent to the
            PWM device file
        Returns:
            N/A
        """
        self.__check_range(duty_cycle, PWM_MIN_DUTY_CYCLE, PWM_MAX_DUTY_CYCLE)
        self.pwm.set_duty_cycle_pwm(duty_cycle/100)

    def get_duty_cycle(self):
        """
        Get duty_cycle
        Args:
            N/A
        Returns:
            duty_cycle (int): duty_cycle value in percentage
        """
        return int(self.pwm.get_duty_cycle_pwm() * 100)

    def set_polarity(self, polarity: Polarity):
        """
        Set polarity
        Args:
            polarity (int): polarity value
        Returns:
            N/A
        """
        self.pwm.set_polarity_pwm(polarity.value)

    def get_polarity(self):
        """
        Get polarity
        Args:
            N/A
        Returns:
            polarity (int): polarity value
        """
        return self.pwm.get_polarity_pwm()

    def enable(self):
        """
        Enable pwm output
        """
        self.gpio.set_pin_state(GpioPins.AO_EN1.value if self.pwm_num==PWMPins.PWM1 else\
                                GpioPins.AO_EN2.value)
        self.gpio.clear_pin_state(GpioPins.DOUT1.value if self.pwm_num==PWMPins.PWM1 else\
                                GpioPins.DOUT2.value)
        self.gpio.clear_pin_state(self.pwm_num.value)
        self.log.info("Enabling PWM")
        self.pwm.enable_pwm()

    def disable(self):
        """
        Disable pwm output
        """
        self.pwm.disable_pwm()
        self.gpio.set_pin_state(self.pwm_num.value)

    def get_enabled(self):
        """
        Get enabled state
        Args:
            N/A
        Returns:
            enabled (bool): True enabled, False Disabled
        """
        return self.pwm.get_enabled_pwm()

    def close(self):
        """
        Close PWM connection
        Args:
            N/A
        Returns:
            N/A
        """
        self.pwm.close_pwm()
