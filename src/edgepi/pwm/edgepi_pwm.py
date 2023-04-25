
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
        self.chip = pwm_num.value.chip
        self.channel = pwm_num.value.channel
        self.freq = freq
        self.duty_cycle = duty_cycle
        self.polarity = polarity.value
    

# TODO: set PWM, change GPIO pins
# TODO: set freq, duty cycle
# TODO: close PWM