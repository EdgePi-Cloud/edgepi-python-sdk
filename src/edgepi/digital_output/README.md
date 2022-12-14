# EdgePi Digital Output Module
Digital output modules is used to modify the output value of digital output pins.

# Hardware
A/DOUT1-8 allow the user to modify the direction and output state of the corresponding pins.

# Example Code
```python
from edgepi.gpio.gpio_constants import GpioPins
from edgepi.digital_output.edgepi_digital_output import EdgePiDigitalOutput

digital_output = EdgePiDigitalOutput()

pin_1_state = digital_output.digital_output_direction(GpioPins.DIN1, True)
pin_2_state = digital_output.digital_output_direction(GpioPins.DIN2, True)
pin_3_state = digital_output.digital_output_direction(GpioPins.DIN3, True)
pin_4_state = digital_output.digital_output_direction(GpioPins.DIN4, True)
pin_5_state = digital_output.digital_output_direction(GpioPins.DIN5, True)
pin_6_state = digital_output.digital_output_direction(GpioPins.DIN6, True)
pin_7_state = digital_output.digital_output_direction(GpioPins.DIN7, True)
pin_8_state = digital_output.digital_output_direction(GpioPins.DIN8, True)

pin_1_state = digital_output.digital_output_state(GpioPins.DIN1, True)
pin_2_state = digital_output.digital_output_state(GpioPins.DIN2, True)
pin_3_state = digital_output.digital_output_state(GpioPins.DIN3, True)
pin_4_state = digital_output.digital_output_state(GpioPins.DIN4, True)
pin_5_state = digital_output.digital_output_state(GpioPins.DIN5, True)
pin_6_state = digital_output.digital_output_state(GpioPins.DIN6, True)
pin_7_state = digital_output.digital_output_state(GpioPins.DIN7, True)
pin_8_state = digital_output.digital_output_state(GpioPins.DIN8, True)

```


# Functionalities

```python
    def digital_output_state(self, pin_name: GpioPins = None, state: bool = None)
```
Take `pin_name` and `state` as a parameter and sets the output state of the corresponding pin with the state passed.
```python
    def digital_output_direction(self, pin_name: GpioPins = None, direction: bool = None):
```
Take `pin_name` and `direction` as a parameter and sets the direction of the corresponding pin with the state passed.

# User Guide
- In order to modify A/DOUT1-8, use GpioPins.DOUT1-8 enum as shown in the example code

# Limitations 
- /dev/gpiochip0 character device is used for handling digital output pin 1 and 2
- GPIO expander chip is used for handling digital output pin 3-8