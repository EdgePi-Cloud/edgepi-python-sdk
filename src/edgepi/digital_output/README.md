# EdgePi Digital Output Module
Digital output modules is used to modify the output value of digital output pins.

# Hardware
A/DOUT1-8 allow the user to modify the direction and output state of the corresponding pins.

# Example Code
```python
from edgepi.gpio.gpio_constants import GpioPins
from edgepi.digital_output.edgepi_digital_output import EdgePiDigitalOutput

digital_output = EdgePiDigitalOutput()

# setting corresponding GpioPin to Output direction
digital_output.digital_output_direction(GpioPins.DOUT1, False)
digital_output.digital_output_direction(GpioPins.DOUT2, False)
digital_output.digital_output_direction(GpioPins.DOUT3, False)
digital_output.digital_output_direction(GpioPins.DOUT4, False)
digital_output.digital_output_direction(GpioPins.DOUT5, False)
digital_output.digital_output_direction(GpioPins.DOUT6, False)
digital_output.digital_output_direction(GpioPins.DOUT7, False)
digital_output.digital_output_direction(GpioPins.DOUT8, False)

# setting corresponding GpioPin to output High/On
digital_output.digital_output_state(GpioPins.DOUT1, True)
digital_output.digital_output_state(GpioPins.DOUT2, True)
digital_output.digital_output_state(GpioPins.DOUT3, True)
digital_output.digital_output_state(GpioPins.DOUT4, True)
digital_output.digital_output_state(GpioPins.DOUT5, True)
digital_output.digital_output_state(GpioPins.DOUT6, True)
digital_output.digital_output_state(GpioPins.DOUT7, True)
digital_output.digital_output_state(GpioPins.DOUT8, True)

# setting corresponding GpioPin to output Low/Off
digital_output.digital_output_state(GpioPins.DOUT1, False)
digital_output.digital_output_state(GpioPins.DOUT2, False)
digital_output.digital_output_state(GpioPins.DOUT3, False)
digital_output.digital_output_state(GpioPins.DOUT4, False)
digital_output.digital_output_state(GpioPins.DOUT5, False)
digital_output.digital_output_state(GpioPins.DOUT6, False)
digital_output.digital_output_state(GpioPins.DOUT7, False)
digital_output.digital_output_state(GpioPins.DOUT8, False)
```


# Functionalities

```python
    def digital_output_state(self, pin_name: GpioPins = None, state: bool = None)
        """
        change the output state of the pin to the state passed as argument
        Args:
            pin_name (GpioPins): GpioPin enums
            state (bool): True = output high, False, output low
        """
```
Take `pin_name` and `state` as a parameter and sets the output state of the corresponding pin with the state passed.
```python
    def digital_output_direction(self, pin_name: GpioPins = None, direction: bool = None):
        """
        change the output state of the pin to the state passed as argument
        Args:
            pin_name (GpioPins): GpioPin enums
            state (bool): True = direction input, False = direction output
        """
```
Take `pin_name` and `direction` as a parameter and sets the direction of the corresponding pin with the state passed.

# User Guide
- In order to modify A/DOUT1-8, use GpioPins.DOUT1-8 enum as shown in the example code

# Limitations 
- /dev/gpiochip0 character device is used for handling digital output pin 1 and 2
- GPIO expander chip is used for handling digital output pin 3-8