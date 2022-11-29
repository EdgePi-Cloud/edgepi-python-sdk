import logging

import pytest
from edgepi.adc.edgepi_adc import EdgePiADC
from edgepi.adc.adc_constants import ADCChannel, ADCNum
from edgepi.dac.edgepi_dac import EdgePiDAC
from edgepi.dac.dac_constants import DACChannel

_logger = logging.getLogger(__name__)

NUM_CHANNELS = 8
READS_PER_WRITE = 1
RW_ERROR = 1e-1
MAX_VOLTAGE = 5.0
VOLTAGE_STEP = 0.1

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

@pytest.fixture(name="adc", scope="module")
def fixture_adc():
    adc = EdgePiADC()
    adc.start_conversions(ADCNum.ADC_1)
    yield adc
    adc.stop_conversions(ADCNum.ADC_1)


@pytest.fixture(name="dac", scope="module")
def fixture_dac():
    return EdgePiDAC()


def _assert_approx(a: float, b: float, error: float):
    """assert `b` is within +/- `error` of `a`"""
    assert (a - error) <= b <= (a + error)


def _voltage_rw_msg(dac_ch: DACChannel, write_voltage: float, read_voltage: float) -> str:
    return (
        f"\nchannel_number={dac_ch.value}, "
        f"write_voltage={write_voltage} V, read_voltage={read_voltage} V"
        f"\nassert {read_voltage} == {write_voltage} ± {RW_ERROR}\n"
    )
        

def _measure_voltage(adc, dac, adc_num: ADCNum, dac_ch: DACChannel, write_voltage: float):
    # write to DAC channel
    dac.write_voltage(dac_ch, write_voltage)

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
        for voltage in range(0, MAX_VOLTAGE, VOLTAGE_STEP):
            yield channel, voltage


@pytest.mark.parametrize("channel, write_voltage", _generate_test_cases())
def test_voltage_rw_adc_1(channel, write_voltage, adc, dac):
    adc.set_config(adc_1_analog_in=_ch_map[channel][0])
    _measure_voltage(adc, dac, ADCNum.ADC_1, _ch_map[channel][1], write_voltage)
