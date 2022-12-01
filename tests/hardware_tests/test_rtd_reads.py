import pytest
from edgepi.adc.edgepi_adc import EdgePiADC
from edgepi.adc.adc_constants import ADCNum


# This has to be manually set with temperature machine. Use this value for testing.
RTD_TEMP = 50
ERROR = 1


@pytest.fixture(name="rtd")
def fixture_rtd():
    adc = EdgePiADC()
    adc.rtd_mode(True)

def test_single_sample_rtd(rtd):
    out = rtd.single_sample_rtd()
    assert out == pytest.approx(RTD_TEMP, abs=ERROR)


def test_read_rtd_temperature(rtd):
    rtd.start_conversions(ADCNum.ADC_1)
    for _ in range(10):
        out = rtd.read_rtd_temperature()
        assert out == pytest.approx(RTD_TEMP, abs=ERROR)
    rtd.stop_conversions(ADCNum.ADC_1)
