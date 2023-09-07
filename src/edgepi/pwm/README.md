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
# Setting PWM parameters, frequency 1000.0 to 10,000.0 , duty cycle form 0-1.0
edgepi_pwm.set_config(PWMPins.PWM1, 1000.0, 0.50)
# enable the pwm signal, PWM duty cycle and frequency must be set to enable the singal
edgepi_pwm.enable(PWMPins.PWM1)
# disable the pwm signal 
edgepi_pwm.disable(PWMPins.PWM1)
# Close PWM device
edgepi_pwm.close(PWMPins.PWM1)

```
__NOTE__: Frequency and duty-cycle must be set before enabling the PWM signal.

# User Guide
- Instantiating the module generate the PWM device file
- frequency and duty cycle must be set before enabling the PWM signal
- the instantiated PWM device must be closed when it is no longer used.


# Limitations 