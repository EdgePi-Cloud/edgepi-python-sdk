# EdgePi DAC Module User Guide
___
## Quick Use Example

This section will demonstrate how to import the EdgePi DAC module, and use it write a voltage value to an EdgePi analog out pin.
Note, the EdgePi has eight analog out pins, indexed from 1 to 8.

### Writing Voltage to Analog Out Pin
```python
from edgepi.dac.dac_constants import DACChannel as Ch
from edgepi.dac.edgepi_dac import EdgePiDAC

# initialize DAC
edgepi_dac = EdgePiDAC()

# setting DAC range 0-5V
edgepi_dac.enable_dac_gain(False)

# write voltage value of 3.3 V to analog out pin number 1
edgepi_dac.write_voltage(Ch.AOUT1, 3.3)

# read state of DAC output 1
code, voltage, gain = edgepi_dac.get_state(Ch.AOUT1, True, True, True)

# Resets the DAC to power-on reset state
edgepi_dac.reset()
```
---
## Using DAC Module
This section introduces DAC functionality available to users, and provides a guide on how to interact with the DAC module.

1. Writing Voltage to Analog Out Pins
    - Write a voltage value to be sent through an analog output pin
3. Reading Voltage from Analog Out Pins
    - Read voltage from DAC channel corresponding to an analog out pin
4. Setting Power Mode Analog Out Pins
    - Each analog out pin can be configured to operate in lower power consumption modes.
5. Resetting DAC
    - Performs a software reset of the DAC, returning all settings and values to the default power-on state.
