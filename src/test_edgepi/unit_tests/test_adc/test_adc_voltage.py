"""Unit tests for adc_voltage.py module"""


from contextlib import nullcontext as does_not_raise

import pytest
from edgepi.utilities.utilities import bitstring_from_list
from edgepi.adc.adc_constants import ADCNum
from edgepi.adc.adc_crc_8_atm import (
    generate_crc_8_table,
    check_crc,
    CRCCheckError,
    CRC_8_ATM_GEN,
)
from edgepi.adc.adc_voltage import (
    _code_to_input_voltage,
    _is_negative_voltage,
    _adc_voltage_to_input_voltage,
    code_to_temperature,
    STEP_DOWN_RESISTOR_1,
    STEP_DOWN_RESISTOR_2
)
from edgepi.adc.adc_crc_8_atm import CRC_8_ATM_LUT

# pylint: disable=too-many-lines

# mock calib values
V_REF = 2.5
GAIN = 1
OFFSET = 0

@pytest.mark.parametrize("code, result",
                        [([0xFF,0xFF,0xFF,0xFF], True),
                         ([0x7F,0xFF,0xFF,0xFF], False),
                        ])
def test_is_negative_voltage(code, result):
    code_bits = bitstring_from_list(code)
    assert _is_negative_voltage(code_bits) ==result


@pytest.mark.parametrize(
    "code, voltage, num_bytes",
    [
        ([0,0,0,0], 0, ADCNum.ADC_1.value.num_data_bytes),
        ([0,0,0,0], 0, ADCNum.ADC_2.value.num_data_bytes),
        # based on a reference voltage of 2.5 V
        (
            [0x7F,0xFF,0xFF,0xFF],
            2.5,
            ADCNum.ADC_1.value.num_data_bytes,
        ),        (
            [0x80,0x0,0x0,0x0],
            -2.5,
            ADCNum.ADC_1.value.num_data_bytes,
        ),
        (
            [0x7F,0xFF,0xFF,0xFF],
            2.5,
            ADCNum.ADC_2.value.num_data_bytes,
        ),
        (
            [0x80,0x0,0x0,0x0],
            -2.5,
            ADCNum.ADC_2.value.num_data_bytes,
        ),
    ],
)
def test_code_to_input_voltage(code, voltage, num_bytes):
    code_bits = bitstring_from_list(code[:num_bytes])
    num_bits = num_bytes * 8
    code_uint = code_bits.uint
    # handling negative number
    if _is_negative_voltage(code_bits):
        code_uint = code_uint - 2**num_bits
    assert pytest.approx(_code_to_input_voltage(code_uint, V_REF, num_bytes * 8),0.0001) == voltage


@pytest.mark.parametrize(
    "code, voltage, num_bytes",
    [
        ([0,0,0,0], 0, ADCNum.ADC_1.value.num_data_bytes),
        ([0,0,0,0], 0, ADCNum.ADC_2.value.num_data_bytes),
        # based on a reference voltage of 2.5 V
        (
            [0x7F,0xFF,0xFF,0xFF],
            2.5,
            ADCNum.ADC_1.value.num_data_bytes,
        ),        (
            [0x80,0x0,0x0,0x0],
            -2.5,
            ADCNum.ADC_1.value.num_data_bytes,
        ),
        (
            [0x7F,0xFF,0xFF,0xFF],
            2.5,
            ADCNum.ADC_2.value.num_data_bytes,
        ),
        (
            [0x80,0x0,0x0,0x0],
            -2.5,
            ADCNum.ADC_2.value.num_data_bytes,
        ),
    ],
)
def test__adc_voltage_to_input_voltage(code, voltage, num_bytes):
    code_bits = bitstring_from_list(code[:num_bytes])
    num_bits = num_bytes * 8
    code_uint = code_bits.uint
    # handling negative number
    if _is_negative_voltage(code_bits):
        code_uint = code_uint - 2**num_bits
    vin = _code_to_input_voltage(code_uint, V_REF, num_bits)
    assert pytest.approx(_adc_voltage_to_input_voltage(vin, GAIN, OFFSET),0.0001) == \
           voltage * (STEP_DOWN_RESISTOR_1 + STEP_DOWN_RESISTOR_2) / STEP_DOWN_RESISTOR_2


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


def test_generate_crc_8_table():
    assert generate_crc_8_table(CRC_8_ATM_GEN) == CRC_8_ATM_LUT


@pytest.mark.parametrize(
    "code, ref_resistance, temp_offset, rtd_conv_constant",
    [
        ([51, 16, 126, 166], 1326.20, 100, 0.385),
        ([0x8, 0x43, 0x1C, 0x45], 1326.20, 100, 0.385),
    ]
)
def test_code_to_temperature(code, ref_resistance, temp_offset, rtd_conv_constant):
    # TODO: add check for expected value later if any values are known. No errors raised
    # is good enough for now.
    code_to_temperature(code, ref_resistance, temp_offset, rtd_conv_constant)
