"""Unit tests for adc_voltage.py module"""


from contextlib import nullcontext as does_not_raise

import pytest
from edgepi.adc.adc_constants import ADCNum
from edgepi.adc.adc_voltage import (
    check_crc,
    CRCCheckError,
    _code_to_input_voltage,
)

# pylint: disable=too-many-lines


V_REF = ADCNum.ADC_1.value.voltage_config.v_ref
GAIN = ADCNum.ADC_1.value.voltage_config.gain
OFFSET = ADCNum.ADC_1.value.voltage_config.offset


@pytest.mark.parametrize(
    "code, voltage, num_bytes",
    [
        (0x00000000, 0, ADCNum.ADC_1.value.num_data_bytes),
        # based on a reference voltage of 2.5 V
        (
            0xFFFFFFFF,
            5.0,
            ADCNum.ADC_1.value.num_data_bytes,
        ),
    ],
)
def test_code_to_voltage(code, voltage, num_bytes):
    assert pytest.approx(_code_to_input_voltage(code, V_REF, num_bytes * 8)) == voltage


@pytest.mark.parametrize(
    "voltage_bytes, crc_code, err",
    [
        ([51, 16, 126, 166], 62, does_not_raise()),
        ([51, 14, 170, 195], 98, does_not_raise()),
        ([51, 16, 133, 237], 75, does_not_raise()),
        ([51, 17, 166, 166], 71, does_not_raise()),
        ([51, 16, 148, 157], 94, does_not_raise()),
        ([51, 14, 144, 155], 150, does_not_raise()),
        ([51, 14, 166, 18], 167, does_not_raise()),
        ([51, 16, 5, 109], 116, does_not_raise()),
        ([51, 15, 16, 130], 4, does_not_raise()),
        ([51, 16, 126, 166], 61, pytest.raises(CRCCheckError)),
        ([51, 14, 170, 195], 99, pytest.raises(CRCCheckError)),
        ([51, 16, 133, 237], 70, pytest.raises(CRCCheckError)),
    ],
)
def test_crc_8_atm_adc_1(voltage_bytes, crc_code, err):
    with err:
        check_crc(voltage_bytes, crc_code)
