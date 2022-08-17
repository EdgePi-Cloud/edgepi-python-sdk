"""unit tests for adc_commands module"""


import pytest
from edgepi.adc.adc_commands import ADCCommands
from edgepi.adc.adc_constants import ADCChannel as CH, ADCReg
from edgepi.reg_helper.reg_helper import BitMask, OpCode


@pytest.fixture(name="adc_ops")
def fixture_test_adc_ops():
    adc_ops = ADCCommands()
    return adc_ops


@pytest.mark.parametrize(
    "sample, result",
    [
        ([1], True),
        ([1, 2, 3, 4, 5], True),
        ([-1, 1, 2, 3], True),
        ([444, 22, 3333, 5], True),
        ([-111, -2222], True),
    ],
)
def test_check_for_int(sample, result, adc_ops):
    assert adc_ops.check_for_int(sample) == result


@pytest.mark.parametrize(
    "sample, error",
    [
        ([1, 2.22, 3, 4, 0], ValueError),
        ([None, 1, 2, 3], ValueError),
        ([], ValueError),
        ([-1, -2.22], ValueError),
    ],
)
def test_check_for_int_exception(sample, error, adc_ops):
    with pytest.raises(Exception) as err:
        adc_ops.check_for_int(sample)
    assert err.type is error


# Test read register content
# In: Register address and number of register to read
# Out: List of bytes Op-code and dummy bytes to transfer


@pytest.mark.parametrize(
    "address, num_of_regs, result",
    [
        (1, 1, [0x21, 0, 255]),
        (2, 4, [0x22, 3, 255, 255, 255, 255]),
        (3, 5, [0x23, 4, 255, 255, 255, 255, 255]),
        (10, 7, [0x2A, 6, 255, 255, 255, 255, 255, 255, 255]),
        (16, 10, [0x30, 9, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255]),
        (16, 1, [0x30, 0, 255]),
    ],
)
def test_read_register_command(address, num_of_regs, result, adc_ops):
    assert adc_ops.read_register_command(address, num_of_regs) == result


@pytest.mark.parametrize(
    "address, num_of_regs, error", [(1, 3.2, ValueError), (3.2, 1, ValueError)]
)
def test_read_register_command_exception(address, num_of_regs, error, adc_ops):
    with pytest.raises(Exception) as err:
        adc_ops.read_register_command(address, num_of_regs)
        assert err.type is error


# Test write register content
# In: Register address and list of values to write
# Out: List of bytes Op-code and dummy bytes to transfer


@pytest.mark.parametrize(
    "address, values, result",
    [
        (1, [2], [0x41, 0, 2]),
        (2, [23, 25, 24, 102], [0x42, 3, 23, 25, 24, 102]),
        (3, [243, 123, 125, 111, 231], [0x43, 4, 243, 123, 125, 111, 231]),
        (10, [15, 25, 55, 225, 115, 2, 2], [0x4A, 6, 15, 25, 55, 225, 115, 2, 2]),
        (
            16,
            [25, 55, 5, 2, 5, 25, 55, 55, 25, 2],
            [0x50, 9, 25, 55, 5, 2, 5, 25, 55, 55, 25, 2],
        ),
    ],
)
def test_write_register_command(address, values, result, adc_ops):
    assert adc_ops.write_register_command(address, values) == result


@pytest.mark.parametrize(
    "address, values, error",
    [(1, [-1, 2], ValueError), (2, [23, 25, 256, 102], ValueError)],
)
def test_write_register_command_exception(address, values, error, adc_ops):
    with pytest.raises(Exception) as err:
        adc_ops.write_register_command(address, values)
        assert err.type is error


