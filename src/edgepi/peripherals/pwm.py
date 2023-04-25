"""
Module for PWM devices
"""


from periphery import PWM


class PwmDevice:
    """Class for representing a PWM device"""

    def __init__(self, chip: int = None, channel: int = None):
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

    def set_duty_cycle_pwm(self, duty_cycle: float = None):
        """
        set pwm duty cycle
        Args:
            duty_cycle (float): duty cycle value from 0 to 1.0
        Return:
            N/A
        """
        self.pwm.duty_cycle = duty_cycle

    def set_polarity_pwm(self, polarity: str = None):
        """
        set pwm polarity
        Args:
            polarity (str): "Normal" or "Inversed"
        Return:
            N/A
        """
        self.pwm.polarity = polarity

    def close_pwm(self):
        """Close pwm connection"""
        self.pwm.close()
