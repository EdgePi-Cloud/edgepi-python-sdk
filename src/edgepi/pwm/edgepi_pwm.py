
"""PWM Module"""

from edgepi.peripherals.pwm import PwmDevice

from edgepi.gpio.gpio_constants import GpioPins
from edgepi.gpio.edgepi_gpio import EdgePiGPIO
from edgepi.pwm.pwm_constants import PWMCh, Polarity

class EdgePiPWM(PwmDevice):
    """handling PWM output"""
    def __init__(self, pwm_num: PWMCh,
                       freq: int = None,
                       duty_cycle: float = None,
                       polarity: Polarity = None):
        # Control internal mux to enable/disable PWM
        self.gpio = EdgePiGPIO()
        super().__init__(channel=pwm_num.value.channel, chip=pwm_num.value.chip)
        self.open_pwm()
        self.freq = freq
        self.duty_cycle = duty_cycle
        self.polarity = polarity.value

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
        self.set_polarity_pwm(polarity)
    
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
        self.enable_pwm()
    
    def disable(self):
        """
        Disable pwm output
        """
        self.disable_pwm()

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
