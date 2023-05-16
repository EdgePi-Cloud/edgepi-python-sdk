# EdgePi PWM Module
PWM modules is used to modify the output of A/DOUT1 and A/DOUT2 pins to PWM signal.

# Hardware
A/DOUT1 and A/DOUT2 can be configured to provide vairable PWM signal.

# Example Code
```python
from edgepi.pwm.pwm_constants import Polarity, PWMPins
from edgepi.pwm.edgepi_pwm import EdgePiPWM

# Enable PWM1
edgepi_pwm = EdgePiPWM(PWMPins.PWM1)

# Set frequency to 1KHz
edgepi_pwm.set_frequency(1000)
# Set Duty Cycle to 50 %
edgepi_pwm.set_duty_cycle(0.5)
# Set polarity of PWM to Normal
edgepi_pwm.set_polarity(Polarity.NORMAL)
# enable the pwm signal 
edgepi_pwm.enable()
# disable the pwm signal 
edgepi_pwm.disable()
# Close PWM device
edgepi_pwm.close()

```

# User Guide
- Instantiating the module generate the PWM device file
- frequency and duty cycle must be set before enabling the PWM signal
- the instantiated PWM device must be closed when it is no longer used.


# Limitations 