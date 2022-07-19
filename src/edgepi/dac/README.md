# EdgePi DAC Module User Guide
___
## Quick Use Example

This section will demonstrate how to import the EdgePi DAC module, and use it write a voltage value to an EdgePi analog out pin.
Note, the EdgePi has eight analog out pins, indexed from 1 to 8.

### Writing Voltage to Analog Out Pin
```
from edgepi.dac.edgepi_dac import EdgePiDAC

# initialize DAC
edgepi_dac = EdgePiDAC()

# write voltage value of 3.3 V to analog out pin number 1
edgepi_dac.write_voltage(1, 3.3)
```
---
## Using DAC Module
This section introduces DAC functionality available to users, and provides a guide on how to interact with the DAC module.

1. Writing Voltage to Analog Out Pins
    - Write a voltage value to be sent through an analog output pin
3. Reading Voltage
    - **TODO**: unclear what exactly the read operation is reading
4. Setting Power Mode Analog Out Pins
    - Each analog out pin can be configured to operate in lower power consumption modes.
5. Setting DAC Output Amplifier Gain
7. Resetting Values
    - **TODO**: unclear what values this is resetting
