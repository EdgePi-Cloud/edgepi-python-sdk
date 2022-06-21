# EdgePi Thermocouple Module User Guide
____
## Quick Use Example

This section will demonstrate how to import the EdgePi Thermcouple module, and use it to make cold-junction and linearized thermocouple temperature measurement. The first example shows how to do this manually, and the second shows how use the thermocouple's continuous conversion functionality to make measurements automatically.

### Manual Measurements
```
from edgepi.edgepi_tc import EdgePiTC

# initialize thermocouple
edgepi_tc = EdgePiTC()

# make a single temperature measurement
temps = edgepi_tc.single_sample()
print(temps)
```

### Automatic Measurements
```
import time
from edgepi.edgepi_tc import EdgePiTC
from edgepi.tc.tc_constants import *

# initialize thermocouple
edgepi_tc = EdgePiTC()

# set thermocouple to measure temperature continuously
edgepi_tc.set_config(conversion_mode=ConvMode.AUTO)

# sample temperature readings 10 times, once per second
for num_measurements in range(10):
  time.sleep(1)                           # wait 1 second between samples
  temps = edgepi_tc.read_temperatures()   # read cold-junction and linearized thermocouple temperatures
  print(temps)

# stop continuous measurements once you're done sampling
edgepi_tc.set_config(conversion_mode=ConvMode.SINGLE)
```
___
## Using Thermocouple Module

This section introduces thermocouple functionality available to users, and provides a guide on how to interact with the thermocouple.

1. ### Configuring Thermocouple Settings:
    * The thermocouple has settings which can be configured. In order to allow you to configure these settings, this module provides a `set_config` method. 
    * Example: using `set_config` to configure multiple settings at once:
        * `edgepi_tc.set_config(conversion_mode=ConvMode.SINGLE, tc_type=TCType.TYPE_K, average_mode=AvgMode.AVG_1)`
    * Example: using `set_config` to configure a single setting:
        * `edgepi_tc.set_config(average_mode=AvgMode.AVG_8)`
     * Note: the constants being passed as arguments above are available in the `tc_constants` module. Please see the EdgePiTC Guide section below for more details.
2. ### Measuring Temperature:
    - Measuring temperature manually
        * The thermocouple is set by default to function in single shot mode. When in single shot mode, temperature measurements must be triggered manually by sending a command to the thermocouple. This command can be sent via the `single_sample` method, which will return both the cold-junction sensor temperature and the linearized thermocouple temperature:
            - `edgepi_tc.single_sample()`
        * Note, if the thermocouple is not in single shot mode, you must set to it single shot mode before calling `single_sample`. To do this:
            - `edgepi_tc.set_config(conversion_mode=ConvMode.SINGLE)`
    - Measuring temperature continuously
        * If instead you wish to have the thermocouple perform temperature measurements automatically, you can enable auto conversion mode, like so:
            - `edgepi_tc.set_config(conversion_mode=ConvMode.AUTO)`
        * After enabling auto conversion mode, the thermocouple will begin automatically triggering a temperature measurement periodically. Note, while the thermocouple will automatically make and store temperature measurements, you must retrieve these by calling `read_temperatures()`:
            - ` temps = edgepi_tc.read_temperatures()`
3. ### Reading Thermocouple Faults
    * The thermocouple can store information about its current operating status. If there are any faults, such as open circuits, this information will be updated and stored in the thermocouple. This module provides you with the ability to read the current fault status of the thermocouple.
        - [ ] this has not yet been implemented and needs updating
 ____
 ## class EdgePiTC Guide
 The `EdgePiTC` class contains all methods for configuring and issuing commands to the EdgePi thermocouple. `EdgePiTC` methods which accept arguments should only receive as arguments, the Enums in the `tc_constants` module.
 
 | Method | Description |
 | --- | --- |
 | `set_config` | Use this method when you wish to configure either individual thermocouple settings, or multiple thermocouple settings at once. This method is intended to accept `tc_constants` Enums as arguments. The method docstring provides more details on which specific `tc_constants` Enum is required by each parameter. |
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
