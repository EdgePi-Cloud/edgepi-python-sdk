"""Hardware dependent integration tests for ADC conversion delay times"""


import logging
import statistics
from time import perf_counter_ns


import pytest
from edgepi.adc.edgepi_adc import EdgePiADC
from edgepi.adc.adc_constants import (
    ADCNum,
    ConvMode,
    ADC1DataRate as DR1,
    ADC2DataRate as DR2,
    FilterMode as FILT,
)
from edgepi.adc.adc_conv_time import expected_continuous_time_delay, expected_initial_time_delay


_logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@pytest.fixture(name="adc", scope="module")
def fixture_adc():
    return EdgePiADC()


# pylint: disable=protected-access, missing-function-docstring


NUM_TRIALS = 10  # number of samples for mean actual conversion time
DELAY_MARGIN = 1  # allows 1 ms error margin between computed and actual conversion time


def _get_data_ready_time(adc):
    times = []
    for _ in range(100):
        start = perf_counter_ns()
        adc._EdgePiADC__is_data_ready()
        end = perf_counter_ns()
        print((end - start) * 10**-6)
        times.append((end - start) * 10**-6)
    return statistics.fmean(times)


def _get_conv_time(adc, adc_num):
    start = perf_counter_ns()
    _logger.info(f"ADCNum: {adc_num.value.id_num}, read_cmd: {adc_num.value.read_cmd}")
    while not adc._EdgePiADC__is_data_ready(adc_num):
        continue
    end = perf_counter_ns()
    return (end - start) * 10**-6


def _get_initial_conv_time(adc, adc_num, conv_mode):
    times = []
    for _ in range(NUM_TRIALS):
        adc._EdgePiADC__send_start_command(adc_num)
        times.append(_get_conv_time(adc, adc_num))
        if conv_mode == ConvMode.CONTINUOUS:
            adc.stop_conversions(adc_num)
    return statistics.fmean(times)


def _get_mean_conv_time_continuous(adc, adc_num):
    adc._EdgePiADC__send_start_command(adc_num)
    times = []
    for _ in range(NUM_TRIALS):
        times.append(_get_conv_time(adc))
    adc.stop_conversions(adc_num)
    # skip first 2 conv times because these are not measured correctly due to
    # new data being available before we start sampling STATUS byte
    return statistics.fmean(times[2:])


