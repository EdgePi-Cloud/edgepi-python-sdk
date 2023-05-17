# EdgePi PWM Module
PWM modules is used to modify the output of A/DOUT1 and A/DOUT2 pins to PWM signal.

# Hardware
A/DOUT1 and A/DOUT2 can be configured to provide vairable PWM signal.

# Example Code
```python
from edgepi.pwm.pwm_constants import Polarity, PWMPins
from edgepi.pwm.edgepi_pwm import EdgePiPWM

# Enable PWM1
edgepi_pwm = EdgePiPWM()

# Initialize and open pwm device
edgepi_pwm.init_pwm(PWMPins.PWM1)
# Setting PWM parameters
edgepi_pwm.set_config(PWMPins.PWM1, 1000, 50)
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