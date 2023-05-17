# EdgePi Digital Output Module
Digital output modules is used to modify the output value of digital output pins.

# Hardware
A/DOUT1-8 allow the user to modify the direction and output state of the corresponding pins.

# Example Code
```python
from edgepi.digital_output.digital_output_constants import DoutPins, DoutTriState
from edgepi.digital_output.edgepi_digital_output import EdgePiDigitalOutput

digital_output = EdgePiDigitalOutput()

# setting corresponding GpioPin to output High/On
digital_output.set_dout_state(DoutPins.DOUT1, DoutTriState.HIGH)
digital_output.set_dout_state(DoutPins.DOUT2, DoutTriState.HIGH)
digital_output.set_dout_state(DoutPins.DOUT3, DoutTriState.HIGH)
digital_output.set_dout_state(DoutPins.DOUT4, DoutTriState.HIGH)
digital_output.set_dout_state(DoutPins.DOUT5, DoutTriState.HIGH)
digital_output.set_dout_state(DoutPins.DOUT6, DoutTriState.HIGH)
digital_output.set_dout_state(DoutPins.DOUT7, DoutTriState.HIGH)
digital_output.set_dout_state(DoutPins.DOUT8, DoutTriState.HIGH)

# setting corresponding GpioPin to output Low/Off
digital_output.set_dout_state(DoutPins.DOUT1, DoutTriState.LOW)
digital_output.set_dout_state(DoutPins.DOUT2, DoutTriState.LOW)
digital_output.set_dout_state(DoutPins.DOUT3, DoutTriState.LOW)
digital_output.set_dout_state(DoutPins.DOUT4, DoutTriState.LOW)
digital_output.set_dout_state(DoutPins.DOUT5, DoutTriState.LOW)
digital_output.set_dout_state(DoutPins.DOUT6, DoutTriState.LOW)
digital_output.set_dout_state(DoutPins.DOUT7, DoutTriState.LOW)
digital_output.set_dout_state(DoutPins.DOUT8, DoutTriState.LOW)

# setting corresponding GpioPin to high impedance state
digital_output.set_dout_state(DoutPins.DOUT1, DoutTriState.HI_Z)
digital_output.set_dout_state(DoutPins.DOUT2, DoutTriState.HI_Z)
digital_output.set_dout_state(DoutPins.DOUT3, DoutTriState.HI_Z)
digital_output.set_dout_state(DoutPins.DOUT4, DoutTriState.HI_Z)
digital_output.set_dout_state(DoutPins.DOUT5, DoutTriState.HI_Z)
digital_output.set_dout_state(DoutPins.DOUT6, DoutTriState.HI_Z)
digital_output.set_dout_state(DoutPins.DOUT7, DoutTriState.HI_Z)
digital_output.set_dout_state(DoutPins.DOUT8, DoutTriState.HI_Z)
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