@pytest.mark.parametrize(
    "adc_num, conv_mode, data_rate, filter_mode",
    [
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_2P5, FILT.SINC1),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_2P5, FILT.SINC2),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_2P5, FILT.SINC3),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_2P5, FILT.SINC4),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_2P5, FILT.FIR),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_5, FILT.SINC1),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_5, FILT.SINC2),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_5, FILT.SINC3),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_5, FILT.SINC4),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_5, FILT.FIR),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_10, FILT.SINC1),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_10, FILT.SINC2),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_10, FILT.SINC3),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_10, FILT.SINC4),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_10, FILT.FIR),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_16P6, FILT.SINC1),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_16P6, FILT.SINC2),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_16P6, FILT.SINC3),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_16P6, FILT.SINC4),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_16P6, FILT.FIR),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_20, FILT.SINC1),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_20, FILT.SINC2),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_20, FILT.SINC3),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_20, FILT.SINC4),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_20, FILT.FIR),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_50, FILT.SINC1),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_50, FILT.SINC2),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_50, FILT.SINC3),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_50, FILT.SINC4),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_50, FILT.FIR),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_60, FILT.SINC1),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_60, FILT.SINC2),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_60, FILT.SINC3),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_60, FILT.SINC4),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_60, FILT.FIR),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_100, FILT.SINC1),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_100, FILT.SINC2),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_100, FILT.SINC3),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_100, FILT.SINC4),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_100, FILT.FIR),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_400, FILT.SINC1),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_400, FILT.SINC2),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_400, FILT.SINC3),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_400, FILT.SINC4),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_400, FILT.FIR),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_1200, FILT.SINC1),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_1200, FILT.SINC2),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_1200, FILT.SINC3),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_1200, FILT.SINC4),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_1200, FILT.FIR),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_2400, FILT.SINC1),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_2400, FILT.SINC2),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_2400, FILT.SINC3),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_2400, FILT.SINC4),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_2400, FILT.FIR),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_4800, FILT.SINC1),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_4800, FILT.SINC2),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_4800, FILT.SINC3),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_4800, FILT.SINC4),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_4800, FILT.FIR),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_7200, FILT.SINC1),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_7200, FILT.SINC2),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_7200, FILT.SINC3),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_7200, FILT.SINC4),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_7200, FILT.FIR),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_14400, FILT.SINC1),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_14400, FILT.SINC2),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_14400, FILT.SINC3),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_14400, FILT.SINC4),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_14400, FILT.FIR),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_19200, FILT.SINC1),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_19200, FILT.SINC2),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_19200, FILT.SINC3),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_19200, FILT.SINC4),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_19200, FILT.FIR),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_38400, FILT.SINC1),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_38400, FILT.SINC2),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_38400, FILT.SINC3),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_38400, FILT.SINC4),
        (ADCNum.ADC_1, ConvMode.PULSE, DR1.SPS_38400, FILT.FIR),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_2P5, FILT.SINC1),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_2P5, FILT.SINC2),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_2P5, FILT.SINC3),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_2P5, FILT.SINC4),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_2P5, FILT.FIR),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_5, FILT.SINC1),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_5, FILT.SINC2),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_5, FILT.SINC3),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_5, FILT.SINC4),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_5, FILT.FIR),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_10, FILT.SINC1),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_10, FILT.SINC2),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_10, FILT.SINC3),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_10, FILT.SINC4),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_10, FILT.FIR),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_16P6, FILT.SINC1),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_16P6, FILT.SINC2),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_16P6, FILT.SINC3),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_16P6, FILT.SINC4),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_16P6, FILT.FIR),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_20, FILT.SINC1),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_20, FILT.SINC2),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_20, FILT.SINC3),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_20, FILT.SINC4),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_20, FILT.FIR),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_50, FILT.SINC1),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_50, FILT.SINC2),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_50, FILT.SINC3),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_50, FILT.SINC4),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_50, FILT.FIR),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_60, FILT.SINC1),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_60, FILT.SINC2),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_60, FILT.SINC3),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_60, FILT.SINC4),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_60, FILT.FIR),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_100, FILT.SINC1),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_100, FILT.SINC2),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_100, FILT.SINC3),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_100, FILT.SINC4),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_100, FILT.FIR),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_400, FILT.SINC1),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_400, FILT.SINC2),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_400, FILT.SINC3),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_400, FILT.SINC4),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_400, FILT.FIR),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_1200, FILT.SINC1),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_1200, FILT.SINC2),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_1200, FILT.SINC3),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_1200, FILT.SINC4),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_1200, FILT.FIR),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_2400, FILT.SINC1),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_2400, FILT.SINC2),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_2400, FILT.SINC3),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_2400, FILT.SINC4),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_2400, FILT.FIR),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_4800, FILT.SINC1),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_4800, FILT.SINC2),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_4800, FILT.SINC3),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_4800, FILT.SINC4),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_4800, FILT.FIR),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_7200, FILT.SINC1),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_7200, FILT.SINC2),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_7200, FILT.SINC3),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_7200, FILT.SINC4),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_7200, FILT.FIR),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_14400, FILT.SINC1),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_14400, FILT.SINC2),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_14400, FILT.SINC3),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_14400, FILT.SINC4),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_14400, FILT.FIR),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_19200, FILT.SINC1),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_19200, FILT.SINC2),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_19200, FILT.SINC3),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_19200, FILT.SINC4),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_19200, FILT.FIR),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_38400, FILT.SINC1),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_38400, FILT.SINC2),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_38400, FILT.SINC3),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_38400, FILT.SINC4),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_38400, FILT.FIR),
        # pulse conversion
        (ADCNum.ADC_2, ConvMode.PULSE, DR2.SPS_10, FILT.SINC1),
        (ADCNum.ADC_2, ConvMode.PULSE, DR2.SPS_10, FILT.SINC2),
        (ADCNum.ADC_2, ConvMode.PULSE, DR2.SPS_10, FILT.SINC3),
        (ADCNum.ADC_2, ConvMode.PULSE, DR2.SPS_10, FILT.SINC4),
        (ADCNum.ADC_2, ConvMode.PULSE, DR2.SPS_10, FILT.FIR),
        (ADCNum.ADC_2, ConvMode.PULSE, DR2.SPS_100, FILT.SINC1),
        (ADCNum.ADC_2, ConvMode.PULSE, DR2.SPS_100, FILT.SINC2),
        (ADCNum.ADC_2, ConvMode.PULSE, DR2.SPS_100, FILT.SINC3),
        (ADCNum.ADC_2, ConvMode.PULSE, DR2.SPS_100, FILT.SINC4),
        (ADCNum.ADC_2, ConvMode.PULSE, DR2.SPS_100, FILT.FIR),
        (ADCNum.ADC_2, ConvMode.PULSE, DR2.SPS_400, FILT.SINC1),
        (ADCNum.ADC_2, ConvMode.PULSE, DR2.SPS_400, FILT.SINC2),
        (ADCNum.ADC_2, ConvMode.PULSE, DR2.SPS_400, FILT.SINC3),
        (ADCNum.ADC_2, ConvMode.PULSE, DR2.SPS_400, FILT.SINC4),
        (ADCNum.ADC_2, ConvMode.PULSE, DR2.SPS_400, FILT.FIR),
        (ADCNum.ADC_2, ConvMode.PULSE, DR2.SPS_800, FILT.SINC1),
        (ADCNum.ADC_2, ConvMode.PULSE, DR2.SPS_800, FILT.SINC2),
        (ADCNum.ADC_2, ConvMode.PULSE, DR2.SPS_800, FILT.SINC3),
        (ADCNum.ADC_2, ConvMode.PULSE, DR2.SPS_800, FILT.SINC4),
        (ADCNum.ADC_2, ConvMode.PULSE, DR2.SPS_800, FILT.FIR),
        # continuous conversion
        (ADCNum.ADC_2, ConvMode.CONTINUOUS, DR2.SPS_10, FILT.SINC1),
        (ADCNum.ADC_2, ConvMode.CONTINUOUS, DR2.SPS_10, FILT.SINC2),
        (ADCNum.ADC_2, ConvMode.CONTINUOUS, DR2.SPS_10, FILT.SINC3),
        (ADCNum.ADC_2, ConvMode.CONTINUOUS, DR2.SPS_10, FILT.SINC4),
        (ADCNum.ADC_2, ConvMode.CONTINUOUS, DR2.SPS_10, FILT.FIR),
        (ADCNum.ADC_2, ConvMode.CONTINUOUS, DR2.SPS_100, FILT.SINC1),
        (ADCNum.ADC_2, ConvMode.CONTINUOUS, DR2.SPS_100, FILT.SINC2),
        (ADCNum.ADC_2, ConvMode.CONTINUOUS, DR2.SPS_100, FILT.SINC3),
        (ADCNum.ADC_2, ConvMode.CONTINUOUS, DR2.SPS_100, FILT.SINC4),
        (ADCNum.ADC_2, ConvMode.CONTINUOUS, DR2.SPS_100, FILT.FIR),
        (ADCNum.ADC_2, ConvMode.CONTINUOUS, DR2.SPS_400, FILT.SINC1),
        (ADCNum.ADC_2, ConvMode.CONTINUOUS, DR2.SPS_400, FILT.SINC2),
        (ADCNum.ADC_2, ConvMode.CONTINUOUS, DR2.SPS_400, FILT.SINC3),
        (ADCNum.ADC_2, ConvMode.CONTINUOUS, DR2.SPS_400, FILT.SINC4),
        (ADCNum.ADC_2, ConvMode.CONTINUOUS, DR2.SPS_400, FILT.FIR),
        (ADCNum.ADC_2, ConvMode.CONTINUOUS, DR2.SPS_800, FILT.SINC1),
        (ADCNum.ADC_2, ConvMode.CONTINUOUS, DR2.SPS_800, FILT.SINC2),
        (ADCNum.ADC_2, ConvMode.CONTINUOUS, DR2.SPS_800, FILT.SINC3),
        (ADCNum.ADC_2, ConvMode.CONTINUOUS, DR2.SPS_800, FILT.SINC4),
        (ADCNum.ADC_2, ConvMode.CONTINUOUS, DR2.SPS_800, FILT.FIR),
    ],
)
def test_expected_initial_time_delay(adc_num, conv_mode, data_rate, filter_mode, adc):
    # configure ADC with new filter and data rate modes
    adc.reset()
    if adc_num == ADCNum.ADC_1:
        adc._EdgePiADC__config(
            conversion_mode=conv_mode, adc_1_data_rate=data_rate, filter_mode=filter_mode
        )
    else:
        adc._EdgePiADC__config(
            conversion_mode=conv_mode, adc_2_data_rate=data_rate, filter_mode=filter_mode
        )
    _logger.info(
        (
            "\n----------------------------------------------------------------"
            f"Testing with configs: adc_num={adc_num}, conv_mode={conv_mode} "
            f"data_rate={data_rate}, filter={filter_mode}"
            "----------------------------------------------------------------"
        )
    )

    # get computed time delay
    expected = expected_initial_time_delay(
        adc_num, data_rate.value.op_code, filter_mode.value.op_code
    )
    _logger.info(f"Computed Conversion Time (ms): {expected}")

    # get actual time delay (time until STATUS byte shows new data)
    mean_time = _get_initial_conv_time(adc, adc_num, conv_mode)
    _logger.info(f"Mean Conversion Time (ms): {mean_time}")

    # assert computed time delay is within allowed margin of mean actual delay
    # cannot use % difference because higher data rate delay times are in fractions of a ms
    # where SPI transfer and function overhead times are a significant factor,
    # resulting in inaccurate sampling of mean actual conversion time.
    # i.e. 50% of mean conversion time may actually be unrelated overhead from sampling STATUS byte
    # to check if data is new, or other function overhead.
    diff = abs(expected - mean_time)
    _logger.info(f"Computed vs Actual Time Delay Difference = {diff} ms")
    assert diff < DELAY_MARGIN


