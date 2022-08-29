"""" Unit tests for edgepi_adc module """


import sys
from copy import deepcopy
from unittest import mock
from unittest.mock import call
from contextlib import nullcontext as does_not_raise

sys.modules["periphery"] = mock.MagicMock()

# pylint: disable=wrong-import-position, protected-access

import pytest
from edgepi.adc.edgepi_adc import EdgePiADC
from edgepi.adc.adc_multiplexers import ChannelMappingError
from edgepi.adc.adc_constants import ADC_NUM_REGS, ADCChannel as CH, ADCNum, ADCReg
from edgepi.reg_helper.reg_helper import OpCode, BitMask

adc_default_vals = [
    0,
    0x11,
    0x5,
    0,
    0x80,
    0x04,
    0x01,
    0,
    0,
    0,
    0,
    0,
    0x40,
    0xBB,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0x01,
    0,
    0,
    0,
    0x40,
]


@pytest.fixture(name="adc")
def fixture_adc(mocker):
    mocker.patch("edgepi.peripherals.spi.SPI")
    mocker.patch("edgepi.adc.edgepi_adc.EdgePiADC._EdgePiADC__write_register")
    yield EdgePiADC()


def test_read_registers_to_map(mocker, adc):
    mocker.patch(
        "edgepi.peripherals.spi.SpiDevice.transfer",
        return_value=[0, 0] + deepcopy(adc_default_vals),
    )
    reg_dict = adc._EdgePiADC__read_registers_to_map()
    assert len(reg_dict) == ADC_NUM_REGS
    for i in range(ADC_NUM_REGS):
        assert reg_dict[i] == adc_default_vals[i]


@pytest.mark.parametrize(
    "reg_updates, args, update_vals, err",
    [
        # set adc1 analog_in
        (
            {ADCReg.REG_INPMUX.value: 0x01, ADCReg.REG_ADC2MUX.value: 0x23},
            {"adc_1_analog_in": CH.AIN4},
            {ADCReg.REG_INPMUX.value: 0x41},
            does_not_raise(),
        ),
        # set adc2 analog_in
        (
            {ADCReg.REG_INPMUX.value: 0x01, ADCReg.REG_ADC2MUX.value: 0x23},
            {"adc_2_analog_in": CH.AIN5},
            {ADCReg.REG_ADC2MUX.value: 0x53},
            does_not_raise(),
        ),
        # set adc analog_in to same pin
        (
            {ADCReg.REG_INPMUX.value: 0x01, ADCReg.REG_ADC2MUX.value: 0x23},
            {"adc_2_analog_in": CH.AIN2},
            {ADCReg.REG_ADC2MUX.value: 0x23},
            does_not_raise(),
        ),
        # set both adc analog_in
        (
            {ADCReg.REG_INPMUX.value: 0x01, ADCReg.REG_ADC2MUX.value: 0x23},
            {"adc_1_analog_in": CH.AIN9, "adc_2_analog_in": CH.AIN5},
            {ADCReg.REG_INPMUX.value: 0x91, ADCReg.REG_ADC2MUX.value: 0x53},
            does_not_raise(),
        ),
        # set adc1 mux_n
        (
            {ADCReg.REG_INPMUX.value: 0x01, ADCReg.REG_ADC2MUX.value: 0x23},
            {"adc_1_mux_n": CH.AINCOM},
            {ADCReg.REG_INPMUX.value: 0x0A},
            does_not_raise(),
        ),
        # set adc2 mux_n
        (
            {ADCReg.REG_INPMUX.value: 0x01, ADCReg.REG_ADC2MUX.value: 0x23},
            {"adc_2_mux_n": CH.AIN5},
            {ADCReg.REG_ADC2MUX.value: 0x25},
            does_not_raise(),
        ),
        # set adc mux_n to same pin
        (
            {ADCReg.REG_INPMUX.value: 0x01, ADCReg.REG_ADC2MUX.value: 0x23},
            {"adc_2_mux_n": CH.AIN3},
            {ADCReg.REG_ADC2MUX.value: 0x23},
            does_not_raise(),
        ),
        # set both adc mux_n
        (
            {ADCReg.REG_INPMUX.value: 0x01, ADCReg.REG_ADC2MUX.value: 0x23},
            {"adc_1_mux_n": CH.AIN9, "adc_2_mux_n": CH.AIN5},
            {ADCReg.REG_INPMUX.value: 0x09, ADCReg.REG_ADC2MUX.value: 0x25},
            does_not_raise(),
        ),
        # set all mux pins
        (
            {ADCReg.REG_INPMUX.value: 0x01, ADCReg.REG_ADC2MUX.value: 0x23},
            {
                "adc_1_mux_n": CH.AIN9,
                "adc_2_mux_n": CH.AIN0,
                "adc_1_analog_in": CH.AIN8,
                "adc_2_analog_in": CH.AIN5,
            },
            {ADCReg.REG_INPMUX.value: 0x89, ADCReg.REG_ADC2MUX.value: 0x50},
            does_not_raise(),
        ),
        # set adc1 analog_in to pin in use on adc2
        (
            {ADCReg.REG_INPMUX.value: 0x01, ADCReg.REG_ADC2MUX.value: 0x23},
            {"adc_1_analog_in": CH.AIN2},
            {ADCReg.REG_INPMUX.value: 0x21},
            does_not_raise(),
        ),
        # set mux pins to same pin on different adc's
        (
            {ADCReg.REG_INPMUX.value: 0x01, ADCReg.REG_ADC2MUX.value: 0x23},
            {"adc_1_analog_in": CH.AIN2, "adc_2_analog_in": CH.AIN2},
            {ADCReg.REG_INPMUX.value: 0x21, ADCReg.REG_ADC2MUX.value: 0x23},
            does_not_raise(),
        ),
        # set adc1 analog_in to same pin as mux_n
        (
            {ADCReg.REG_INPMUX.value: 0x01, ADCReg.REG_ADC2MUX.value: 0x23},
            {"adc_1_analog_in": CH.AIN1},
            {ADCReg.REG_INPMUX.value: 0x11},
            pytest.raises(ChannelMappingError),
        ),
        # set adc2 analog_in to same pin as mux_n
        (
            {ADCReg.REG_INPMUX.value: 0x01, ADCReg.REG_ADC2MUX.value: 0x23},
            {"adc_2_analog_in": CH.AIN3},
            {ADCReg.REG_INPMUX.value: 0x33},
            pytest.raises(ChannelMappingError),
        ),
        # set adc 1 mux_n and mux_p to same pin
        (
            {ADCReg.REG_INPMUX.value: 0x01, ADCReg.REG_ADC2MUX.value: 0x23},
            {"adc_1_analog_in": CH.AIN2, "adc_1_mux_n": CH.AIN2},
            {ADCReg.REG_INPMUX.value: 0x22},
            pytest.raises(ChannelMappingError),
        ),
        # set adc 1 mux_n and mux_p to float mode
        (
            {ADCReg.REG_INPMUX.value: 0x01, ADCReg.REG_ADC2MUX.value: 0x23},
            {"adc_1_analog_in": CH.FLOAT, "adc_1_mux_n": CH.FLOAT},
            {ADCReg.REG_INPMUX.value: 0xFF},
            does_not_raise(),
        ),
    ],
)
def test_config(mocker, reg_updates, args, update_vals, err, adc):
    # modify default register values as needed
    adc_vals = deepcopy(adc_default_vals)
    for addx, reg_val in reg_updates.items():
        adc_vals[addx] = reg_val

    # mock each call to __read_register
    mocker.patch(
        "edgepi.adc.edgepi_adc.EdgePiADC._EdgePiADC__read_register",
        side_effect=[
            [reg_updates[ADCReg.REG_INPMUX.value]],
            [reg_updates[ADCReg.REG_ADC2MUX.value]],
            adc_vals,
        ],
    )

    with err:
        reg_values = adc._EdgePiADC__config(**args)

        for addx, entry in reg_values.items():
            if entry["is_changed"]:
                assert entry["value"] == update_vals[addx]
            else:
                assert entry["value"] == adc_vals[addx]


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
    mocker.patch(
        "edgepi.adc.edgepi_adc.EdgePiADC._EdgePiADC__read_register",
        side_effect=[[mux_map[0]], [mux_map[1]]],
    )
    out = adc._EdgePiADC__get_channel_assign_opcodes(
        adc_1_mux_p, adc_2_mux_p, adc_1_mux_n, adc_2_mux_n
    )
    assert out == expected


