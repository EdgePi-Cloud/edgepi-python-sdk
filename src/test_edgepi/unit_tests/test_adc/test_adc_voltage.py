"""Unit tests for adc_voltage.py module"""

import pytest

from edgepi.calibration.calibration_constants import CalibParam
from edgepi.utilities.utilities import bitstring_from_list
from edgepi.adc.adc_constants import ADCNum
from edgepi.adc.adc_voltage import (
    _code_to_input_voltage,
    _is_negative_voltage,
    _adc_voltage_to_input_voltage,
    code_to_voltage,
    code_to_voltage_single_ended,
    code_to_temperature,
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
        (0, 0, ADCNum.ADC_1.value.num_data_bytes),
        (0, 0, ADCNum.ADC_2.value.num_data_bytes),
        # based on a reference voltage of 2.5 V
        (
            2147483647,
            2.5,
            ADCNum.ADC_1.value.num_data_bytes,
        ),
        (
            -2147483648,
            -2.5,
            ADCNum.ADC_1.value.num_data_bytes,
        ),
        (
            8388607,
            2.5,
            ADCNum.ADC_2.value.num_data_bytes,
        ),
        (
            -8388608,
            -2.5,
            ADCNum.ADC_2.value.num_data_bytes,
        ),
    ],
)
def test_code_to_input_voltage(code, voltage, num_bytes):
    assert pytest.approx(_code_to_input_voltage(code, V_REF, num_bytes * 8),0.0001) == voltage


@pytest.mark.parametrize(
    "voltage, gain, offset, result",
    [
        (0	  ,1, -0.014, -0.014),
        (0.25 ,1, -0.014, 1.192913828),
        (0.5  ,1, -0.014, 2.399827655),
        (0.75 ,1, -0.014, 3.606741483),
        (1	  ,1, -0.014, 4.813655311),
        (1.25 ,1, -0.014, 6.020569138),
        (1.5  ,1, -0.014, 7.227482966),
        (1.75 ,1, -0.014, 8.434396794),
        (2	  ,1, -0.014, 9.641310621),
        (2.25 ,1, -0.014, 10.84822445),
        (2.5  ,1, -0.014, 12.05513828),
    ],
)
def test__adc_voltage_to_input_voltage(voltage, gain, offset, result):
    assert pytest.approx(_adc_voltage_to_input_voltage(voltage, gain, offset),0.0001) == result

@pytest.mark.parametrize(
    "code, adc_num, calibs, result",
    [
        ([0x00, 0x00, 0x00, 0x00], ADCNum.ADC_1.value,CalibParam(gain=1, offset=0.0), 0),
        ([0x7F, 0xFF, 0xFF, 0xFF], ADCNum.ADC_1.value,CalibParam(gain=1, offset=0.0), 12.069),
        ([0x80, 0x00, 0x00, 0x00], ADCNum.ADC_1.value,CalibParam(gain=1, offset=0.0), -12.069),
        ([0x00, 0x00, 0x00, 0x00], ADCNum.ADC_1.value,CalibParam(gain=1, offset=0.0), 0),
        ([0x00, 0x00, 0x00, 0x00], ADCNum.ADC_1.value,CalibParam(gain=1, offset=0.0), 0),
        ([0x00, 0x00, 0x00, 0x00], ADCNum.ADC_2.value,CalibParam(gain=1, offset=0.0), 0),
        ([0x7F, 0xFF, 0xFF, 0xFF], ADCNum.ADC_2.value,CalibParam(gain=1, offset=0.0), 12.069),
        ([0x7F, 0xFF, 0xFF, 0x00], ADCNum.ADC_2.value,CalibParam(gain=1, offset=0.0), 12.069),
        ([0x80, 0x00, 0x00, 0xFF], ADCNum.ADC_2.value,CalibParam(gain=1, offset=0.0), -12.069),
        ([0x80, 0x00, 0x00, 0x00], ADCNum.ADC_2.value,CalibParam(gain=1, offset=0.0), -12.069),
        ([0x00, 0x00, 0x00, 0x00], ADCNum.ADC_2.value,CalibParam(gain=1, offset=0.0), 0),
    ],
)
def test_code_to_voltage(code, adc_num, calibs, result):
    assert pytest.approx(code_to_voltage(code, adc_num, calibs),0.0001) == result

@pytest.mark.parametrize(
    "code, adc_num, calibs, result",
    [
        ([0x00, 0x00, 0x00, 0x00], ADCNum.ADC_1.value,CalibParam(gain=1, offset=0.00), 12.069),
        ([0x7F, 0xFF, 0xFF, 0xFF], ADCNum.ADC_1.value,CalibParam(gain=1, offset=0.00), 24.138),
        ([0x80, 0x00, 0x00, 0x00], ADCNum.ADC_1.value,CalibParam(gain=1, offset=0.00), 0.00),
        ([0x00, 0x00, 0x00, 0x00], ADCNum.ADC_1.value,CalibParam(gain=1, offset=0.00), 12.069),
        ([0x00, 0x00, 0x00, 0x00], ADCNum.ADC_1.value,CalibParam(gain=1, offset=0.00), 12.069),
        ([0x00, 0x00, 0x00, 0x00], ADCNum.ADC_2.value,CalibParam(gain=1, offset=0.00), 12.069),
        ([0x7F, 0xFF, 0xFF, 0xFF], ADCNum.ADC_2.value,CalibParam(gain=1, offset=0.00), 24.138),
        ([0x7F, 0xFF, 0xFF, 0x00], ADCNum.ADC_2.value,CalibParam(gain=1, offset=0.00), 24.138),
        ([0x80, 0x00, 0x00, 0xFF], ADCNum.ADC_2.value,CalibParam(gain=1, offset=0.00), 0.00),
        ([0x80, 0x00, 0x00, 0x00], ADCNum.ADC_2.value,CalibParam(gain=1, offset=0.00), 0.00),
        ([0x00, 0x00, 0x00, 0x00], ADCNum.ADC_2.value,CalibParam(gain=1, offset=0.00), 12.069),
    ],
)
def test_code_to_voltage_single_ended(code, adc_num, calibs, result):
    assert pytest.approx(code_to_voltage_single_ended(code, adc_num, calibs),0.0001) == result

@pytest.mark.parametrize(
    "code, ref_resistance, temp_offset, rtd_conv_constant,rtd_gain,rtd_offset,adc_num,expected",
    [
        ([0x03, 0x85, 0x1E, 0xB8], 2000, 100, 0.385,1,0, ADCNum.ADC_1, 25.97),
        ([0x03, 0x85, 0x1E], 2000, 100, 0.385,1,0, ADCNum.ADC_2, 25.97),
        ([0x03, 0x85, 0x1E, 0xB8], 2000, 100, 0.385,1,-0.5, ADCNum.ADC_1, 25.47),
        ([0x03, 0x85, 0x1E], 2000, 100, 0.385,1,-0.5, ADCNum.ADC_2, 25.47),
    ]
)
def test_code_to_temperature(
            code,ref_resistance,temp_offset,rtd_conv_constant,rtd_gain,rtd_offset,adc_num,expected):
    temperature = code_to_temperature(
                    code,ref_resistance,temp_offset,rtd_conv_constant,rtd_gain,rtd_offset,adc_num)
    assert expected == pytest.approx(temperature, 0.001)
