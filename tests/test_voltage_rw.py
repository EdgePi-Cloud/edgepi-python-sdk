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
    return EdgePiADC()


@pytest.fixture(name="dac", scope="module")
def fixture_dac():
    return EdgePiDAC()


def _measure_voltage(adc, dac, adc_num: ADCNum, dac_ch: DACChannel, write_voltage: float):
    # write to DAC channel
    dac.write_voltage(dac_ch, write_voltage)

    num_failed = 0
    for _ in range(READS_PER_WRITE):
        read_voltage = adc.read_voltage(adc_num)
        try:
            assert read_voltage == pytest.approx(write_voltage, abs=RW_ERROR)
        except AssertionError as err:
            _logger.error(
                    (
                        "voltage read-write error exceeds tolerance: "
                        f"channel_number={dac_ch.value}, "
                        f"write_voltage={write_voltage} V, read_voltage={read_voltage} V\n{err}"
                    )
                )
            num_failed += 1

    return num_failed

def test_voltage_rw_adc_1(adc, dac):
    # set ADC read channel
    adc.start_conversions(ADCNum.ADC_1)

    _logger.info("starting voltage read-write test with ADC1")
    _logger.info(
            (
                f"voltage_range: 0-{MAX_VOLTAGE} V, voltage_step: {VOLTAGE_STEP} V, "
                f"read_write_error_tolerance: +/- {RW_ERROR} V, num_read_trials: {READS_PER_WRITE}"
            )
        )

    num_failed = 0
    for ch in range(NUM_CHANNELS):
        adc.set_config(adc_1_analog_in=_ch_map[ch][0])

        voltage = 0
        while voltage <= MAX_VOLTAGE:
            num_failed += _measure_voltage(adc, dac, ADCNum.ADC_1, _ch_map[ch][1], voltage)
            voltage += VOLTAGE_STEP

    adc.stop_conversions(ADCNum.ADC_1)

    if num_failed > 0:
        total_tests = NUM_CHANNELS * (MAX_VOLTAGE / VOLTAGE_STEP) * READS_PER_WRITE
        raise AssertionError(f"voltage read-write test failed: {num_failed}/{int(total_tests)} tests failed")
