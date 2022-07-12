# EdgePi Thermocouple Module User Guide
____
## Quick Use Example

This section will demonstrate how to import the EdgePi Thermcouple module, and use it to make cold-junction and linearized thermocouple temperature measurement. The first example shows how to do this manually, and the second shows how use the thermocouple's continuous conversion functionality to make measurements automatically.

### Manual Measurements
```
from edgepi.edgepi_tc import EdgePiTC
from edgepi.tc.tc_constants import ConvMode

# initialize thermocouple
edgepi_tc = EdgePiTC()

# set thermocouple to single sample mode
edgepi_tc.set_config(conversion_mode=ConvMode.SINGLE)

# make a single temperature measurement
temps = edgepi_tc.single_sample()
print(temps)
```

### Automatic Measurements
```
import time
from edgepi.edgepi_tc import EdgePiTC
from edgepi.tc.tc_constants import ConvMode

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
 ## EdgePiTC Methods Guide
 The `EdgePiTC` class contains all methods for configuring and issuing commands to the EdgePi thermocouple. `EdgePiTC` methods which accept arguments should only receive as arguments, the Enums in the `tc_constants` module.
 
<table>
    <tr>
        <th>Method</th>
        <th>Description</th>
        <th>Input</th>
        <th>Output</th>
    </tr>
    <tr>
        <td><code>set_config</code></td>
        <td>A general use method for configuring thermocouple settings. This method can be used to configure 
            thermocouple settings individually, or multiple settings at once.
        </td>
        <td>
            <p>This method is intended to accept <code>tc_constants</code> Enums as arguments. Please see 
                Using OpCodes below for a comprehensive list of these Enums. In order to use a particular Enum,
                you must first import it from <code>tc_constants</code> like so: 
                <p><code>from edgepi.tc.tc_constants import ConvMode</code></p>
            </p>
            <p>Following are the arguments received by this method and the <code>tc_constants</code> Enums they must be used with</p>
            <ul>
                <li>
                    <p><code>conversion_mode</code> (<code>ConvMode</code>): enable manual or automatic sampling</p>
                </li>
                <li>
                    <p><code>oc_fault_mode</code> (<code>OpenCircuitMode</code>): set open circuit fault detection mode</p>
                </li>
                <li>
                    <p><code>cold_junction_mode</code> (<code>CJMode</code>): enable or disable cold junction sensor</p>
                </li>
                <li>
                    <p><code>fault_mode</code> (<code>FaultMode</code>): set fault reading mode</p>
                </li>
                <li>
                    <p><code>noise_filter_mode</code> (<code>NoiseFilterMode</code>): set which noise frequency to reject</p>
                </li>
                <li>
                    <p><code>average_mode</code> (<code>AvgMode</code>): number of samples to average per temperature measurement</p>
                </li>
                <li>
                    <p><code>tc_type</code> (<code>TCType</code>): set thermocouple type</p>
                </li>
                <li>
                    <p><code>voltage_mode</code> (<code>VoltageMode</code>): set input voltage range</p>
                </li>
                <li>
                    <p><code>cj_high_mask</code> (<code>CJHighMask</code>): choose whether to mask CJHIGH fault from asserting through the FAULT pin</p>
                </li>
                <li>
                    <p><code>cj_low_mask</code> (<code>CJLowMask</code>): choose whether to mask CJLOW fault from asserting through the FAULT pin</p>
                </li>
                <li>
                    <p><code>tc_high_mask</code> (<code>TCLHighMask</code>): choose whether to mask TCHIGH fault from asserting through the FAULT pin</p>
                </li>
                <li>
                    <p><code>tc_low_mask</code> (<code>TCLowMask</code>): choose whether to mask TCLOW fault from asserting through the FAULT pin</p>
                </li>
                <li>
                    <p><code>ovuv_mask</code> (<code>OvuvMask</code>): choose whether to mask OVUV fault from asserting through the FAULT pin</p>
                </li>
                <li>
                    <p><code>open_mask</code> (<code>OpenMask</code>): choose whether to mask OPEN fault from asserting through the FAULT pin</p>
                </li>
                <li>
                    <p><code>cj_high_threshold</code> (<code>int</code>): set cold junction temperature upper threshold. If cold junction temperature rises
                    above this limit, the FAULT output will assert</p>
                </li>
                <li>
                    <p><code>cj_low_threshold</code> (<code>int</code>): set cold junction temperature lower threshold. If cold junction temperature falls
                    below this limit, the FAULT output will assert</p>
                </li>
                <li>
                    <p><code>lt_high_threshold</code> (<code>int</code>): set thermocouple hot junction temperature upper threshold. If thermocouple hot junction 
                    temperature rises above this limit, the FAULT output will assert</p>
                </li>
                <li>
                    <p>
                    <code>lt_high_threshold_decimals</code> (<code>DecBits4</code>): set thermocouple hot junction temperature upper threshold decimal value.
                      Note you <strong>must</strong> set both <code>lt_high_threshold</code> and <code>lt_high_threshold_decimals</code> at the same time.
                    </p>
                </li>
                <li>
                    <p><code>lt_low_threshold</code> (<code>int</code>): set thermocouple hot junction temperature lower threshold. If thermocouple hot junction 
                    temperature falls below this limit, the FAULT output will assert</p>
                </li>
                <li>
                    <p>
                    <code>lt_low_threshold_decimals</code> (<code>DecBits4</code>): set thermocouple hot junction temperature lower threshold decimal value.
                    Note you <strong>must</strong> set both <code>lt_low_threshold</code> and <code>lt_low_threshold_decimals</code> at the same time.
                    </p>
                </li>
                <li>
                    <p><code>cj_offset</code> (<code>int</code>): set cold junction temperature offset.</p>
                </li>
                <li>
                    <p>
                    <code>cj_offset_decimals</code> (<code>DecBits4</code>): set cold junction temperature offset decimal value.
                    Note you <strong>must</strong> set both <code>cj_offset</code> and <code>cj_offset_decimals</code> at the same time.
                    </p>
                </li>
                <li>
                    <p><code>cj_temp</code> (<code>int</code>): write temperature values to the cold-junction sensor, when it is disabled.</p>
                </li>
                <li>
                    <p>
                    <code>cj_temp_decimals</code> (<code>DecBits6</code>): set cold junction temperature overwrite decimal value.
                    Note you <strong>must</strong> set both <code>cj_temp</code> and <code>cj_temp_decimals</code> at the same time.
                    </p>
                </li>
            </ul>
        </td>
        <td>
            None
        </td>
    </tr>
    <tr>
        <td><code>single_sample</code></td>
        <td>When in single sampling conversion mode, Use this method to trigger a single temperature conversion.</td>
        <td>None</td>
        <td>A tuple containing the measured cold junction and linearized thermocouple temperature measurements, of the format 
            <code>(cold_junction_temperature, linearized_thermocouple_temperature)</code>
        </td>
    </tr>
    <tr>
        <td><code>read_temperatures</code></td>
        <td>When the thermocouple is set to automatic conversion mode, use this method to read cold-junction sensor and linearized thermocouple temperature measurements.</td>
        <td>None</td>
        <td>A tuple containing the measured cold junction and linearized thermocouple temperature measurements, of the format 
            <code>(cold_junction_temperature, linearized_thermocouple_temperature)</code>
        </td>
    </tr>
    <tr>
        <td><code>read_faults</code></td>
        <td>Use for reading the fault status of the thermocouple</td>
        <td>None</td>
        <td>a dictionary of Fault objects, each of which stores information about the fault it represents</td>
    </tr>
    <tr>
        <td><code>clear_faults</code></td>
        <td>
        When in Interrupt Fault Mode, use to clear the Fault Status Register bits and deassert the FAULT pin output.
        Note that the FAULT output and the fault bit may reassert immediately if the fault persists.
        If thermocouple is in Comparator Fault Mode, this will have no effect on the thermocouple.
        </td>
        <td>None</td>
        <td>None</td>
    </tr>
</table>

---
## OpCodes Guide
 
The methods outlined above are designed to accept predefined Enums, which contain the OpCodes necessary to perform each transaction, as arguments. These are defined in the `tc_constants` module. Below is a guide showing the purpose of each `tc_constants` Enum and OpCode, and which Enums to use with each `EdgePiTC` method. Please avoid passing any other values as arguments to the `EdgePiTC` methods, as this can result in undefined behaviour.

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
      <td><code>DecBits4, DecBits6</code></td>
      <td>Use for setting temperature threshold registers. These enums specify the decimal values permitted by MAX31856 for temperature threshold registers. Only these values are permitted for specifying decimal values, due to the limited precision offered by the number of bits assigned to decimal places (refer to MAX31856 documentation for more details). Please refer to documentation above or <code>set_config</code> docstring for whether to use DecBits4 or DecBits6 for setting decimal values</td>
      <td>Example: <code>DecBits4.P0_5</code> or <code>DecBits6.P0_5</code>allows you to specify a temperature threshold with a decimal value of 0.5</td>
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
      <td>Settings for thermocouple voltage mode (for use if your thermocouple type is not list under `TCType`)</td>
      <td>
         <ul>
            <li><code>VoltageMode.GAIN_8</code>: set a full-scale input voltage range of +/- 78.125 mV</li>
           <li><code>VoltageMode.GAIN_32</code>: set a full-scale input voltage range of +/- 19.531 mV</li>
         </ul>
      </td>
   </tr>
   <tr>
      <td><code>OpenMask</code></td>
      <td>Settings for masking OPEN fault</td>
      <td>
         <ul>
           <li><code>OpenMask.OPEN_MASK_ON</code>: mask the OPEN fault from asserting</li>
           <li><code>OpenMask.OPEN_MASK_OFF</code>: do not mask the OPEN fault from asserting</li>
         </ul>
      </td>
   </tr>
   <tr>
      <td><code>OvuvMask</code></td>
      <td>Settings for masking OVUV fault</td>
      <td>
         <ul>
           <li><code>OvuvMask.OVUV_MASK_ON</code>: mask the OVUV fault from asserting</li>
           <li><code>OvuvMask.OVUV_MASK_OFF</code>: do not mask the OVUV fault from asserting</li>
         </ul>
      </td>
   </tr>
   <tr>
      <td><code>TCLowMask</code></td>
      <td>Settings for masking TCLOW fault</td>
      <td>
         <ul>
           <li><code>TCLowMask.TCLOW_MASK_ON</code>: mask the TCLOW fault from asserting</li>
           <li><code>TCLowMask.TCLOW_MASK_OFF</code>: do not mask the TCLOW fault from asserting</li>
         </ul>
      </td>
   </tr>
   <tr>
      <td><code>TCHighMask</code></td>
      <td>Settings for masking TCHIGH fault</td>
      <td>
         <ul>
           <li><code>TCHighMask.TCHIGH_MASK_ON</code>: mask the TCHIGH fault from asserting</li>
           <li><code>TCHighMask.TCHIGH_MASK_OFF</code>: do not mask the TCHIGH fault from asserting</li>
         </ul>
      </td>
   </tr>
   <tr>
      <td><code>CJLowMask</code></td>
      <td>Settings for masking CJLOW fault</td>
      <td>
         <ul>
           <li><code>CJLowMask.CJLOW_MASK_ON</code>: mask the CJLOW fault from asserting</li>
           <li><code>CJLowMask.CJLOW_MASK_OFF</code>: do not mask the CJLOW fault from asserting</li>
         </ul>
      </td>
   </tr>
   <tr>
      <td><code>CJHighMask</code></td>
      <td>Settings for masking CJHIGH fault</td>
      <td>
         <ul>
           <li><code>CJHighMask.CJHIGH_MASK_ON</code>: mask the CJHIGH fault from asserting</li>
           <li><code>CJHighMask.CJHIGH_MASK_OFF</code>: do not mask the CJHIGH fault from asserting</li>
         </ul>
      </td>
   </tr>
   <tr>
      <td><code>OpenCircuitMode</code></td>
      <td>
        Settings for thermocouple open-circuit fault detection mode. Using a higher impedance mode will increase nominal test time, increasing
        temperature conversion time in turn.
     </td>
      <td>
         <ul>
           <li><code>OpenCircuitMode.DISABLED</code>: disable open circuit testing</li>
           <li><code>OpenCircuitMode.LOW_INPUT_IMPEDANCE</code>: series resistance < 5kΩ </li>
           <li><code>OpenCircuitMode.MED_INPUT_IMPEDANCE</code>: 5kΩ < series resistance < 40kΩ, time constant < 2 ms  </li>
           <li><code>OpenCircuitMode.HIGH_INPUT_IMPEDANCE</code>: 5kΩ < series resistance < 40kΩ, time constant > 2 ms</li>
         </ul>
      </td>
   </tr>
</table>

---
## Temperature Threshold Setting
In order to set temperature fault thresholds using this module, please refer to the table below for accepted temperature values by thermocouple type. Attempting to set a temperature threshold outside of your thermocouple type's range will raise an exception.

<table>
    <thead>
        <tr>
            <th rowspan="3">Thermocouple Type</th>
            <th colspan="4">Temperature Range (°C)</th>
        </tr>
        <tr>
            <th colspan="2">Cold Junction</th>
            <th colspan="2">Thermocouple</th>
        </tr>
        <tr>
            <td>Low</td>
            <td>High</td>
            <td>Low</td>
            <td>High</td>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Type B</td>
            <td>0</td>
            <td>125</td>
            <td>250</td>
            <td>1820</td>
        </tr>
        <tr>
            <td>Type E</td>
            <td>-55</td>
            <td>125</td>
            <td>-200</td>
            <td>1000</td>
        </tr>
        <tr>
            <td>Type J</td>
            <td>-55</td>
            <td>125</td>
            <td>-210</td>
            <td>1200</td>
        </tr>
        <tr>
            <td>Type K</td>
            <td>-55</td>
            <td>125</td>
            <td>-200</td>
            <td>1372</td>
        </tr>
        <tr>
            <td>Type N</td>
            <td>-55</td>
            <td>125</td>
            <td>-200</td>
            <td>1300</td>
        </tr>
        <tr>
            <td>Type R</td>
            <td>-50</td>
            <td>125</td>
            <td>-50</td>
            <td>1768</td>
        </tr>
        <tr>
            <td>Type S</td>
            <td>-50</td>
            <td>125</td>
            <td>-50</td>
            <td>1768</td>
        </tr>
        <tr>
            <td>Type T</td>
            <td>-55</td>
            <td>125</td>
            <td>-200</td>
            <td>400</td>
        </tr>
    </tbody>
</table>
