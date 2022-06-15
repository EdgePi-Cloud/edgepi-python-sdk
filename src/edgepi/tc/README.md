# EdgePi Thermocouple Module User Guide
____
## Installing EdgePi SDK Package via Pip
- Inside a virtual environment, run either of the following to install:
- Via GitHub HTTPS 
    * `$ python3 -m pip install https://github.com/osensa/edgepi-python-sdk/tree/abstract-config`
        - [ ] branch name needs to be updated to main once current changes are deployed
    * Note: since this repository is currently private, you will be required to input your personal access token. See this [guide]([https://link-url-here.org](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)) for creating a personal access token, if you do not yet have one.
- Via TestPyPi
    * `$ python3 -m pip install -i https://test.pypi.org/simple/ EdgePi-Python-SDK`
- Via PyPi
    * ` $ python3 -m pip install EdgePi-Python-SDK`
        - [ ] Note, the SDK is not yet available on PyPi. The package name here is a placeholder and will have to be replaced.
____
## Quick Use Example

This section will demonstrate how to import the EdgePi Thermcouple module, and use it to continuously monitor cold-junction and linearized
thermocouple temperature measurements.

```
from edgepi.edgepi_tc import EdgePiTC
from edgepi.tc.tc_constants import *

# initialize thermocouple
edgepi_tc = EdgePiTC()

# read temperature measurements continuously every 1 second.
edgepi_tc.set_config(conversion_mode=ConvMode.AUTO)

stop_condition = False

while True:
  time.sleep(1)                           # wait 1 second between measurements
  temps = edgepi_tc.read_temperatures()   # read cold-junction and linearized thermocouple temperatures
  print(temps)

  # stop continuous measurements if some condition is met
  if stop_condition:
      edgepi_tc.set_config(conversion_mode=ConvMode.SINGLE)
      break
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
 
 | Method | Description |
 | --- | --- |
 | `set_config` | Use this method when you wish to configure multiple thermocouple settings at once. Note, below are outlined methods for configuring the same settings individually as well. This method is intended to accept `tc_constants` Enums as arguments. The method docstring provides more details on which specific `tc_constants` Enum is required by each parameter. |
 | `set_average_mode` | Use this method to set the number of samples taken by the thermocouple for each temperature measurement. Note, increasing the number of samples will increase temperature conversion time, while decreasing sample noise. Do not change the averaging mode while temperature conversion are taking place. Arguments are expected to be `AvgMode` Enums. |
 | `auto_sample_mode` | Use this method to set the thermocouple to perform temperature conversions continuously. Note, applying this setting will result in the thermocouple immediately and automatically triggering conversions until it is switched back to single shot mode. The time between conversions varies depending on the thermocouple's settings configuration, but generally requires one hundred to a few hundred milliseconds. To access these measurements, the `read_temperatures` method can be called. Make sure to allow enough time between readings. |
 | `read_temperatures` | Use this method to read cold-junction sensor and linearized thermocouple temperature measurements, while conversions are set to occur continuously. |
| `single_sample` | Use this method to trigger a single temperature conversion while conversions are set to single shot mode. Note, this method will return the measured temperatures, so there is no need to call `read_temperatures` as with auto sampling. |
 ___
## Using OpCodes
The methods outline above are designed to accept predefined Enums, which contain the OpCodes necessary to perform each transaction, as arguments. These are defined in the `tc_constants` module. Below is a guide showing the purpose of each `tc_constants` Enum and OpCode, and which Enums to use with each `EdgePiTC` method. Please avoid passing any other values as arguments to the `EdgePiTC` methods, as this can result in undefined behaviour.

<table>
   <tr>
      <th>Class</th>
      <th>Description</th>
      <th>OpCodes</th>
   </tr>
   <tr>
      <td><code>TCOps</code></td>
      <td>Commands that can be sent to the thermocouple.</td>
      <td>
         <ul>
            <li><code>TCOps.SINGLE</code>: trigger a single temperature conversion.</li>
            <li><code>TCOps.CLEAR_FAULTS</code>: clear the Fault Status register, when using thermocouple in Interrupt Fault Mode</li>
         </ul>
      </td>
   </tr>
   <tr>
      <td><code>DecBits</code></td>
      <td>Use for setting temperature threshold registers. These enums specify the decimal values permitted by MAX31856 for temperature threshold registers. Only these values are permitted for specifying decimal values, due to the limited precision offered by the number of bits assigned to decimal places (refer to MAX31856 documentation for more details).</td>
      <td>Example: <code>DecBits.p1</code> allows you to specify a temperature threshold with a decimal value of 0.5, i.e. 21.5.</td>
   </tr>
   <tr>
      <td><code>CJMode</code></td>
      <td>Settings for enabling or disabling the thermocouple cold junction sensor.</td>
      <td>
         <ul>
            <li><code>CJMode.ENABLE</code>: enable the thermocouple cold junction sensor</li>
            <li><code>CJMode.DISABLE</code>: disable the thermocouple cold junction sensor</li>
         </ul>
      </td>
   </tr>
   <tr>
      <td><code>FaultMode</code></td>
      <td>Settings for the thermocouple fault status reading mode.</td>
      <td>
         <ul>
            <li><code>FaultMode.COMPARATOR</code>: faults in fault status register will deassert only once the fault condition is no longer true.</li>
            <li><code>FaultMode.INTERRUPT</code>: faults in fault status register will deassert only once a <code>TCOps.CLEAR_FAULTS</code> command is sent to the thermocouple.</li>
         </ul>
      </td>
   </tr>
   <tr>
      <td><code>NoiseFilterMode</code></td>
      <td>Settings for thermocouple noise filter mode. Only modify when thermocouple is in single sample mode, not continuous mode.</td>
      <td>
         <ul>
            <li><code>NoiseFilterMode.Hz_60</code>: reject 60 Hz and its harmonics</li>
            <li><code>NoiseFilterMode.Hz_50</code>: reject 50 Hz and its harmonics</li>
         </ul>
      </td>
   </tr>
   <tr>
      <td><code>AvgMode</code></td>
      <td>Settings for thermocouple averaging mode.</td>
      <td>
         <ul>
            <li><code>AvgMode.AVG_1</code>: perform a single sample per temperature conversion</li>
            <li><code>AvgMode.AVG_2</code>: perform 2 samples per temperature conversion</li>
            <li><code>AvgMode.AVG_4</code>: perform 4 samples per temperature conversion</li>
            <li><code>AvgMode.AVG_8</code>: perform 8 samples per temperature conversion</li>
            <li><code>AvgMode.AVG_16</code>: perform 16 samples per temperature conversion</li>
         </ul>
      </td>
   </tr>
   <tr>
      <td><code>TCType</code></td>
      <td>Settings for thermocouple type. Note, if your thermocouple type is not listed here, see <code>VoltageMode</code> settings below.</td>
      <td>
         <ul>
            <li><code>TCType.TYPE_B</code>: indicates a type B thermocouple</li>
            <li><code>TCType.TYPE_E</code>: indicates a type E thermocouple</li>
            <li><code>TCType.TYPE_J</code>: indicates a type J thermocouple</li>
            <li><code>TCType.TYPE_K</code>: indicates a type K thermocouple</li>
            <li><code>TCType.TYPE_N</code>: indicates a type N thermocouple</li>
            <li><code>TCType.TYPE_R</code>: indicates a type R thermocouple</li>
            <li><code>TCType.TYPE_S</code>: indicates a type S thermocouple</li>
            <li><code>TCType.TYPE_T</code>: indicates a type T thermocouple</li>
         </ul>
      </td>
   </tr>
   <tr>
      <td><code>VoltageMode</code></td>
      <td>Settings for thermocouple voltage mode. Use to set thermocouple type if your thermocouple type is not listed under <code>TCType</code> thermocouples.</td>
      <td>
         <ul>
            <li><code>VoltageMode.GAIN_8</code>: full-scale input voltage range of +/- 78.125 mV</li>
            <li><code>VoltageMode.GAIN_32</code>:  full-scale input voltage range of +/- 19.531 mV</li>
         </ul>
      </td>
   </tr>
</table>
