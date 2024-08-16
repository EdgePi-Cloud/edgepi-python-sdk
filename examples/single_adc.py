"""Example reading from individual ADC pins"""

import time

from edgepi.adc.edgepi_adc import EdgePiADC
from edgepi.adc.adc_constants import AnalogIn, ADC1DataRate, ConvMode

ITER = 50

def run_test():
    """
    This test performs 400 analog input reads, with a total of 50 per ADC pin.
    """
    edgepi_adc = EdgePiADC(enable_cache=False)

    start = time.time()
    result_list = []
    adc_choices = [
        AnalogIn.AIN1, AnalogIn.AIN2, AnalogIn.AIN3, AnalogIn.AIN4,
        AnalogIn.AIN5, AnalogIn.AIN6, AnalogIn.AIN7, AnalogIn.AIN8,
    ]

    for _ in range(ITER):
        tmp_list = []
        for ain in adc_choices:
            edgepi_adc.set_config(
                adc_1_analog_in=ain,
                conversion_mode=ConvMode.PULSE,
                adc_1_data_rate=ADC1DataRate.SPS_38400
            )

            voltage = edgepi_adc.single_sample()
            tmp_list += [voltage]

        result_list += [tmp_list]

    elapsed = time.time() - start

    print(result_list[24])
    print(f"Time elapsed {elapsed/ITER:.6f} s")
    print(f"Frequency {ITER/elapsed:.4f} hz")

if __name__ == "__main__":
    run_test()