@pytest.mark.parametrize(
    "adc_1_mux_p, adc_2_mux_p, adc_1_mux_n, adc_2_mux_n, expected",
    [
        (None, None, None, None, []),
        (
            CH.AIN0,
            None,
            None,
            None,
            [
                OpCode(
                    op_code=0,
                    reg_address=ADCReg.REG_INPMUX.value,
                    op_mask=BitMask.HIGH_NIBBLE.value,
                )
            ],
        ),
        (
            None,
            CH.AIN1,
            None,
            None,
            [
                OpCode(
                    op_code=0x10,
                    reg_address=ADCReg.REG_ADC2MUX.value,
                    op_mask=BitMask.HIGH_NIBBLE.value,
                )
            ],
        ),
        (
            CH.AIN0,
            CH.AIN1,
            None,
            None,
            [
                OpCode(
                    op_code=0x00,
                    reg_address=ADCReg.REG_INPMUX.value,
                    op_mask=BitMask.HIGH_NIBBLE.value,
                ),
                OpCode(
                    op_code=0x10,
                    reg_address=ADCReg.REG_ADC2MUX.value,
                    op_mask=BitMask.HIGH_NIBBLE.value,
                ),
            ],
        ),
        (
            None,
            None,
            CH.AINCOM,
            None,
            [
                OpCode(
                    op_code=0x0A,
                    reg_address=ADCReg.REG_INPMUX.value,
                    op_mask=BitMask.LOW_NIBBLE.value,
                )
            ],
        ),
        (
            None,
            None,
            None,
            CH.AINCOM,
            [
                OpCode(
                    op_code=0x0A,
                    reg_address=ADCReg.REG_ADC2MUX.value,
                    op_mask=BitMask.LOW_NIBBLE.value,
                )
            ],
        ),
        (
            CH.AIN0,
            CH.AIN1,
            CH.AIN2,
            CH.AIN3,
            [
                OpCode(
                    op_code=0x02,
                    reg_address=ADCReg.REG_INPMUX.value,
                    op_mask=BitMask.BYTE.value,
                ),
                OpCode(
                    op_code=0x13,
                    reg_address=ADCReg.REG_ADC2MUX.value,
                    op_mask=BitMask.BYTE.value,
                )
            ],
        ),
        (
            CH.AIN0,
            None,
            CH.AIN2,
            CH.AIN3,
            [
                OpCode(
                    op_code=0x02,
                    reg_address=ADCReg.REG_INPMUX.value,
                    op_mask=BitMask.BYTE.value,
                ),
                OpCode(
                    op_code=0x03,
                    reg_address=ADCReg.REG_ADC2MUX.value,
                    op_mask=BitMask.LOW_NIBBLE.value,
                )
            ],
        ),
        (
            None,
            CH.AIN1,
            CH.AIN2,
            CH.AIN3,
            [
                OpCode(
                    op_code=0x02,
                    reg_address=ADCReg.REG_INPMUX.value,
                    op_mask=BitMask.LOW_NIBBLE.value,
                ),
                OpCode(
                    op_code=0x13,
                    reg_address=ADCReg.REG_ADC2MUX.value,
                    op_mask=BitMask.BYTE.value,
                )
            ],
        ),
        (
            CH.AIN0,
            CH.AIN1,
            None,
            CH.AIN3,
            [
                OpCode(
                    op_code=0x0,
                    reg_address=ADCReg.REG_INPMUX.value,
                    op_mask=BitMask.HIGH_NIBBLE.value,
                ),
                OpCode(
                    op_code=0x13,
                    reg_address=ADCReg.REG_ADC2MUX.value,
                    op_mask=BitMask.BYTE.value,
                )
            ],
        ),
        (
            CH.AIN0,
            CH.AIN1,
            CH.AIN2,
            None,
            [
                OpCode(
                    op_code=0x02,
                    reg_address=ADCReg.REG_INPMUX.value,
                    op_mask=BitMask.BYTE.value,
                ),
                OpCode(
                    op_code=0x10,
                    reg_address=ADCReg.REG_ADC2MUX.value,
                    op_mask=BitMask.HIGH_NIBBLE.value,
                )
            ],
        ),
        (
            None,
            CH.AIN1,
            None,
            CH.AIN3,
            [
                OpCode(
                    op_code=0x13,
                    reg_address=ADCReg.REG_ADC2MUX.value,
                    op_mask=BitMask.BYTE.value,
                )
            ],
        ),
        (
            CH.AIN0,
            None,
            CH.AIN2,
            None,
            [
                OpCode(
                    op_code=0x02,
                    reg_address=ADCReg.REG_INPMUX.value,
                    op_mask=BitMask.BYTE.value,
                ),
            ],
        ),
    ],
)
def test_get_channel_assign_opcodes(
    adc_1_mux_p,
    adc_2_mux_p,
    adc_1_mux_n,
    adc_2_mux_n,
    expected,
    adc_ops
):
    out = adc_ops.get_channel_assign_opcodes(adc_1_mux_p, adc_2_mux_p, adc_1_mux_n, adc_2_mux_n)
    assert list(out) == expected


# TODO: pytest.raises() does not see ChannelMappingError as equal to where it's defined
# the exception is raised in above test if channels are the same, but not here.
# def test_get_channel_assign_opcodes_raises(adc_ops):
#     with pytest.raises(ChannelMappingError):
#         adc_ops.get_channel_assign_opcodes(CH.AIN1.value, CH.AIN1.value)
