"""" Unit tests for edgepi_adc module """


import sys
from unittest import mock

sys.modules["periphery"] = mock.MagicMock()

# pylint: disable=wrong-import-position, protected-access

import pytest
from edgepi.adc.edgepi_adc import EdgePiADC
from edgepi.adc.adc_constants import ADC_DEFAULT_VALS, ADC_NUM_REGS, ADCChannel as CH, ADCReg
from edgepi.reg_helper.reg_helper import OpCode, BitMask


@pytest.fixture(name="adc")
def fixture_adc(mocker):
    mocker.patch("edgepi.peripherals.spi.SPI")
    yield EdgePiADC()


def test_read_registers_to_map(mocker, adc):
    mocker.patch(
        "edgepi.peripherals.spi.SpiDevice.transfer", return_value=[0, 0] + ADC_DEFAULT_VALS
    )
    reg_dict = adc._EdgePiADC__read_registers_to_map()
    assert len(reg_dict) == ADC_NUM_REGS
    for i in range(ADC_NUM_REGS):
        assert reg_dict[i] == ADC_DEFAULT_VALS[i]


@pytest.mark.parametrize(
    "args, update_vals",
    [
        ({"adc_1_analog_in": CH.AIN3}, {ADCReg.REG_INPMUX.value: 0x01}),
        ({"adc_1_analog_in": CH.AIN4}, {ADCReg.REG_INPMUX.value: 0x21}),
    ],
)
def test_config(mocker, args, update_vals, adc):
    mocker.patch(
        "edgepi.peripherals.spi.SpiDevice.transfer", return_value=[0, 0] + ADC_DEFAULT_VALS
    )
    reg_values = adc._EdgePiADC__config(**args)

    for addx, entry in reg_values.items():
        if entry["is_changed"]:
            assert entry["value"] == update_vals[addx]
        else:
            assert entry["value"] == ADC_DEFAULT_VALS[addx]


@pytest.mark.parametrize(
    "mux_map, adc_1_mux_p, adc_2_mux_p, adc_1_mux_n, adc_2_mux_n, expected",
    [
        ([0x12, 0x34], None, None, None, None, []),
        (
            [0x12, 0x34],
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
            [0x12, 0x34],
            CH.AIN5,
            None,
            None,
            None,
            [
                OpCode(
                    op_code=0x50,
                    reg_address=ADCReg.REG_INPMUX.value,
                    op_mask=BitMask.HIGH_NIBBLE.value,
                )
            ],
        ),
        (
            [0x12, 0x34],
            None,
            CH.AIN5,
            None,
            None,
            [
                OpCode(
                    op_code=0x50,
                    reg_address=ADCReg.REG_ADC2MUX.value,
                    op_mask=BitMask.HIGH_NIBBLE.value,
                )
            ],
        ),
        (
            [0x12, 0x34],
            None,
            None,
            CH.AIN6,
            None,
            [
                OpCode(
                    op_code=0x06,
                    reg_address=ADCReg.REG_INPMUX.value,
                    op_mask=BitMask.LOW_NIBBLE.value,
                )
            ],
        ),
        (
            [0x12, 0x34],
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
            [0x12, 0x34],
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
            [0x12, 0x34],
            None,
            None,
            CH.AIN7,
            CH.AIN8,
            [
                OpCode(
                    op_code=0x07,
                    reg_address=ADCReg.REG_INPMUX.value,
                    op_mask=BitMask.LOW_NIBBLE.value,
                ),
                OpCode(
                    op_code=0x08,
                    reg_address=ADCReg.REG_ADC2MUX.value,
                    op_mask=BitMask.LOW_NIBBLE.value,
                ),
            ],
        ),
        (
            [0x12, 0x34],
            CH.AIN8,
            None,
            CH.AIN9,
            None,
            [
                OpCode(
                    op_code=0x89,
                    reg_address=ADCReg.REG_INPMUX.value,
                    op_mask=BitMask.BYTE.value,
                ),
            ],
        ),
        (
            [0x12, 0x34],
            None,
            CH.AIN4,
            None,
            CH.AIN3,
            [
                OpCode(
                    op_code=0x43,
                    reg_address=ADCReg.REG_ADC2MUX.value,
                    op_mask=BitMask.BYTE.value,
                ),
            ],
        ),
        (
            [0x12, 0x34],
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
                ),
            ],
        ),
        (
            [0x02, 0x13],
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
                ),
            ],
        ),
        (
            [0x12, 0x34],
            CH.AIN5,
            CH.AIN7,
            CH.AIN6,
            CH.AIN8,
            [
                OpCode(
                    op_code=0x56,
                    reg_address=ADCReg.REG_INPMUX.value,
                    op_mask=BitMask.BYTE.value,
                ),
                OpCode(
                    op_code=0x78,
                    reg_address=ADCReg.REG_ADC2MUX.value,
                    op_mask=BitMask.BYTE.value,
                ),
            ],
        ),
        (
            [0x12, 0x34],
            CH.AIN0,
            None,
            CH.AIN2,
            CH.AIN8,
            [
                OpCode(
                    op_code=0x02,
                    reg_address=ADCReg.REG_INPMUX.value,
                    op_mask=BitMask.BYTE.value,
                ),
                OpCode(
                    op_code=0x08,
                    reg_address=ADCReg.REG_ADC2MUX.value,
                    op_mask=BitMask.LOW_NIBBLE.value,
                ),
            ],
        ),
        (
            [0x12, 0x34],
            None,
            CH.AIN2,
            CH.AIN3,
            CH.AINCOM,
            [
                OpCode(
                    op_code=0x03,
                    reg_address=ADCReg.REG_INPMUX.value,
                    op_mask=BitMask.LOW_NIBBLE.value,
                ),
                OpCode(
                    op_code=0x2A,
                    reg_address=ADCReg.REG_ADC2MUX.value,
                    op_mask=BitMask.BYTE.value,
                ),
            ],
        ),
        (
            [0x12, 0x34],
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
                ),
            ],
        ),
        (
            [0x12, 0x34],
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
                ),
            ],
        ),
        (
            [0x12, 0x34],
            None,
            CH.AIN4,
            None,
            CH.AIN3,
            [
                OpCode(
                    op_code=0x43,
                    reg_address=ADCReg.REG_ADC2MUX.value,
                    op_mask=BitMask.BYTE.value,
                )
            ],
        ),
    ],
)
def test_get_channel_assign_opcodes(
    mocker, mux_map, adc_1_mux_p, adc_2_mux_p, adc_1_mux_n, adc_2_mux_n, expected, adc
):
    mocker.patch("edgepi.peripherals.spi.SpiDevice.transfer", side_effect=[[0, 0, mux_map[0]], [0, 0, mux_map[1]]])
    out = adc._EdgePiADC__get_channel_assign_opcodes(
        adc_1_mux_p, adc_2_mux_p, adc_1_mux_n, adc_2_mux_n
    )
    assert out == expected

# TODO: pytest.raises() does not see ChannelMappingError as equal to where it's defined
# the exception is raised in above test if channels are the same, but not here.
# def test_get_channel_assign_opcodes_raises(adc_ops):
#     with pytest.raises(ChannelMappingError):
#         adc_ops.get_channel_assign_opcodes(CH.AIN1.value, CH.AIN1.value)
