"""
Module for PWM devices
"""

import logging
from periphery import PWM


class PwmDevice:
    """Class for representing a PWM device"""

    def __init__(self, chip: int = None, channel: int = None):
        self.log = logging.getLogger(__name__)
        self.chip = chip
        self.channel = channel
        self.pwm = None

    def open_pwm(self):
        """
        Instantiate PWM device
        """
        self.pwm = PWM(self.chip, self.channel)

    def enable_pwm(self):
        """
        enable pwm signal
        Args:
            N/A
        Return:
            N/A
        """
        self.pwm.enable()

    def disable_pwm(self):
        """
        disable pwm signal
        Args:
            N/A
        Return:
            N/A
        """
        self.pwm.disable()

    def set_frequency_pwm(self, freq: int = None):
        """
        set pwm frequency
        Args:
            freq (int): frequency to set
        Return:
            N/A
        """
        self.pwm.frequency = freq
    
    def get_frequency_pwm(self):
        """
        get pwm frequency
        Args:
            N/A
        Return:
            freq (int): frequency to set
        """
        return self.pwm.frequency

    def set_duty_cycle_pwm(self, duty_cycle: float = None):
        """
        set pwm duty cycle
        Args:
            duty_cycle (float): duty cycle value from 0 to 1.0
        Return:
            N/A
        """
        self.pwm.duty_cycle = duty_cycle
    
    def get_duty_cycle_pwm(self):
        """
        get pwm duty cycle
        Args:
            N/A
        Return:
            duty_cycle (float): duty cycle value from 0 to 1.0
        """
        return self.pwm.duty_cycle

    def set_polarity_pwm(self, polarity: str = None):
        """
        set pwm polarity
        Args:
            polarity (str): "Normal" or "Inversed"
        Return:
            N/A
        """
        self.pwm.polarity = polarity
    
    def get_polarity_pwm(self):
        """
        get pwm polarity
        Args:
            N/A
        Return:
            polarity (str): "Normal" or "Inversed"
        """
        return self.pwm.polarity
    
    def get_enabled_pwm(self):
        """
        Get pwm output state
        Args:
            N/A
        Return:
            enabled (bool): True enabled, False, disabled
        """
        return self.pwm.enabled

    def close_pwm(self):
        """Close pwm connection"""
        self.pwm.close()
