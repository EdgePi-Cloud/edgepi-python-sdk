# EdgePi ADC Module User Guide
___
## Quick Use Example
This section will demonstrate how to import the EdgePi ADC module, and use it to measure a voltage value from an analog input pin.
Note, the EdgePi ADC can be used with two different sampling modes: pulse conversion mode, and continuous conversion mode.

### Reading Voltage from Analog Input Pin: Pulse Conversion Mode
In pulse conversion mode, a sampling event must be manually triggered. This can be achieved as follows.
```
from edgepi.dac.edgepi_adc import EdgePiADC
from edgepi.adc.adc_constants import ADCChannel, ConvMode

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
sampling data must also be manually by the user.
```
from edgepi.dac.edgepi_adc import EdgePiADC
from edgepi.adc.adc_constants import ADCChannel, ConvMode

# initialize ADC
edgepi_adc = EdgePiADC()

# configure ADC to sample input pin 4 (the input pins are 0-indexed)
edgepi_adc.set_config(adc_1_analog_in=ADCChannel.AIN3, conversion_mode=ConvMode.CONTINUOUS)

# send command to start automatic conversions
edgepi_adc.start_conversions()

# perform 10 voltage reads
for _ in range(10):
  out = edgepi_adc.read_voltage()
  print(out)
  
# stop automatic conversions
edgepi_adc.stop_conversions()
```
