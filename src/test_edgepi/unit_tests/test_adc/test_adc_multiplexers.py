"""" Unit tests for adc_multiplexers.py """


from contextlib import nullcontext as does_not_raise

import pytest
from edgepi.adc.adc_constants import ADCChannel as CH, ADCReg
from edgepi.reg_helper.reg_helper import BitMask, OpCode
from edgepi.adc.adc_multiplexers import (
    ChannelNotSetError,
    generate_mux_opcodes,
    _validate_mux_mapping,
    ChannelMappingError,
    ChannelNotAvailableError,
    validate_channels_allowed,
    validate_channels_set,
)


@pytest.mark.parametrize(
    "mux_regs, expected",
    [
        (
            {
                ADCReg.REG_INPMUX: [CH.AIN0.value, CH.AIN1.value],
                ADCReg.REG_ADC2MUX: [CH.AIN2.value, CH.AIN3.value],
            },
            does_not_raise(),
        ),
        (
            {
                ADCReg.REG_INPMUX: [CH.AIN0.value, CH.AIN0.value],
                ADCReg.REG_ADC2MUX: [CH.AIN2.value, CH.AIN3.value],
            },
            pytest.raises(ChannelMappingError),
        ),
        (
            {
                ADCReg.REG_INPMUX: [CH.AIN0.value, CH.AIN1.value],
                ADCReg.REG_ADC2MUX: [CH.AIN2.value, CH.AIN2.value],
            },
            pytest.raises(ChannelMappingError),
        ),
        (
            {
                ADCReg.REG_INPMUX: [CH.AIN0.value, CH.AIN0.value],
                ADCReg.REG_ADC2MUX: [CH.AIN0.value, CH.AIN0.value],
            },
            pytest.raises(ChannelMappingError),
        ),
        (
            {
                ADCReg.REG_INPMUX: [CH.AIN0.value, CH.AIN1.value],
                ADCReg.REG_ADC2MUX: [CH.AIN2.value, CH.AIN0.value],
            },
            does_not_raise(),
        ),
        (
            {
                ADCReg.REG_INPMUX: [CH.AIN0.value, CH.AIN2.value],
                ADCReg.REG_ADC2MUX: [CH.AIN2.value, CH.AIN1.value],
            },
            does_not_raise(),
        ),
        (
            {
                ADCReg.REG_INPMUX: [CH.AIN0.value, CH.AIN2.value],
                ADCReg.REG_ADC2MUX: [CH.AIN0.value, CH.AIN1.value],
            },
            does_not_raise(),
        ),
        (
            {
                ADCReg.REG_INPMUX: [CH.AIN0.value, CH.AIN1.value],
                ADCReg.REG_ADC2MUX: [CH.AIN2.value, CH.AIN1.value],
            },
            does_not_raise(),
        ),
        (
            {
                ADCReg.REG_INPMUX: [CH.FLOAT.value, CH.AIN2.value],
                ADCReg.REG_ADC2MUX: [CH.AIN2.value, CH.AIN3.value],
            },
            does_not_raise(),
        ),
        (
            {
                ADCReg.REG_INPMUX: [CH.FLOAT.value, CH.FLOAT.value],
                ADCReg.REG_ADC2MUX: [CH.AIN2.value, CH.AIN1.value],
            },
            does_not_raise(),
        ),
        (
            {
                ADCReg.REG_INPMUX: [CH.FLOAT.value, CH.FLOAT.value],
                ADCReg.REG_ADC2MUX: [CH.FLOAT.value, CH.FLOAT.value],
            },
            does_not_raise(),
        ),
    ],
)
def test_validate_mux_mapping(mux_regs, expected):
    with expected:
        _validate_mux_mapping(mux_regs)


