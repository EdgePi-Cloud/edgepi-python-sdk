"""Hardware dependent integration tests for ADC conversion delay times"""


import logging
import statistics
from time import perf_counter_ns


import pytest
from edgepi.adc.edgepi_adc import EdgePiADC
from edgepi.adc.adc_constants import ADCNum, ConvMode, ADC1DataRate as DR1, FilterMode as FILT
from edgepi.adc.adc_conv_time import (
    compute_continuous_time_delay,
    compute_initial_time_delay,
    SAFETY_MARGIN,
)


_logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@pytest.fixture(name="adc", scope="module")
def fixture_adc():
    return EdgePiADC()


# pylint: disable=protected-access, missing-function-docstring


NUM_TRIALS = 10  # number of samples for mean actual conversion time
DELAY_MARGIN = 0.01  # allow 1% margin between computed and actual delay


def _get_conv_time(adc):
    start = perf_counter_ns()
    # adc.start_conversions()
    while not adc._EdgePiADC__is_data_ready():
        continue
    end = perf_counter_ns()
    return (end - start) * 10**-6


def _get_initial_conv_time(adc, adc_num, **kwargs):
    adc._EdgePiADC__send_start_command(adc_num)
    conv_time = _get_conv_time(adc)
    conv_mode = kwargs["conv_mode"]
    if conv_mode == ConvMode.CONTINUOUS:
        adc.stop_conversions()
    return conv_time


def _get_mean_delay(adc, adc_num, conv_time_function, **kwargs):
    times = []
    for _ in range(NUM_TRIALS):
        times.append(conv_time_function(adc, adc_num, **kwargs))
    return statistics.mean(times)


@pytest.mark.parametrize(
    "adc_num, conv_mode, data_rate, filter_mode",
    [
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_2P5, FILT.SINC1),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_2P5, FILT.SINC2),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_2P5, FILT.SINC3),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_2P5, FILT.SINC4),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_2P5, FILT.FIR),
    ],
)
def test_compute_initial_time_delay(adc_num, conv_mode, data_rate, filter_mode, adc):
    # configure ADC with new filter and data rate modes
    adc.set_config(conversion_mode=conv_mode, adc_1_data_rate=data_rate, filter_mode=filter_mode)
    _logger.info(
        (
            "\n----------------------------------------------------------------"
            f"Testing with configs: adc_num={adc_num}, conv_mode={conv_mode} "
            f"data_rate={data_rate}, filter={filter_mode}"
            "----------------------------------------------------------------"
        )
    )

    # get computed time delay
    expected = compute_initial_time_delay(
        ADCNum.ADC_1, data_rate.value.op_code, filter_mode.value.op_code
    )
    _logger.info(f"Computed Conversion Time (ms): {expected}")

    # get actual time delay (time until STATUS byte shows new data)
    mean_time = _get_mean_delay(adc, adc_num, _get_initial_conv_time, conv_mode=conv_mode)
    _logger.info(f"Mean Conversion Time (ms): {mean_time}")

    # assert computed time delay is within allowed margin of mean actual delay
    _logger.info(
        (
            f"Computed vs Actual Time Delay Difference = "
            f"{(abs(expected - mean_time) / mean_time) * 100} %"
        )
    )
    assert abs(expected - mean_time) / mean_time < DELAY_MARGIN
