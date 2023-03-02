"""Unit tests for adc_voltage.py module"""

import pytest

from edgepi.utilities.utilities import bitstring_from_list
from edgepi.adc.adc_constants import ADCNum
from edgepi.adc.adc_voltage import (
    _code_to_input_voltage,
    _is_negative_voltage,
    _adc_voltage_to_input_voltage,
    code_to_temperature,
    STEP_DOWN_RESISTOR_1,
    STEP_DOWN_RESISTOR_2
)

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