@pytest.mark.parametrize(
    "mux_updates, mux_values, expected",
    [
        (
            {
                ADCReg.REG_INPMUX: (None, None),
                ADCReg.REG_ADC2MUX: (None, None),
            },
            {
                ADCReg.REG_INPMUX: [CH.AIN0.value, CH.AIN1.value],
                ADCReg.REG_ADC2MUX: [CH.AIN3.value, CH.AIN4.value],
            },
            [],
        ),
        (
            {
                ADCReg.REG_INPMUX: (None, CH.AIN2),
                ADCReg.REG_ADC2MUX: (None, None),
            },
            {
                ADCReg.REG_INPMUX: [CH.AIN0.value, CH.AIN1.value],
                ADCReg.REG_ADC2MUX: [CH.AIN3.value, CH.AIN4.value],
            },
            [OpCode(0x02, ADCReg.REG_INPMUX.value, BitMask.LOW_NIBBLE.value)],
        ),
        (
            {
                ADCReg.REG_INPMUX: (CH.AIN1, CH.AINCOM),
                ADCReg.REG_ADC2MUX: (None, None),
            },
            {
                ADCReg.REG_INPMUX: [CH.AIN0.value, CH.AIN1.value],
                ADCReg.REG_ADC2MUX: [CH.AIN3.value, CH.AIN4.value],
            },
            [OpCode(0x1A, ADCReg.REG_INPMUX.value, BitMask.BYTE.value)],
        ),
        (
            {
                ADCReg.REG_INPMUX: (CH.AIN7, None),
                ADCReg.REG_ADC2MUX: (None, None),
            },
            {
                ADCReg.REG_INPMUX: [CH.AIN0.value, CH.AIN1.value],
                ADCReg.REG_ADC2MUX: [CH.AIN3.value, CH.AIN4.value],
            },
            [OpCode(0x70, ADCReg.REG_INPMUX.value, BitMask.HIGH_NIBBLE.value)],
        ),
        (
            {
                ADCReg.REG_INPMUX: (None, CH.AIN5),
                ADCReg.REG_ADC2MUX: (None, None),
            },
            {
                ADCReg.REG_INPMUX: [CH.AIN1.value, CH.AIN2.value],
                ADCReg.REG_ADC2MUX: [CH.AIN3.value, CH.AIN4.value],
            },
            [OpCode(0x05, ADCReg.REG_INPMUX.value, BitMask.LOW_NIBBLE.value)],
        ),
        (
            {
                ADCReg.REG_INPMUX: (None, None),
                ADCReg.REG_ADC2MUX: (CH.AIN5, None),
            },
            {
                ADCReg.REG_INPMUX: [CH.AIN1.value, CH.AIN2.value],
                ADCReg.REG_ADC2MUX: [CH.AIN3.value, CH.AIN4.value],
            },
            [OpCode(0x50, ADCReg.REG_ADC2MUX.value, BitMask.HIGH_NIBBLE.value)],
        ),
        (
            {
                ADCReg.REG_INPMUX: (None, None),
                ADCReg.REG_ADC2MUX: (None, CH.AIN6),
            },
            {
                ADCReg.REG_INPMUX: [CH.AIN1.value, CH.AIN2.value],
                ADCReg.REG_ADC2MUX: [CH.AIN3.value, CH.AIN4.value],
            },
            [OpCode(0x06, ADCReg.REG_ADC2MUX.value, BitMask.LOW_NIBBLE.value)],
        ),
        (
            {
                ADCReg.REG_INPMUX: (None, None),
                ADCReg.REG_ADC2MUX: (CH.AIN5, CH.AIN6),
            },
            {
                ADCReg.REG_INPMUX: [CH.AIN1.value, CH.AIN2.value],
                ADCReg.REG_ADC2MUX: [CH.AIN3.value, CH.AIN4.value],
            },
            [OpCode(0x56, ADCReg.REG_ADC2MUX.value, BitMask.BYTE.value)],
        ),
        (
            {
                ADCReg.REG_INPMUX: (CH.AIN1, None),
                ADCReg.REG_ADC2MUX: (None, None),
            },
            {
                ADCReg.REG_INPMUX: [CH.AIN1.value, CH.AIN2.value],
                ADCReg.REG_ADC2MUX: [CH.AIN3.value, CH.AIN4.value],
            },
            [OpCode(0x10, ADCReg.REG_INPMUX.value, BitMask.HIGH_NIBBLE.value)],
        ),
        (
            {
                ADCReg.REG_INPMUX: (CH.AIN5, None),
                ADCReg.REG_ADC2MUX: (None, CH.AIN6),
            },
            {
                ADCReg.REG_INPMUX: [CH.AIN1.value, CH.AIN2.value],
                ADCReg.REG_ADC2MUX: [CH.AIN3.value, CH.AIN4.value],
            },
            [
                OpCode(0x50, ADCReg.REG_INPMUX.value, BitMask.HIGH_NIBBLE.value),
                OpCode(0x06, ADCReg.REG_ADC2MUX.value, BitMask.LOW_NIBBLE.value),
            ],
        ),
        (
            {
                ADCReg.REG_INPMUX: (None, CH.AIN5),
                ADCReg.REG_ADC2MUX: (CH.AIN6, None),
            },
            {
                ADCReg.REG_INPMUX: [CH.AIN1.value, CH.AIN2.value],
                ADCReg.REG_ADC2MUX: [CH.AIN3.value, CH.AIN4.value],
            },
            [
                OpCode(0x05, ADCReg.REG_INPMUX.value, BitMask.LOW_NIBBLE.value),
                OpCode(0x60, ADCReg.REG_ADC2MUX.value, BitMask.HIGH_NIBBLE.value),
            ],
        ),
        (
            {
                ADCReg.REG_INPMUX: (CH.AIN1, CH.AIN2),
                ADCReg.REG_ADC2MUX: (CH.AIN3, CH.AIN4),
            },
            {
                ADCReg.REG_INPMUX: [CH.AIN0.value, CH.AIN1.value],
                ADCReg.REG_ADC2MUX: [CH.AIN2.value, CH.AIN3.value],
            },
            [
                OpCode(0x12, ADCReg.REG_INPMUX.value, BitMask.BYTE.value),
                OpCode(0x34, ADCReg.REG_ADC2MUX.value, BitMask.BYTE.value),
            ],
        ),
    ],
)
def test_generate_mux_opcodes(mux_updates, mux_values, expected):
    assert generate_mux_opcodes(mux_updates, mux_values) == expected


