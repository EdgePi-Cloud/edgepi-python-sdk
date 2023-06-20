from edgepi.adc.edgepi_adc import EdgePiADC
from edgepi.adc.adc_constants import AnalogIn, ConvMode, ADCNum, ADC1DataRate, DiffMode
import logging

_logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':
  # initialize ADC
  edgepi_adc = EdgePiADC()
  
  # configure ADC to sample A-IN 1 (Refer to the EdgePi label for details)
  edgepi_adc.set_config(adc_1_analog_in=AnalogIn.AIN1, conversion_mode=ConvMode.CONTINUOUS, adc_1_data_rate=ADC1DataRate.SPS_38400)
  
  edgepi_adc.start_conversions(ADCNum.ADC_1)
  
  # perform 10 voltage reads
  for _ in range(10):
    out = edgepi_adc.read_voltage(ADCNum.ADC_1)
    print(out)
  
  edgepi_adc.stop_conversions(ADCNum.ADC_1)