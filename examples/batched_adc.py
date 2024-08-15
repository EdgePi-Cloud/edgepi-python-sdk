import time

from edgepi.adc.edgepi_adc import EdgePiADC
from edgepi.adc.adc_constants import AnalogIn, ConvMode, ADCNum, ADC1DataRate, DiffMode

from edgepi.dac.edgepi_dac import EdgePiDAC
from edgepi.dac.dac_constants import DACChannel as Ch

ITER = 50

def run_test():
    edgepi_adc = EdgePiADC(enable_cache=False)

    start = time.time()
    result_list = []
    adc_choices = [
        AnalogIn.AIN1, AnalogIn.AIN2, AnalogIn.AIN3, AnalogIn.AIN4,
        AnalogIn.AIN5, AnalogIn.AIN6, AnalogIn.AIN7, AnalogIn.AIN8,
    ]

    for _ in range(ITER):
        tmp = edgepi_adc.batch_config_and_read_samples_adc1(
            data_rate=ADC1DataRate.SPS_38400,
            analog_in_list=adc_choices,
        )
        result_list += [tmp]

    elapsed = time.time() - start

    print(result_list[24])
    print(f"Time elapsed {elapsed/ITER:.6f} s")
    print(f"Frequency {ITER/elapsed:.4f} hz")

if __name__ == "__main__":
    run_test()