@pytest.mark.parametrize(
    "mode0_val, expected",
    [
        (0x00, False),
        (0x40, True),
        (0b11100000, True),
        (0b10100000, False),
    ],
)
def test_is_in_pulse_mode(mocker, mode0_val, expected, adc):
    mocker.patch(
        "edgepi.adc.edgepi_adc.EdgePiADC._EdgePiADC__read_register", return_value=[mode0_val]
    )
    assert adc._EdgePiADC__is_in_pulse_mode() == expected


# TODO: when ADC2 functionality is added, use this format instead
# @pytest.mark.parametrize(
#     "adc_num, adc1_pulse_mode, calls",
#     [
#         (ADCNum.ADC_1, False, [call([ADCNum.ADC_1.value.read_cmd])]),
#         (ADCNum.ADC_2, False, [call([ADCNum.ADC_2.value.read_cmd])]),
#         (ADCNum.ADC_2, True, [call([ADCNum.ADC_2.value.read_cmd])]),
#         (
#             ADCNum.ADC_1,
#             True,
#             [call([ADCNum.ADC_1.value.start_cmd]), call([ADCNum.ADC_1.value.read_cmd])],
#         ),
#     ],
# )
# def test_read_voltage(mocker, adc_num, adc1_pulse_mode, calls, adc):
#     transfer = mocker.patch("edgepi.adc.adc_multiplexers.validate_channels_set")
#     mocker.patch("edgepi.adc.edgepi_adc.EdgePiADC._EdgePiADC__read_register")
#     mocker.patch(
#         "edgepi.adc.edgepi_adc.EdgePiADC._EdgePiADC__is_in_pulse_mode", return_value=adc1_pulse_mode
#     )
#     transfer = mocker.patch("edgepi.peripherals.spi.SpiDevice.transfer")
#     adc.read_voltage(adc_num)
#     transfer.assert_has_calls(calls)
