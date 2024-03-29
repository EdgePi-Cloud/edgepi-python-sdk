# EdgePi ADC Module User Guide
___
## Quick Use Example
This section will demonstrate how to import the EdgePi ADC module, and use it to measure a voltage value from an analog input pin.
Note, the EdgePi ADC can be used with two different sampling modes: pulse conversion mode, and continuous conversion mode.

### Reading Voltage from Analog Input Pin: Pulse Conversion Mode
In pulse conversion mode, a sampling event must be manually triggered. This can be achieved as follows.
```python
from edgepi.adc.edgepi_adc import EdgePiADC
from edgepi.adc.adc_constants import AnalogIn, ConvMode, ADC1DataRate

# initialize ADC
edgepi_adc = EdgePiADC()

# configure ADC to sample A-IN 1 (Refer to the EdgePi label for details)
edgepi_adc.set_config(adc_1_analog_in=AnalogIn.AIN1, conversion_mode=ConvMode.PULSE, adc_1_data_rate=ADC1DataRate.SPS_38400)

# trigger sampling event
out = edgepi_adc.single_sample()
print(out)
```

### Reading Voltage from Analog Input Pin: Continuous Conversion Mode
In continuous conversion mode, sampling events occur automatically. However, after configuring the ADC
to perform continuous conversion, the user must send a command to start the conversions, and
sampling data must also be manually by the user.
```python
from edgepi.adc.edgepi_adc import EdgePiADC
from edgepi.adc.adc_constants import AnalogIn, ConvMode, ADCNum, ADC1DataRate

# initialize ADC
edgepi_adc = EdgePiADC()

# configure ADC to sample A-IN 1 (Refer to the EdgePi label for details)
edgepi_adc.set_config(adc_1_analog_in=AnalogIn.AIN1, conversion_mode=ConvMode.CONTINUOUS, adc_1_data_rate=ADC1DataRate.SPS_38400)

# send command to start automatic conversions
edgepi_adc.start_conversions(ADCNum.ADC_1)

# perform 10 voltage reads
for _ in range(10):
  out = edgepi_adc.read_voltage(ADCNum.ADC_1)
  print(out)
  
# stop automatic conversions
edgepi_adc.stop_conversions(ADCNum.ADC_1)
```
### Reading Voltage from Analog Input Pin: Continuous Conversion Mode and Differential
```python
from edgepi.adc.edgepi_adc import EdgePiADC
from edgepi.adc.adc_constants import AnalogIn, ConvMode, ADCNum, ADC1DataRate, DiffMode

# initialize ADC
edgepi_adc = EdgePiADC()

# configure ADC to sample A-IN 1 (Refer to the EdgePi label for details)
edgepi_adc.set_config(adc_1_analog_in=AnalogIn.AIN1, conversion_mode=ConvMode.CONTINUOUS, adc_1_data_rate=ADC1DataRate.SPS_38400)
# Configure inputs to differential between A/DIN5 and A/DIN6
edgepi_adc.select_differential(ADCNum.ADC_1,DiffMode.DIFF_3)

# send command to start automatic conversions
edgepi_adc.start_conversions(ADCNum.ADC_1)

# perform 10 voltage reads
for _ in range(10):
  out = edgepi_adc.read_voltage(ADCNum.ADC_1)
  print(out)
  
# stop automatic conversions
edgepi_adc.stop_conversions(ADCNum.ADC_1)
```
___

### Reading RTD Measurements: Pulse Conversion Mode
Input 4-8 can be configured to read three-leaded RTD sensor.
```python
from edgepi.adc.edgepi_adc import EdgePiADC
from edgepi.adc.adc_constants import AnalogIn, ConvMode, ADCNum

# initialize ADC
edgepi_adc = EdgePiADC()

edgepi_adc.set_config(conversion_mode=ConvMode.PULSE)
# Both ADC_1 and ADC_2 are available but only one of them is used at a time. It uses ADC_2 by default
edgepi_adc.set_rtd(True, ADCNum.ADC_2)

# trigger sampling event
edgepi_adc.single_sample_rtd()

# Disable RTD
edgepi_adc.set_rtd(False, ADCNum.ADC_2)

```
### Reading RTD Measurements: Continuous Conversion Mode
Input 4-8 can be configured to read three-leaded RTD sensor.
```python
from edgepi.adc.edgepi_adc import EdgePiADC
from edgepi.adc.adc_constants import AnalogIn, ConvMode, ADCNum

# initialize ADC
edgepi_adc = EdgePiADC()

edgepi_adc.set_config(conversion_mode=ConvMode.CONTINUOUS)
# Both ADC_1 and ADC_2 are available but only one of them is used at a time
edgepi_adc.set_rtd(True, ADCNum.ADC_2)

# send command to start automatic conversions
edgepi_adc.start_conversions(ADCNum.ADC_2)

# perform 10 voltage reads
for _ in range(10):
  out = edgepi_adc.read_rtd_temperature()
  print(out)
  
# stop automatic conversions
edgepi_adc.stop_conversions(ADCNum.ADC_2)
# Disable RTD
edgepi_adc.set_rtd(False, ADCNum.ADC_2)

```
___

## Using ADC Module
This section introduces ADC functionality available to users.

1. Reading Voltage from Analog Input Pins
    - The main functionality offered by the ADC, voltages can be read from any of the EdgePi's analog input pins.
2. Configuring ADC Settings
    - Before performing voltage reads, there are certain settings users must configure:
        * input voltage pin to measure via ADC1
        * voltage reading conversion mode (continuous mode by default)
    - There are also other settings users may be interested in configuring:
        * ADC filter mode
        * ADC sampling data rate (samples per second)
3. Read ADC Alarms
    - When voltage reads are triggered, the ADC passes along information about the status of several possible faults.
