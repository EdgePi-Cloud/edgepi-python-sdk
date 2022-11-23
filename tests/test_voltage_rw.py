import logging

import pytest
from pytest_check import check
from edgepi.adc.edgepi_adc import EdgePiADC
from edgepi.adc.adc_constants import ADCChannel, ADCNum
from edgepi.dac.edgepi_dac import EdgePiDAC
from edgepi.dac.dac_constants import DACChannel

_logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.error)

NUM_CHANNELS = 8
NUM_ADC_READS = 10
RW_ERROR = 1e-1
MAX_VOLTAGE = 5.0
VOLTAGE_STEP = 1.0

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
    

def _measure_voltage(adc, dac, adc_num: ADCNum, dac_ch: int, write_voltage: float):
    # write to DAC channel
    dac.write_voltage(dac_ch, write_voltage)

    for _ in range(NUM_ADC_READS):
        read_voltage = adc.read_voltage(adc_num)
        try:
            assert write_voltage == pytest.approx(read_voltage, abs=RW_ERROR)
        except AssertionError as err:
            _logger.error(f"voltage read error exceeds tolerance: {err}")

def test_voltage_rw_adc_1(adc, dac):
    # set ADC read channel
    adc.start_conversions(ADCNum.ADC_1)

    for ch in range(NUM_CHANNELS):
        adc.set_config(adc_1_analog_in=_ch_map[ch][0])

        voltage = 0
        while voltage <= MAX_VOLTAGE:
            _measure_voltage(adc, dac, ADCNum.ADC_1, _ch_map[ch][1], voltage)
            voltage += VOLTAGE_STEP
            
    
    adc.stop_conversions(ADCNum.ADC_1)
