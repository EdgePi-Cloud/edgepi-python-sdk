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
edgepi_dac.toggle_dac_gain(False)

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

1. setting output voltage range

```python
    def set_dac_gain(self, set_gain: bool, auto_code_change: bool = False):
        """
        Enable/Disable internal DAC gain by toggling the DAC_GAIN pin
        Args:
            set_gain (bool): enable boolean to set or clear the gpio pin
            auto_code_change (bool): flag to re-write code value of each channel to keep the same
                                    output voltage
        Return:
            gain_state (bool): state of the gain pin
        """
```

2. set output voltage

```python
    def write_voltage(self, analog_out: DACChannel, voltage: float):
        """
        Write a voltage value to an analog out pin. Voltage will be continuously
        transmitted to the analog out pin until a 0 V value is written to it.

        Args:
            `analog_out` (DACChannel): A/D_OUT pin to write a voltage value to.

            `voltage` (float): the voltage value to write, in volts.

        Raises:
            `ValueError`: if voltage has more decimal places than DAC accuracy limit
        """
```

3. reading channel state 

```python
    def get_state(self, analog_out: DACChannel = None,
                        code: bool = None,
                        voltage: bool = None,
                        gain: bool = None):
        """
        the method returns the state of requested parameters. It will either read the register of
        DAC or GPIO expander to retrieve the current state.

        Args:
            analog_out (DACChannel): channel number of interest
            code (bool): requesting the current code value written in the specified channel input
                         register
            voltage (bool): requesting the current expected voltage at the terminal block pin
            gian (bool): requesting the current gain value set for the DAC
        Returns:
            code_val (int): code value read from the input register, None when not requested
            voltage_val (float): voltage calculated using the code value, None when not requested
            gain_state (bool): true if dac gain is enabled or False disabled, None when not
                               requested
        """
```

4. Resetting DAC to power-on reset state

```python
    def reset(self):
        """
        Performs a software reset of the EdgePi DAC to power-on default values,
        and stops all voltage transmissions through pins.
        """
        cmd = self.dac_ops.combine_command(COM.COM_SW_RESET.value, NULL_BITS, SW_RESET)
        self.transfer(cmd)
```
