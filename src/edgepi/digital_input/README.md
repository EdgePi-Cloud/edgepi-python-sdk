# EdgePi Digital Input Module
Digital input modules is used to read the current digital pin states.

# Hardware
A/DIN1-8 allow the user to connect digitial signals for sampling the state of the corresponding signals.

# Example Code
```python
from edgepi.gpio.gpio_constants import GpioPins
from edgepi.digital_input.edgepi_digital_input import EdgePiDigitalInput

digital_input = EdgePiDigitalInput()
pin_1_state = digital_input.digital_input_state(GpioPins.DIN1)
pin_2_state = digital_input.digital_input_state(GpioPins.DIN2)
pin_3_state = digital_input.digital_input_state(GpioPins.DIN3)
pin_4_state = digital_input.digital_input_state(GpioPins.DIN4)
pin_5_state = digital_input.digital_input_state(GpioPins.DIN5)
pin_6_state = digital_input.digital_input_state(GpioPins.DIN6)
pin_7_state = digital_input.digital_input_state(GpioPins.DIN7)
pin_8_state = digital_input.digital_input_state(GpioPins.DIN8)

```


# Functionalities

```python
    def digital_input_state(self, pin_name: GpioPins = None)
```
Take `pin_name` as a parameter and returns a boolean value of the corresponding state.

# User Guide
- In order to read A/DIN1-8, use GpioPins.DIN1-8 enum as shown in the example code

# Limitations 
- /dev/gpiochip0 character device is used for handling digital input pins
- only read function implemented, GPIO polling and edge_event are not implemented.


