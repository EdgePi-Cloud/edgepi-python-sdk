"""Example reading from from individual ADC pins"""

import time

from edgepi.adc.edgepi_adc import EdgePiADC
from edgepi.adc.adc_constants import AnalogIn, ADC1DataRate, DiffMode

ITER = 50

def run_test():
    """
    This test performs 300 analog input reads, with 50 for each of 4 analog pins, and
    50 for each of 2 differential analog pairs.
    """
    
    edgepi_adc = EdgePiADC(enable_cache=False)

    start = time.time()
    result_list = []
    adc_choices = [
        AnalogIn.AIN1, AnalogIn.AIN2,
        AnalogIn.AIN5, AnalogIn.AIN6,
    ]
    differential_pairs = [
        DiffMode.DIFF_2,
        DiffMode.DIFF_4,
    ]

    for _ in range(ITER):
        tmp = edgepi_adc.read_samples_adc1_batch(
            ADC1DataRate.SPS_38400,
            adc_choices,
            differential_pairs,
        )
        result_list += [tmp]

    elapsed = time.time() - start

    print(result_list[24])
    print(f"Time elapsed {elapsed/ITER:.6f} s")
    print(f"Frequency {ITER/elapsed:.4f} hz")

if __name__ == "__main__":
    run_test()
