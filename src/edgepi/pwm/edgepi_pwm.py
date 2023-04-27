
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
        super().__init__(channel=pwm_num.value.chip, chip=pwm_num.value.chip)
        self.open_pwm()
        self.freq = freq
        self.duty_cycle = duty_cycle
        self.polarity = polarity.value

# TODO: set PWM, change GPIO pins
# TODO: set freq, duty cycle
# TODO: close PWM
    def set_frequency(self, frequency: int):
        """
        Set frequency
        """
    def get_frequency(self):
        """
        Get frequency
        """ 

    def set_dutycycle(self, duty_cycle: float):
        """
        Set Duty Cycle
        """
    
    def get_dutycycle(self):
        """
        get Duty cycle
        """

    def set_polarity(self, polarity: Polarity):
        """
        Set Duty Cycle
        """
    
    def get_polarity(self):
        """
        get Duty cycle
        """
    
    def enable_pwm(self):
        """
        Enable pwm output
        """
    
    def disable_pwm(self):
        """
        Disable pwm output
        """

    def get_enabled(self):
        """
        Get enabled state
        """

    def close(self):
        """
        Close PWM connection
        Args:
            N/A
        Returns:
            N/A
        """
        self.close_pwm()
