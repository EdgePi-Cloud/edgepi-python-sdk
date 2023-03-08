"""Hardware tests for EdgePi differential voltage reading/writing accuracy using DAC and ADC"""

import logging

from time import sleep
import pytest
from edgepi.adc.edgepi_adc import EdgePiADC
from edgepi.adc.adc_constants import ADCChannel, ADCNum, DiffMode
from edgepi.dac.edgepi_dac import EdgePiDAC
from edgepi.dac.dac_constants import DACChannel

_logger = logging.getLogger(__name__)


NUM_CHANNELS = 1
READS_PER_WRITE = 1
RW_ERROR = 2e-3 # TODO: change to mV
MAX_VOLTAGE = 5.0
VOLTAGE_STEP = 0.5
WRITE_READ_DELAY = 0.1

_ch_map = {
    0: (ADCChannel.AIN0, DACChannel.AOUT0),
    1: (ADCChannel.AIN1, DACChannel.AOUT1),
    2: (ADCChannel.AIN2, DACChannel.AOUT2),
    3: (ADCChannel.AIN3, DACChannel.AOUT3),
    4: (ADCChannel.AIN4, DACChannel.AOUT4),
    5: (ADCChannel.AIN5, DACChannel.AOUT5),
    6: (ADCChannel.AIN6, DACChannel.AOUT6),
    7: (ADCChannel.AIN7, DACChannel.AOUT7),
}

# Sending start and stop conversion command for each ADC
@pytest.fixture(name="adc_1", scope="module")
def fixture_adc_1():
    adc = EdgePiADC()
    adc.start_conversions(ADCNum.ADC_1)
    yield adc
    adc.stop_conversions(ADCNum.ADC_1)


@pytest.fixture(name="adc_2", scope="module")
def fixture_adc_2():
    adc = EdgePiADC()
    adc.start_conversions(ADCNum.ADC_2)
    yield adc
    adc.stop_conversions(ADCNum.ADC_2)

# DAC Instantiation
@pytest.fixture(name="dac", scope="module")
def fixture_dac():
    return EdgePiDAC()

# custom assert for error window
def _assert_approx(a: float, b: float, error: float):
    """assert `b` is within +/- `error` of `a`"""
    # pylint: disable=invalid-name
    assert (a - error) <= b <= (a + error)

def _measure_voltage_differential(
    adc, dac, adc_num: ADCNum, write_voltages: dict[DACChannel, float], expected_volt
    ):
    # write to DAC channel
    for channel, write_voltage in write_voltages.items():
        dac.write_voltage(channel, write_voltage)
    sleep(WRITE_READ_DELAY)
    for _ in range(READS_PER_WRITE):
        read_voltage = adc.read_voltage(adc_num)
        _logger.info(f"diff_read_voltage = {read_voltage}")
        _assert_approx(expected_volt, read_voltage, RW_ERROR)

def _generate_diff_test_cases():
    _logger.info(
            (
                f"voltage_range: 0-{MAX_VOLTAGE} V, voltage_step: {VOLTAGE_STEP} V, "
                f"read_write_error_tolerance: +/- {RW_ERROR} V, num_read_trials: {READS_PER_WRITE}"
            )
        )
    for diff in DiffMode:
        voltage = 0
        while voltage < MAX_VOLTAGE - VOLTAGE_STEP:
            voltage += VOLTAGE_STEP
            yield diff, voltage, voltage

@pytest.mark.parametrize("diff, mux_p_volt, mux_n_volt",
                        [
                        (DiffMode.DIFF_1, 1.5, 0.5),
                        (DiffMode.DIFF_1, 1.5, 0.6),
                        (DiffMode.DIFF_1, 1.5, 0.7),
                        (DiffMode.DIFF_1, 1.5, 0.8)
                        ])
def test_differential_rw_adc_1(diff, mux_p_volt, mux_n_volt, adc_1, dac):
    adc_1.select_differential(ADCNum.ADC_1, diff)
    _logger.info(
        f"voltage read/write diff pair: mux_p = {diff.value.mux_p}, mux_n = {diff.value.mux_n}"
        )
    _logger.info(f"mux_p_write_voltage = {mux_p_volt}, mux_n_write_voltage = {mux_n_volt}")
    write_voltages = {
        diff.value.mux_p: mux_p_volt,
        diff.value.mux_n: mux_n_volt,
    }
    expected_volt = mux_p_volt-mux_n_volt
    _measure_voltage_differential(adc_1, dac, ADCNum.ADC_1, write_voltages, expected_volt)

@pytest.mark.parametrize("diff, mux_p_volt, mux_n_volt",
                        [
                        (DiffMode.DIFF_1, 1.5, 0.5),
                        (DiffMode.DIFF_1, 1.5, 0.6),
                        (DiffMode.DIFF_1, 1.5, 0.7),
                        (DiffMode.DIFF_1, 1.5, 0.8)
                        ])
def test_differential_rw_adc_2(diff, mux_p_volt, mux_n_volt, adc_2, dac):
    adc_2.select_differential(ADCNum.ADC_2, diff)
    _logger.info(
        f"voltage read/write diff pair: mux_p = {diff.value.mux_p}, mux_n = {diff.value.mux_n}"
        )
    _logger.info(f"mux_p_write_voltage = {mux_p_volt}, mux_n_write_voltage = {mux_n_volt}")
    write_voltages = {
        diff.value.mux_p: mux_p_volt,
        diff.value.mux_n: mux_n_volt,
    }
    expected_volt = mux_p_volt-mux_n_volt
    _measure_voltage_differential(adc_2, dac, ADCNum.ADC_2, write_voltages, expected_volt)