@pytest.mark.parametrize(
    "mux_reg_val, expected_err",
    [
        (0x00, does_not_raise()),
        (0x10, does_not_raise()),
        (0x20, does_not_raise()),
        (0x30, does_not_raise()),
        (0x40, does_not_raise()),
        (0x50, does_not_raise()),
        (0x60, does_not_raise()),
        (0x70, does_not_raise()),
        (0x80, does_not_raise()),
        (0x90, does_not_raise()),
        (0xA0, does_not_raise()),
        (0xF0, pytest.raises(ChannelNotSetError)),
    ],
)
def test_validate_channels_set(mux_reg_val, expected_err):
    with expected_err:
        validate_channels_set(mux_reg_val)


@pytest.mark.parametrize(
    "channels, rtd_enabled, err_type",
    [
        ([CH.AIN1], True, does_not_raise()),
        ([CH.AIN0, CH.AIN1, CH.AIN2, CH.AIN3, CH.AINCOM, CH.FLOAT], False, does_not_raise()),
        (
            [
                CH.AIN0,
                CH.AIN1,
                CH.AIN2,
                CH.AIN3,
                CH.AIN3,
                CH.AIN4,
                CH.AIN5,
                CH.AIN6,
                CH.AIN7,
                CH.AINCOM,
                CH.FLOAT,
            ],
            True,
            does_not_raise(),
        ),
        ([CH.AIN4], False, pytest.raises(ChannelNotAvailableError)),
        (
            [
                CH.AIN4,
                CH.AIN5,
                CH.AIN6,
                CH.AIN7,
            ],
            False,
            pytest.raises(ChannelNotAvailableError),
        ),
    ],
)
def test_validate_channels_allowed(channels, rtd_enabled, err_type):
    with err_type:
        validate_channels_allowed(channels, rtd_enabled)
