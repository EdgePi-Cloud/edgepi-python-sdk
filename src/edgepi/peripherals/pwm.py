"""
Module for PWM devices
"""

import logging
from periphery import PWM
from edgepi.pwm.pwm_constants import Polarity


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
        Enable pwm signal
        Args:
            N/A
        Return:
            N/A
        """
        self.log.info("Enabling PWM")
        self.pwm.enable()

    def disable_pwm(self):
        """
        Disable pwm signal
        Args:
            N/A
        Return:
            N/A
        """
        self.pwm.disable()

    def set_frequency_pwm(self, freq: float = None):
        """
        Set pwm frequency
        Args:
            freq (float): frequency to set
        Return:
            N/A
        """
        self.pwm.frequency = freq

    def get_frequency_pwm(self):
        """
        Get pwm frequency
        Args:
            N/A
        Return:
            freq (float): frequency to set
        """
        return self.pwm.frequency

    def set_duty_cycle_pwm(self, duty_cycle: float = None):
        """
        Set pwm duty cycle
        Args:
            duty_cycle (float): duty cycle value from 0 to 1.0
        Return:
            N/A
        """
        self.pwm.duty_cycle = duty_cycle

    def get_duty_cycle_pwm(self):
        """
        Get pwm duty cycle
        Args:
            N/A
        Return:
            duty_cycle (float): duty cycle value from 0 to 1.0
        """
        return self.pwm.duty_cycle

    def set_polarity_pwm(self, polarity: Polarity = None):
        """
        Set pwm polarity
        Args:
            polarity (Polarity)
        Return:
            N/A
        """
        if polarity == Polarity.NORMAL:
            self.pwm.polarity = "normal"
        elif polarity == Polarity.INVERSED:
            self.pwm.polarity = "inversed"
        else:
            raise ValueError(f"{polarity} is not a valid value for polarity.")

    def get_polarity_pwm(self):
        """
        Get pwm polarity
        Args:
            N/A
        Return:
            polarity (Polarity)
        """
        if self.pwm.polarity == "normal":
            return Polarity.NORMAL
        if self.pwm.polarity == "inversed":
            return Polarity.INVERSED

        raise ValueError(f"{self.pwm.polarity} is not a valid value for polarity.")

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
