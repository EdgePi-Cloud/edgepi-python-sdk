"""" Unit tests for adc_multiplexers.py """


from contextlib import nullcontext as does_not_raise

import pytest
from edgepi.adc.adc_constants import ADCChannel as CH, ADCReg
from edgepi.reg_helper.reg_helper import BitMask, OpCode
from edgepi.adc.adc_multiplexers import (
    generate_mux_opcodes,
    ChannelNotAvailableError,
    validate_channels_allowed,
)


@pytest.mark.parametrize(
    "mux_updates, expected",
    [
        (
            {
                ADCReg.REG_INPMUX: (None, None),
                ADCReg.REG_ADC2MUX: (None, None),
            },
            [],
        ),
        (
            {
                ADCReg.REG_INPMUX: (None, CH.AIN2),
                ADCReg.REG_ADC2MUX: (None, None),
            },
            [],
        ),
        (
            {
                ADCReg.REG_INPMUX: (CH.AIN1, CH.AINCOM),
                ADCReg.REG_ADC2MUX: (None, None),
            },
            [OpCode(0x1A, ADCReg.REG_INPMUX.value, BitMask.BYTE.value)],
        ),
        (
            {
                ADCReg.REG_INPMUX: (CH.AIN7, None),
                ADCReg.REG_ADC2MUX: (None, None),
            },
            [],
        ),
        (
            {
                ADCReg.REG_INPMUX: (None, CH.AIN5),
                ADCReg.REG_ADC2MUX: (None, None),
            },
            [],
        ),
        (
            {
                ADCReg.REG_INPMUX: (None, None),
                ADCReg.REG_ADC2MUX: (CH.AIN5, None),
            },
            [],
        ),
        (
            {
                ADCReg.REG_INPMUX: (None, None),
                ADCReg.REG_ADC2MUX: (None, CH.AIN6),
            },
            [],
        ),
        (
            {
                ADCReg.REG_INPMUX: (None, None),
                ADCReg.REG_ADC2MUX: (CH.AIN5, CH.AIN6),
            },
            [OpCode(0x56, ADCReg.REG_ADC2MUX.value, BitMask.BYTE.value)],
        ),
        (
            {
                ADCReg.REG_INPMUX: (CH.AIN1, None),
                ADCReg.REG_ADC2MUX: (None, None),
            },
            [],
        ),
        (
            {
                ADCReg.REG_INPMUX: (CH.AIN5, None),
                ADCReg.REG_ADC2MUX: (None, CH.AIN6),
            },
            [],
        ),
        (
            {
                ADCReg.REG_INPMUX: (None, CH.AIN5),
                ADCReg.REG_ADC2MUX: (CH.AIN6, None),
            },
            [],
        ),
        (
            {
                ADCReg.REG_INPMUX: (CH.AIN1, CH.AIN2),
                ADCReg.REG_ADC2MUX: (CH.AIN3, CH.AIN4),
            },
            [
                OpCode(0x12, ADCReg.REG_INPMUX.value, BitMask.BYTE.value),
                OpCode(0x34, ADCReg.REG_ADC2MUX.value, BitMask.BYTE.value),
            ],
        ),
    ],
)
def test_generate_mux_opcodes(mux_updates, expected):
    assert generate_mux_opcodes(mux_updates) == expected


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
            pytest.raises(ChannelNotAvailableError),
        ),
        ([CH.AIN4], True, pytest.raises(ChannelNotAvailableError)),
        (
            [
                CH.AIN4,
                CH.AIN5,
                CH.AIN6,
                CH.AIN7,
            ],
            True,
            pytest.raises(ChannelNotAvailableError),
        ),
    ],
)
def test_validate_channels_allowed(channels, rtd_enabled, err_type):
    with err_type:
        validate_channels_allowed(channels, rtd_enabled)
