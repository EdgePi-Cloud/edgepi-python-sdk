
"""PWM Module"""

import logging

from edgepi.peripherals.pwm import PwmDevice

from edgepi.gpio.gpio_constants import GpioPins
from edgepi.gpio.edgepi_gpio import EdgePiGPIO
from edgepi.pwm.pwm_constants import PWMCh, Polarity

class EdgePiPWM(PwmDevice):

    __pwm_pin_to_channel = {GpioPins.PWM1 : PWMCh.PWM_1,
                            GpioPins.PWM2 : PWMCh.PWM_2}

    """handling PWM output"""
    def __init__(self, pwm_num: GpioPins,
                       freq: int = None,
                       duty_cycle: float = None,
                       polarity: Polarity = None):
        self.log = logging.getLogger(__name__)
        # Control internal mux to enable/disable PWM
        self.pwm_num = pwm_num
        self.gpio = EdgePiGPIO()
        super().__init__(channel=self.__pwm_pin_to_channel[pwm_num].value.channel, 
                         chip=self.__pwm_pin_to_channel[pwm_num].value.chip)
        self.open_pwm()
        self.freq = freq
        self.duty_cycle = duty_cycle
        self.polarity = polarity
        self.log.info(f"__init__: Setting DC,FEQ,POL = {self.duty_cycle}, {self.freq}, {self.polarity}")
        self.set_dutycycle(self.duty_cycle)
        self.set_frequency(self.freq)
        self.set_polarity(self.polarity)

    def set_frequency(self, frequency: int):
        """
        Set frequency
        Args:
            frequency (int): frequency value
        Returns:
            N/A
        """
        self.set_frequency_pwm(frequency)

    def get_frequency(self):
        """
        Get frequency
        Args:
            N/A
        Returns:
            frequency (int): frequency value
        """ 
        return self.get_frequency_pwm()

    def set_dutycycle(self, duty_cycle: float):
        """
        Set duty_cycle
        Args:
            duty_cycle (int): duty_cycle value
        Returns:
            N/A
        """
        self.set_duty_cycle_pwm(duty_cycle)
    
    def get_dutycycle(self):
        """
        Get duty_cycle
        Args:
            N/A
        Returns:
            duty_cycle (int): duty_cycle value
        """ 
        return self.get_duty_cycle_pwm()

    def set_polarity(self, polarity: Polarity):
        """
        Set polarity
        Args:
            polarity (int): polarity value
        Returns:
            N/A
        """
        self.set_polarity_pwm(polarity.value)
    
    def get_polarity(self):
        """
        Get polarity
        Args:
            N/A
        Returns:
            polarity (int): polarity value
        """ 
        return self.get_polarity_pwm()
    
    def enable(self):
        """
        Enable pwm output
        """
        self.gpio.set_pin_state(GpioPins.AO_EN1.value if self.pwm_num==GpioPins.PWM1 else\
                                GpioPins.AO_EN2.value)
        self.gpio.clear_pin_state(GpioPins.DOUT1.value if self.pwm_num==GpioPins.PWM1 else\
                                GpioPins.DOUT2.value)
        self.gpio.clear_pin_state(self.pwm_num.value)
        self.log.info("Enabling PWM")
        self.enable_pwm()
    
    def disable(self):
        """
        Disable pwm output
        """
        self.disable_pwm()
        self.gpio.set_pin_state(self.pwm_num.value)

    def get_enabled(self):
        """
        Get enabled state
        Args:
            N/A
        Returns:
            enabled (bool): True enabled, False Disabled
        """
        return self.get_enabled_pwm()

    def close(self):
        """
        Close PWM connection
        Args:
            N/A
        Returns:
            N/A
        """
        self.close_pwm()
