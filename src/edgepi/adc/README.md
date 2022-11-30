# EdgePi ADC Module User Guide
___
## Quick Use Example
This section will demonstrate how to import the EdgePi ADC module, and use it to measure a voltage value from an analog input pin.
Note, the EdgePi ADC can be used with two different sampling modes: pulse conversion mode, and continuous conversion mode.
The EdgePi ADC contains two internal ADC's; for simplicity, the two examples below only show the use of ADC_1.

### Reading Voltage from Analog Input Pin: Pulse Conversion Mode
In pulse conversion mode, a sampling event must be manually triggered. This can be achieved as follows. Only ADC_1
is able to perform pulse conversions, so the ADC number does not need to be passed as an argument here.
```
from edgepi.dac.edgepi_adc import EdgePiADC
from edgepi.adc.adc_constants import ADCChannel, ConvMode, ADCNum

# initialize ADC
edgepi_adc = EdgePiADC()

# configure ADC to sample input pin 4 (the input pins are 0-indexed)
edgepi_adc.set_config(adc_1_analog_in=ADCChannel.AIN3, conversion_mode=ConvMode.PULSE)

# trigger sampling event
out = edgepi_adc.single_sample()
print(out)
```

### Reading Voltage from Analog Input Pin: Continuous Conversion Mode
In continuous conversion mode, sampling events occur automatically. However, after configuring the ADC
to perform continuous conversion, the user must send a command to start the conversions, and
sampling data must also be manually retrieved by the user. Note the use of `ADCNum` to specify the ADC number.
```
from edgepi.dac.edgepi_adc import EdgePiADC
from edgepi.adc.adc_constants import ADCChannel, ConvMode, ADCNum

# initialize ADC
edgepi_adc = EdgePiADC()

# configure ADC to sample input pin 4 (the input pins are 0-indexed)
edgepi_adc.set_config(adc_1_analog_in=ADCChannel.AIN3, conversion_mode=ConvMode.CONTINUOUS)

# send command to start automatic conversions
edgepi_adc.start_conversions(ADCNum.ADC_1)

# perform 10 voltage reads
for _ in range(10):
  out = edgepi_adc.read_voltage()
  print(out)
  
# stop automatic conversions
edgepi_adc.stop_conversions(ADCNum.ADC_1)
```
___
## Using ADC Module
This section introduces ADC functionality available to users.

1. Reading Voltage from Analog Input Pins - Individual Channel
    - Read voltage from any of the EdgePi's analog input pins.
2. Reading Voltage from Analog Input Pins - Differentials
    - Read differential voltage between analog input pin pairs.
3. Reading RTD
    - Set ADC to RTD mode to perform RTD readings
4. Configuring ADC Settings
    - Before performing voltage reads, there are certain settings users must configure:
        * input voltage pin to measure via ADC1
        * voltage reading conversion mode (continuous mode by default)
    - There are also other settings users may be interested in configuring:
        * ADC filter mode
        * ADC sampling data rate (samples per second)
5. Read ADC Alarms
    - When voltage reads are triggered, the ADC passes along information about the status of several possible faults.
---
## Reading Single Channel Voltage
In order to read voltage from a single input channel, the following parameters need to be provided:
1. Conversion Mode
    * ADC1 features two conversion modes. By default it will operate in continuous conversion mode, but can also be configured to use pulse conversions.
3. ADC Number
    * When using continuous conversion mode, the ADC number must be provided to identify which ADC to start and read conversions for.
4. Input Channel
    * Select one of eight input channels to read voltage from.

### Single Channel - Pulse Mode
```
edgepi_adc = EdgePiADC()

# configure ADC to sample input pin 4 (the input pins are 0-indexed)
edgepi_adc.set_config(adc_1_analog_in=ADCChannel.AIN3, conversion_mode=ConvMode.PULSE)

# trigger sampling event
out = edgepi_adc.single_sample()
```

### Single Channel - Continuous Mode: ADC1
```
edgepi_adc = EdgePiADC()

# configure ADC to sample input pin 4 (the input pins are 0-indexed)
edgepi_adc.set_config(adc_1_analog_in=ADCChannel.AIN3, conversion_mode=ConvMode.CONTINUOUS)

# trigger sampling events
edgepi_adc.start_conversions(ADCNum.ADC_1)
out = edgepi_adc.read_voltage(ADCNum.ADC_1)
```

### Single Channel - Continuous Mode: ADC2
```
edgepi_adc = EdgePiADC()

# configure ADC to sample input pin 4 (the input pins are 0-indexed)
# conversion mode doesn't need to be specified for ADC2, as it can only operate in continuous conversion mode
edgepi_adc.set_config(adc_2_analog_in=ADCChannel.AIN3)

# trigger sampling events
edgepi_adc.start_conversions(ADCNum.ADC_2)
out = edgepi_adc.read_voltage(ADCNum.ADC_2)
```
---
## Reading Differential Voltage
In order to read differential voltage, the following parameters need to be provided:
1. ADC Number
    * Either ADC may be used for differential voltage reading.
3. Differential Pair
   * It is only possible to use predefined pairs of channels for differential voltage reading. These are available via the `DiffMode` enum.

### Differential Voltage Reading (with Continuous Voltage Reading)
```
edgepi_adc = EdgePiADC()

# configure ADC to read Differential Pair 1 (AIN0, AIN1)
edgepi_adc.select_differential(ADCNum.ADC_1, DiffMode.DIFF_1)

# trigger sampling events
edgepi_adc.start_conversions(ADCNum.ADC_1)
out = edgepi_adc.read_voltage(ADCNum.ADC_1)
```
