"""Hardware tests for RTD temperature reading accuracy"""

import pytest
from edgepi.adc.edgepi_adc import EdgePiADC
from edgepi.adc.adc_constants import ADCNum, ConvMode


# This has to be manually set with temperature machine. Use this value for testing.
RTD_TEMP = 28
ERROR = 1


@pytest.fixture(name="rtd", scope="module")
def fixture_rtd():
    adc = EdgePiADC()
    adc.set_rtd(True)
    return adc

def test_single_sample_rtd(rtd):
    out = rtd.single_sample_rtd()
    assert out == pytest.approx(RTD_TEMP, abs=ERROR)
    rtd.reset()


def test_read_rtd_temperature(rtd):
    rtd.set_config(conversion_mode=ConvMode.CONTINUOUS)
    rtd.start_conversions(ADCNum.ADC_2)
    for _ in range(10):
        out = rtd.read_rtd_temperature()
        assert out == pytest.approx(RTD_TEMP, abs=ERROR)
    rtd.stop_conversions(ADCNum.ADC_2)
    rtd.reset()