@pytest.mark.parametrize(
    "adc_num, conv_mode, data_rate, filter_mode",
    [
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_2P5, FILT.SINC1),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_2P5, FILT.SINC2),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_2P5, FILT.SINC3),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_2P5, FILT.SINC4),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_2P5, FILT.FIR),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_5, FILT.SINC1),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_5, FILT.SINC2),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_5, FILT.SINC3),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_5, FILT.SINC4),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_5, FILT.FIR),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_10, FILT.SINC1),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_10, FILT.SINC2),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_10, FILT.SINC3),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_10, FILT.SINC4),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_10, FILT.FIR),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_16P6, FILT.SINC1),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_16P6, FILT.SINC2),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_16P6, FILT.SINC3),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_16P6, FILT.SINC4),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_16P6, FILT.FIR),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_20, FILT.SINC1),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_20, FILT.SINC2),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_20, FILT.SINC3),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_20, FILT.SINC4),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_20, FILT.FIR),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_50, FILT.SINC1),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_50, FILT.SINC2),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_50, FILT.SINC3),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_50, FILT.SINC4),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_50, FILT.FIR),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_60, FILT.SINC1),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_60, FILT.SINC2),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_60, FILT.SINC3),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_60, FILT.SINC4),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_60, FILT.FIR),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_100, FILT.SINC1),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_100, FILT.SINC2),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_100, FILT.SINC3),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_100, FILT.SINC4),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_100, FILT.FIR),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_400, FILT.SINC1),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_400, FILT.SINC2),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_400, FILT.SINC3),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_400, FILT.SINC4),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_400, FILT.FIR),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_1200, FILT.SINC1),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_1200, FILT.SINC2),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_1200, FILT.SINC3),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_1200, FILT.SINC4),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_1200, FILT.FIR),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_2400, FILT.SINC1),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_2400, FILT.SINC2),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_2400, FILT.SINC3),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_2400, FILT.SINC4),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_2400, FILT.FIR),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_4800, FILT.SINC1),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_4800, FILT.SINC2),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_4800, FILT.SINC3),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_4800, FILT.SINC4),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_4800, FILT.FIR),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_7200, FILT.SINC1),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_7200, FILT.SINC2),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_7200, FILT.SINC3),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_7200, FILT.SINC4),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_7200, FILT.FIR),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_14400, FILT.SINC1),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_14400, FILT.SINC2),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_14400, FILT.SINC3),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_14400, FILT.SINC4),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_14400, FILT.FIR),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_19200, FILT.SINC1),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_19200, FILT.SINC2),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_19200, FILT.SINC3),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_19200, FILT.SINC4),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_19200, FILT.FIR),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_38400, FILT.SINC1),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_38400, FILT.SINC2),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_38400, FILT.SINC3),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_38400, FILT.SINC4),
        (ADCNum.ADC_1, ConvMode.CONTINUOUS, DR1.SPS_38400, FILT.FIR),
        (ADCNum.ADC_2, ConvMode.CONTINUOUS, DR2.SPS_10, FILT.SINC1),
        (ADCNum.ADC_2, ConvMode.CONTINUOUS, DR2.SPS_10, FILT.SINC2),
        (ADCNum.ADC_2, ConvMode.CONTINUOUS, DR2.SPS_10, FILT.SINC3),
        (ADCNum.ADC_2, ConvMode.CONTINUOUS, DR2.SPS_10, FILT.SINC4),
        (ADCNum.ADC_2, ConvMode.CONTINUOUS, DR2.SPS_10, FILT.FIR),
        (ADCNum.ADC_2, ConvMode.CONTINUOUS, DR2.SPS_100, FILT.SINC1),
        (ADCNum.ADC_2, ConvMode.CONTINUOUS, DR2.SPS_100, FILT.SINC2),
        (ADCNum.ADC_2, ConvMode.CONTINUOUS, DR2.SPS_100, FILT.SINC3),
        (ADCNum.ADC_2, ConvMode.CONTINUOUS, DR2.SPS_100, FILT.SINC4),
        (ADCNum.ADC_2, ConvMode.CONTINUOUS, DR2.SPS_100, FILT.FIR),
        (ADCNum.ADC_2, ConvMode.CONTINUOUS, DR2.SPS_400, FILT.SINC1),
        (ADCNum.ADC_2, ConvMode.CONTINUOUS, DR2.SPS_400, FILT.SINC2),
        (ADCNum.ADC_2, ConvMode.CONTINUOUS, DR2.SPS_400, FILT.SINC3),
        (ADCNum.ADC_2, ConvMode.CONTINUOUS, DR2.SPS_400, FILT.SINC4),
        (ADCNum.ADC_2, ConvMode.CONTINUOUS, DR2.SPS_400, FILT.FIR),
        (ADCNum.ADC_2, ConvMode.CONTINUOUS, DR2.SPS_800, FILT.SINC1),
        (ADCNum.ADC_2, ConvMode.CONTINUOUS, DR2.SPS_800, FILT.SINC2),
        (ADCNum.ADC_2, ConvMode.CONTINUOUS, DR2.SPS_800, FILT.SINC3),
        (ADCNum.ADC_2, ConvMode.CONTINUOUS, DR2.SPS_800, FILT.SINC4),
        (ADCNum.ADC_2, ConvMode.CONTINUOUS, DR2.SPS_800, FILT.FIR),
    ],
)
def test_expected_continuous_time_delay(adc_num, conv_mode, data_rate, filter_mode, adc):
    # configure ADC with new filter and data rate modes
    if adc_num == ADCNum.ADC_1:
        adc._EdgePiADC__config(
            conversion_mode=conv_mode, adc_1_data_rate=data_rate, filter_mode=filter_mode
        )
    else:
        adc._EdgePiADC__config(
            conversion_mode=conv_mode, adc_2_data_rate=data_rate, filter_mode=filter_mode
        )
    _logger.info(
        (
            "\n----------------------------------------------------------------"
            f"Testing with configs: adc_num={adc_num}, conv_mode={conv_mode} "
            f"data_rate={data_rate}, filter={filter_mode}"
            "----------------------------------------------------------------"
        )
    )

    # get computed time delay
    expected = expected_continuous_time_delay(adc_num, data_rate.value.op_code)
    _logger.info(f"Computed Conversion Time (ms): {expected}")

    # get actual time delay (time until STATUS byte shows new data)
    mean_time = _get_mean_conv_time_continuous(adc, adc_num)
    _logger.info(f"Mean Conversion Time (ms): {mean_time}")

    # assert computed time delay is within allowed margin of mean actual delay
    diff = abs(expected - mean_time)
    _logger.info(f"Computed vs Actual Time Delay Difference = {diff} ms")
    assert diff < DELAY_MARGIN
