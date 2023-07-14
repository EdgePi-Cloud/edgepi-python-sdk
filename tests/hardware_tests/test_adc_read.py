"Hardware ADC single-ended test"

import logging

from time import sleep
import pytest
from edgepi.dac.dac_constants import DACChannel
from edgepi.adc.edgepi_adc import EdgePiADC
from edgepi.adc.adc_constants import AnalogIn, ADCNum
from edgepi.dac.edgepi_dac import EdgePiDAC

_logger = logging.getLogger(__name__)

NUM_CHANNELS = 2
READS_PER_WRITE = 1
RW_ERROR = 1e-1 # TODO: change to mV
MAX_VOLTAGE = 5.0
VOLTAGE_STEP = 0.5
WRITE_READ_DELAY = 0.1

_ch_map = {
    0: (AnalogIn.AIN1, DACChannel.AOUT1),
    1: (AnalogIn.AIN2, DACChannel.AOUT2),
    2: (AnalogIn.AIN3, DACChannel.AOUT3),
    3: (AnalogIn.AIN4, DACChannel.AOUT4),
    4: (AnalogIn.AIN5, DACChannel.AOUT5),
    5: (AnalogIn.AIN6, DACChannel.AOUT6),
    6: (AnalogIn.AIN7, DACChannel.AOUT7),
    7: (AnalogIn.AIN8, DACChannel.AOUT8),
}

@pytest.fixture(name="dac", scope="module")
def fixture_dac():
    return EdgePiDAC()

@pytest.fixture(name="adc_1", scope="module")
def fixture_adc_1():
    adc = EdgePiADC()
    adc.start_conversions(ADCNum.ADC_1)
    yield adc
    adc.stop_conversions(ADCNum.ADC_1)

def _assert_approx(a: float, b: float, error: float):
    """assert `b` is within +/- `error` of `a`"""
    # pylint: disable=invalid-name
    assert (a - error) <= b <= (a + error)


def _voltage_rw_msg(dac_ch: DACChannel, write_voltage: float, read_voltage: float) -> str:
    return (
        f"\nchannel_number={dac_ch.value}, "
        f"write_voltage={write_voltage} V, read_voltage={read_voltage} V"
        f"\nassert {read_voltage} == {write_voltage} ± {RW_ERROR}\n"
    )


def _measure_voltage_individual(
    adc, dac, adc_num: ADCNum, dac_ch: DACChannel, write_voltage: float
    ):
    # write to DAC channel
    dac.write_voltage(dac_ch, write_voltage)
    sleep(WRITE_READ_DELAY)
    for _ in range(READS_PER_WRITE):
        read_voltage = adc.read_voltage(adc_num)
        _logger.info(_voltage_rw_msg(dac_ch, write_voltage, read_voltage))
        _assert_approx(write_voltage, read_voltage, RW_ERROR)


def _generate_test_cases():
    _logger.info(
            (
                f"voltage_range: 0-{MAX_VOLTAGE} V, voltage_step: {VOLTAGE_STEP} V, "
                f"read_write_error_tolerance: +/- {RW_ERROR} V, num_read_trials: {READS_PER_WRITE}"
            )
        )
    for channel in range(NUM_CHANNELS):
        voltage = 0
        while voltage < MAX_VOLTAGE - VOLTAGE_STEP:
            voltage += VOLTAGE_STEP
            yield channel, voltage


@pytest.mark.parametrize("channel, write_voltage", _generate_test_cases())
def test_voltage_rw_adc_1(channel, write_voltage, adc_1, dac):
    adc_1.set_config(adc_1_analog_in=_ch_map[channel][0])
    _measure_voltage_individual(adc_1, dac, ADCNum.ADC_1, _ch_map[channel][1], write_voltage)

@pytest.mark.parametrize("channel, write_voltage", _generate_test_cases())
def test_voltage_rw_adc_2(channel, write_voltage, adc_1, dac):
    adc_1.set_config(adc_1_analog_in=_ch_map[channel][0])
    _measure_voltage_individual(adc_1, dac, ADCNum.ADC_1, _ch_map[channel][1], write_voltage)