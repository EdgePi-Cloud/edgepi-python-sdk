# EdgePi Thermocouple Module User Guide
____
## Installing EdgePi SDK Package via Pip
- Inside a virtual environment, run the following:
- Via GitHub HTTPS 
    * `$ python -m pip install https://github.com/osensa/edgepi-python-sdk/tree/abstract-config`
    * Note: since this repository is currently private, you will be required to input your personal access token. See this [guide]([https://link-url-here.org](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)) for creating one, if you do not yet have one.
- Via TestPyPi
    * `$ python -m pip install -i https://test.pypi.org/simple/ EdgePi-Python-SDK`
____
## Importing Thermocouple Module from SDK Package
```
from edgepi.edgepi_tc import EdgePiTC
from edgepi.tc.tc_constants import *

# initialize thermocouple
edgepi_tc = EdgePiTC()
```
___
## Using Thermocouple Module
- Configuring multiple thermocouple settings at once:
    * `edgepi_tc.set_config(conversion_mode=ConvMode.SINGLE, tc_type=TCType.TYPE_K, average_mode=AvgMode.AVG_1)`
        * Note: the Enums being passed as arguments above are available in the `tc_constants` module. Please only pass these as arguments to `edgepi_tc` module methods.
- Configuring thermocouple settings individually:
    * `edgepi_tc.set_average_mode(AvgMode.AVG_4)`
- Using thermocouple to make a single temperature measurement
    * `edgepi_tc.single_sample()`
 ____
 ## class EdgePiTC Guide
 The `EdgePiTC` class contains all methods for configuring and issuing commands to the EdgePi thermocouple. `EdgePiTC` methods which accept arguments should only receive as arguments, the Enums in the `tc_constants` module.
 * `set_config`: use this method when you wish to configure multiple thermocouple settings at once. Note, below are outlined methods for configuring the same settings individually as well.
     - This method is intended to accept `tc_constants` Enums as arguments. The method docstring outlines which specific `tc_constants` Enum is required by each parameter.
 * `set_average_mode`: use this method to set the number of samples taken by the thermocouple for each temperature measurement. Note, increasing the number of samples will increase temperature conversion time while decreasing sample noise. Do not change the averaging mode while temperature conversion are taking place.
    - Use `AvgMode` Enums as arguments
* `set_type`: use this method to set the thermocouple type, from a set of common thermocouple types.
    - Use `TCType` Enums as arguments
* `auto_sample_mode`: use this method to set the thermocouple to perform temperature conversions continuously. Note, applying this setting will result in the thermocouple immediately and automatically triggering conversions until it is switched back to single shot mode. The time between conversions varies depending on the settings currently activated on the thermocouple, but generally requires one to a few hundred milliseconds. To access these measurements, the `read_temps` method can be called.
* `read_temps`: use this method to read temperature measurements from the cold-junction sensor and linearized thermocouple temperature, while conversions are set to occur continuously.
* `single_sample`: use this method to trigger a single temperature conversion while conversions are set to single shot mode.
 ___
## Using OpCodes
Below is a guide showing the purpose of each `tc_constants` Enum, and which Enums to use with each `EdgePiTC` method.

* class TCOps:
    - Commands that can be sent to the thermocouple.
        * `TCOps.SINGLE`: trigger a single temperature conversion.
        * `TCOps.CLEAR_FAULTS`: when using thermocouple in Interrupt Fault Mode, this will clear the Fault Status register
* class DecBits:
    - Settings for setting temperature threshold registers. These enums specify the decimal values permitted by MAX31856 for temperature threshold setting, due to the limited precision offered by the number of bits assigned to decimal places (refer to MAX31856 documentation for more detail).
        * Example: `DecBits.p1` = 0.5 --> this allows you to specify a temperature threshold with a decimal value of 0.5, i.e. 21.5
* class CJMode:
    - Settings for enabling or disabling the thermocouple cold junction sensor.
        * `CJMode.ENABLE`: enable the thermocouple cold junction sensor
        * `CJMode.DISABLE`: disable the thermocouple cold junction sensor
* class FaultMode:
    - Settings for the thermocouple fault status reading mode.
        * `FaultMode.COMPARATOR`: faults in fault status register will deassert only once the fault condition is no longer true
        * `FaultMode.INTERRUPT`: faults in fault status register will deassert only once a `TCOps.CLEAR_FAULTS` command is sent to the thermocouple.
* class NoiseFilterMode
    - Settings for thermocouple noise filter mode. Only modify when thermocouple is in single sample mode, not continuous mode.
        * `NoiseFilterMode.Hz_60`: reject 60 Hz and its harmonics
        * `NoiseFilterMode.Hz_50`: reject 50 Hz and its harmonics
* class AvgMode
    - Settings for thermocouple averaging mode.
        * `AvgMode.AVG_1`: perform a single sample per temperature conversion
        * `AvgMode.AVG_2`: perform 2 samples per temperature conversion
        * `AvgMode.AVG_4`: perform 4 samples per temperature conversion
        * `AvgMode.AVG_8`: perform 8 samples per temperature conversion
        * `AvgMode.AVG_2`16: perform 16 samples per temperature conversion
* class TCType
    - Settings for thermocouple type
        * `TCType.TYPE_B`: indicates a type B thermocouple
        * `TCType.TYPE_E`: indicates a type E thermocouple
        * `TCType.TYPE_J`: indicates a type J thermocouple
        * `TCType.TYPE_K`: indicates a type K thermocouple
        * `TCType.TYPE_N`: indicates a type N thermocouple
        * `TCType.TYPE_R`: indicates a type R thermocouple
        * `TCType.TYPE_S`: indicates a type S thermocouple
        * `TCType.TYPE_T`: indicates a type T thermocouple
* class VoltageMode
    - Settings for thermocouple voltage mode. Use to set thermocouple type if your thermocouple type is not listed under TCType thermocouples.
        * `VoltageMode.GAIN_8`: full-scale input voltage range of +/- 78.125 mV
        * `VoltageMode.GAIN_32`: full-scale input voltage range of +/- 19.531 mV
