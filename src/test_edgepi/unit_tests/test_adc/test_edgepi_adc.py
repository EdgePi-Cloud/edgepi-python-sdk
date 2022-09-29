"""" Unit tests for edgepi_adc module """


import sys
from copy import deepcopy
from unittest import mock
from contextlib import nullcontext as does_not_raise

sys.modules["periphery"] = mock.MagicMock()

# pylint: disable=wrong-import-position, protected-access

import pytest
from edgepi.adc.edgepi_adc import ADCRegisterUpdateError, EdgePiADC
from edgepi.adc.adc_constants import ADC_NUM_REGS, ADCChannel as CH, ADCReg
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
    mocker.patch("edgepi.peripherals.i2c.I2C")
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
    "reg_updates, args, update_vals",
    [
        # set adc1 analog_in
        (
            {ADCReg.REG_INPMUX.value: 0x01, ADCReg.REG_ADC2MUX.value: 0x23},
            {"adc_1_analog_in": CH.AIN4},
            {ADCReg.REG_INPMUX.value: 0x41},
        ),
        # set adc2 analog_in
        (
            {ADCReg.REG_INPMUX.value: 0x01, ADCReg.REG_ADC2MUX.value: 0x23},
            {"adc_2_analog_in": CH.AIN5},
            {ADCReg.REG_ADC2MUX.value: 0x53},
        ),
        # set adc analog_in to same pin
        (
            {ADCReg.REG_INPMUX.value: 0x01, ADCReg.REG_ADC2MUX.value: 0x23},
            {"adc_2_analog_in": CH.AIN2},
            {ADCReg.REG_ADC2MUX.value: 0x23},
        ),
        # set both adc analog_in
        (
            {ADCReg.REG_INPMUX.value: 0x01, ADCReg.REG_ADC2MUX.value: 0x23},
            {"adc_1_analog_in": CH.AIN7, "adc_2_analog_in": CH.AIN5},
            {ADCReg.REG_INPMUX.value: 0x71, ADCReg.REG_ADC2MUX.value: 0x53},
        ),
        # set adc1 mux_n
        (
            {ADCReg.REG_INPMUX.value: 0x01, ADCReg.REG_ADC2MUX.value: 0x23},
            {"adc_1_mux_n": CH.AINCOM},
            {ADCReg.REG_INPMUX.value: 0x0A},
        ),
        # set adc2 mux_n
        (
            {ADCReg.REG_INPMUX.value: 0x01, ADCReg.REG_ADC2MUX.value: 0x23},
            {"adc_2_mux_n": CH.AIN5},
            {ADCReg.REG_ADC2MUX.value: 0x25},
        ),
        # set adc mux_n to same pin
        (
            {ADCReg.REG_INPMUX.value: 0x01, ADCReg.REG_ADC2MUX.value: 0x23},
            {"adc_2_mux_n": CH.AIN3},
            {ADCReg.REG_ADC2MUX.value: 0x23},
        ),
        # set both adc mux_n
        (
            {ADCReg.REG_INPMUX.value: 0x01, ADCReg.REG_ADC2MUX.value: 0x23},
            {"adc_1_mux_n": CH.AIN7, "adc_2_mux_n": CH.AIN5},
            {ADCReg.REG_INPMUX.value: 0x07, ADCReg.REG_ADC2MUX.value: 0x25},
        ),
        # set all mux pins
        (
            {ADCReg.REG_INPMUX.value: 0x01, ADCReg.REG_ADC2MUX.value: 0x23},
            {
                "adc_1_mux_n": CH.AIN7,
                "adc_2_mux_n": CH.AIN0,
                "adc_1_analog_in": CH.AIN6,
                "adc_2_analog_in": CH.AIN5,
            },
            {ADCReg.REG_INPMUX.value: 0x67, ADCReg.REG_ADC2MUX.value: 0x50},
        ),
        # set adc1 analog_in to pin in use on adc2
        (
            {ADCReg.REG_INPMUX.value: 0x01, ADCReg.REG_ADC2MUX.value: 0x23},
            {"adc_1_analog_in": CH.AIN2},
            {ADCReg.REG_INPMUX.value: 0x21},
        ),
        # set mux pins to same pin on different adc's
        (
            {ADCReg.REG_INPMUX.value: 0x01, ADCReg.REG_ADC2MUX.value: 0x23},
            {"adc_1_analog_in": CH.AIN2, "adc_2_analog_in": CH.AIN2},
            {ADCReg.REG_INPMUX.value: 0x21, ADCReg.REG_ADC2MUX.value: 0x23},
        ),
        # set adc1 analog_in to same pin as mux_n
        (
            {ADCReg.REG_INPMUX.value: 0x01, ADCReg.REG_ADC2MUX.value: 0x23},
            {"adc_1_analog_in": CH.AIN1},
            {ADCReg.REG_INPMUX.value: 0x11},
        ),
        # set adc2 analog_in to same pin as mux_n
        (
            {ADCReg.REG_INPMUX.value: 0x01, ADCReg.REG_ADC2MUX.value: 0x33},
            {"adc_2_analog_in": CH.AIN3},
            {ADCReg.REG_ADC2MUX.value: 0x33},
        ),
        # set adc 1 mux_n and mux_p to same pin
        (
            {ADCReg.REG_INPMUX.value: 0x01, ADCReg.REG_ADC2MUX.value: 0x23},
            {"adc_1_analog_in": CH.AIN2, "adc_1_mux_n": CH.AIN2},
            {ADCReg.REG_INPMUX.value: 0x22},
        ),
        # set adc 1 mux_n and mux_p to float mode
        (
            {ADCReg.REG_INPMUX.value: 0x01, ADCReg.REG_ADC2MUX.value: 0x23},
            {"adc_1_analog_in": CH.FLOAT, "adc_1_mux_n": CH.FLOAT},
            {ADCReg.REG_INPMUX.value: 0xFF},
        ),
    ],
)
def test_config(mocker, reg_updates, args, update_vals, adc):
    # modify default register values as needed
    adc_vals = deepcopy(adc_default_vals)
    for addx, reg_val in reg_updates.items():
        adc_vals[addx] = reg_val

    # mock RTD_EN as on
    mocker.patch("edgepi.adc.edgepi_adc.EdgePiADC._EdgePiADC__get_rtd_en_status", return_value=True)

    # mock each call to __read_register
    mocker.patch(
        "edgepi.adc.edgepi_adc.EdgePiADC._EdgePiADC__read_register",
        side_effect=[
            [reg_updates[ADCReg.REG_INPMUX.value]],
            [reg_updates[ADCReg.REG_ADC2MUX.value]],
            adc_vals,
            adc_vals,
        ],
    )

    # need to mock since cannot actually updated register values here
    mocker.patch("edgepi.adc.edgepi_adc.EdgePiADC._EdgePiADC__validate_updates", return_value=True)

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
            CH.AIN6,
            [
                OpCode(
                    op_code=0x07,
                    reg_address=ADCReg.REG_INPMUX.value,
                    op_mask=BitMask.LOW_NIBBLE.value,
                ),
                OpCode(
                    op_code=0x06,
                    reg_address=ADCReg.REG_ADC2MUX.value,
                    op_mask=BitMask.LOW_NIBBLE.value,
                ),
            ],
        ),
        (
            [0x12, 0x34],
            CH.AIN6,
            None,
            CH.AIN7,
            None,
            [
                OpCode(
                    op_code=0x67,
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
            CH.AIN4,
            [
                OpCode(
                    op_code=0x56,
                    reg_address=ADCReg.REG_INPMUX.value,
                    op_mask=BitMask.BYTE.value,
                ),
                OpCode(
                    op_code=0x74,
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
            CH.AIN7,
            [
                OpCode(
                    op_code=0x02,
                    reg_address=ADCReg.REG_INPMUX.value,
                    op_mask=BitMask.BYTE.value,
                ),
                OpCode(
                    op_code=0x07,
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
    # mock RTD_EN as on
    mocker.patch("edgepi.adc.edgepi_adc.EdgePiADC._EdgePiADC__get_rtd_en_status", return_value=True)
    mocker.patch(
        "edgepi.adc.edgepi_adc.EdgePiADC._EdgePiADC__read_register",
        side_effect=[[mux_map[0]], [mux_map[1]]],
    )
    out = adc._EdgePiADC__get_channel_assign_opcodes(
        adc_1_mux_p, adc_2_mux_p, adc_1_mux_n, adc_2_mux_n
    )
    assert out == expected


@pytest.mark.parametrize(
    "updated_regs, actual_regs, err",
    [
        (
            {ADCReg.REG_INTERFACE.value: {"value": 0x4}},
            {ADCReg.REG_INTERFACE.value: 0x4},
            does_not_raise(),
        ),
        (
            {
                ADCReg.REG_INTERFACE.value: {"value": 0x0},
                ADCReg.REG_INPMUX.value: {"value": 0x1},
                ADCReg.REG_MODE0.value: {"value": 0x2},
                ADCReg.REG_MODE1.value: {"value": 0x3},
            },
            {
                ADCReg.REG_INTERFACE.value: 0x0,
                ADCReg.REG_INPMUX.value: 0x1,
                ADCReg.REG_MODE0.value: 0x2,
                ADCReg.REG_MODE1.value: 0x3,
            },
            does_not_raise(),
        ),
        (
            {
                ADCReg.REG_INTERFACE.value: {"value": 0x0},
                ADCReg.REG_INPMUX.value: {"value": 0x1},
                ADCReg.REG_MODE0.value: {"value": 0x2},
                ADCReg.REG_MODE1.value: {"value": 0x3},
            },
            {
                ADCReg.REG_INTERFACE.value: 0x0,
                ADCReg.REG_INPMUX.value: 0x0,
                ADCReg.REG_MODE0.value: 0x2,
                ADCReg.REG_MODE1.value: 0x3,
            },
            pytest.raises(ADCRegisterUpdateError),
        ),
        (
            {
                ADCReg.REG_INTERFACE.value: {"value": 0x0},
                ADCReg.REG_INPMUX.value: {"value": 0x0},
                ADCReg.REG_MODE0.value: {"value": 0x2},
                ADCReg.REG_MODE1.value: {"value": 0x3},
            },
            {
                ADCReg.REG_INTERFACE.value: 0x0,
                ADCReg.REG_INPMUX.value: 0x1,
                ADCReg.REG_MODE0.value: 0x2,
                ADCReg.REG_MODE1.value: 0x3,
            },
            pytest.raises(ADCRegisterUpdateError),
        ),
    ],
)
def test_validate_updates(mocker, updated_regs, actual_regs, err, adc):
    mocker.patch(
        "edgepi.adc.edgepi_adc.EdgePiADC._EdgePiADC__read_registers_to_map",
        return_value=actual_regs,
    )
    with err:
        assert adc._EdgePiADC__validate_updates(updated_regs)
