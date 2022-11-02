"""" Unit tests for edgepi_adc module """


import sys
from copy import deepcopy
from unittest import mock
from contextlib import nullcontext as does_not_raise

sys.modules["periphery"] = mock.MagicMock()

# pylint: disable=wrong-import-position, protected-access

import pytest
from edgepi.adc.edgepi_adc import ADCRegisterUpdateError, EdgePiADC, RTDEnabledError
from edgepi.adc.adc_constants import (
    ADC_NUM_REGS,
    ADCReg,
    ADCChannel as CH,
    ADCReferenceSwitching,
    ConvMode,
    ADCNum,
    DiffMode,
    IDACMUX,
    IDACMAG,
    REFMUX
)
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
    # mock RTD as off by default, mock as on if needed
    mocker.patch(
        "edgepi.adc.edgepi_adc.EdgePiADC._EdgePiADC__get_rtd_en_status", return_value=False
        )
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
        # set idac_1_mux and idac_2_mux
        (
            {ADCReg.REG_IDACMUX.value: 0xBB},
            {"idac_1_mux": IDACMUX.IDAC1_AIN0, "idac_2_mux": IDACMUX.IDAC2_AIN0},
            {ADCReg.REG_IDACMUX.value: 0x00},
        ),
        (
            {ADCReg.REG_IDACMUX.value: 0xBB},
            {"idac_1_mux": IDACMUX.IDAC1_AIN1, "idac_2_mux": IDACMUX.IDAC2_AIN1},
            {ADCReg.REG_IDACMUX.value: 0x11},
        ),
        (
            {ADCReg.REG_IDACMUX.value: 0xBB},
            {"idac_1_mux": IDACMUX.IDAC1_AIN2, "idac_2_mux": IDACMUX.IDAC2_AIN2},
            {ADCReg.REG_IDACMUX.value: 0x22},
        ),
        (
            {ADCReg.REG_IDACMUX.value: 0xBB},
            {"idac_1_mux": IDACMUX.IDAC1_AIN3, "idac_2_mux": IDACMUX.IDAC2_AIN3},
            {ADCReg.REG_IDACMUX.value: 0x33},
        ),
        (
            {ADCReg.REG_IDACMUX.value: 0xBB},
            {"idac_1_mux": IDACMUX.IDAC1_AIN4, "idac_2_mux": IDACMUX.IDAC2_AIN4},
            {ADCReg.REG_IDACMUX.value: 0x44},
        ),
        (
            {ADCReg.REG_IDACMUX.value: 0xBB},
            {"idac_1_mux": IDACMUX.IDAC1_AIN5, "idac_2_mux": IDACMUX.IDAC2_AIN5},
            {ADCReg.REG_IDACMUX.value: 0x55},
        ),
        (
            {ADCReg.REG_IDACMUX.value: 0xBB},
            {"idac_1_mux": IDACMUX.IDAC1_AIN6, "idac_2_mux": IDACMUX.IDAC2_AIN6},
            {ADCReg.REG_IDACMUX.value: 0x66},
        ),
        (
            {ADCReg.REG_IDACMUX.value: 0xBB},
            {"idac_1_mux": IDACMUX.IDAC1_AIN7, "idac_2_mux": IDACMUX.IDAC2_AIN7},
            {ADCReg.REG_IDACMUX.value: 0x77},
        ),
        (
            {ADCReg.REG_IDACMUX.value: 0xBB},
            {"idac_1_mux": IDACMUX.IDAC1_AIN8, "idac_2_mux": IDACMUX.IDAC2_AIN8},
            {ADCReg.REG_IDACMUX.value: 0x88},
        ),
        (
            {ADCReg.REG_IDACMUX.value: 0xBB},
            {"idac_1_mux": IDACMUX.IDAC1_AIN9, "idac_2_mux": IDACMUX.IDAC2_AIN9},
            {ADCReg.REG_IDACMUX.value: 0x99},
        ),
        (
            {ADCReg.REG_IDACMUX.value: 0xBB},
            {"idac_1_mux": IDACMUX.IDAC1_AIN9, "idac_2_mux": IDACMUX.IDAC2_AIN9},
            {ADCReg.REG_IDACMUX.value: 0x99},
        ),
        (
            {ADCReg.REG_IDACMUX.value: 0xBB},
            {"idac_1_mux": IDACMUX.IDAC1_AINCOM, "idac_2_mux": IDACMUX.IDAC2_AINCOM},
            {ADCReg.REG_IDACMUX.value: 0xAA},
        ),
        (
            {ADCReg.REG_IDACMUX.value: 0x00},
            {"idac_1_mux": IDACMUX.IDAC1_NO_CONNECT, "idac_2_mux": IDACMUX.IDAC2_NO_CONNECT},
            {ADCReg.REG_IDACMUX.value: 0xBB},
        ),
        # set idac_1_mag and idac_2_mag
        (
            {ADCReg.REG_IDACMAG.value: 0x00},
            {"idac_1_mag": IDACMAG.IDAC1_50, "idac_2_mag": IDACMAG.IDAC2_50},
            {ADCReg.REG_IDACMAG.value: 0x11},
        ),
        (
            {ADCReg.REG_IDACMAG.value: 0x00},
            {"idac_1_mag": IDACMAG.IDAC1_100, "idac_2_mag": IDACMAG.IDAC2_100},
            {ADCReg.REG_IDACMAG.value: 0x22},
        ),
        (
            {ADCReg.REG_IDACMAG.value: 0x00},
            {"idac_1_mag": IDACMAG.IDAC1_250, "idac_2_mag": IDACMAG.IDAC2_250},
            {ADCReg.REG_IDACMAG.value: 0x33},
        ),
        (
            {ADCReg.REG_IDACMAG.value: 0x00},
            {"idac_1_mag": IDACMAG.IDAC1_500, "idac_2_mag": IDACMAG.IDAC2_500},
            {ADCReg.REG_IDACMAG.value: 0x44},
        ),
        (
            {ADCReg.REG_IDACMAG.value: 0x00},
            {"idac_1_mag": IDACMAG.IDAC1_750, "idac_2_mag": IDACMAG.IDAC2_750},
            {ADCReg.REG_IDACMAG.value: 0x55},
        ),
        (
            {ADCReg.REG_IDACMAG.value: 0x00},
            {"idac_1_mag": IDACMAG.IDAC1_1000, "idac_2_mag": IDACMAG.IDAC2_1000},
            {ADCReg.REG_IDACMAG.value: 0x66},
        ),
        (
            {ADCReg.REG_IDACMAG.value: 0x00},
            {"idac_1_mag": IDACMAG.IDAC1_1500, "idac_2_mag": IDACMAG.IDAC2_1500},
            {ADCReg.REG_IDACMAG.value: 0x77},
        ),
        (
            {ADCReg.REG_IDACMAG.value: 0x00},
            {"idac_1_mag": IDACMAG.IDAC1_2000, "idac_2_mag": IDACMAG.IDAC2_2000},
            {ADCReg.REG_IDACMAG.value: 0x88},
        ),
        (
            {ADCReg.REG_IDACMAG.value: 0x00},
            {"idac_1_mag": IDACMAG.IDAC1_2500, "idac_2_mag": IDACMAG.IDAC2_2500},
            {ADCReg.REG_IDACMAG.value: 0x99},
        ),
        (
            {ADCReg.REG_IDACMAG.value: 0x00},
            {"idac_1_mag": IDACMAG.IDAC1_3000, "idac_2_mag": IDACMAG.IDAC2_3000},
            {ADCReg.REG_IDACMAG.value: 0xAA},
        ),
        (
            {ADCReg.REG_IDACMAG.value: 0xAA},
            {"idac_1_mag": IDACMAG.IDAC1_OFF, "idac_2_mag": IDACMAG.IDAC2_OFF},
            {ADCReg.REG_IDACMAG.value: 0x00},
        ),
    ],
)
def test_config(mocker, reg_updates, args, update_vals, adc):
    # modify default register values as needed
    adc_vals = deepcopy(adc_default_vals)
    for addx, reg_val in reg_updates.items():
        adc_vals[addx] = reg_val

    # mock RTD_EN as off
    mocker.patch(
        "edgepi.adc.edgepi_adc.EdgePiADC._EdgePiADC__get_rtd_en_status", return_value=False
    )

    # mock each call to __read_register
    mocker.patch(
        "edgepi.adc.edgepi_adc.EdgePiADC._EdgePiADC__read_register",
        side_effect=[
            adc_vals,
        ],
    )

    # need to mock since cannot actually check updated register values here
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
    # mock RTD_EN as off
    mocker.patch(
        "edgepi.adc.edgepi_adc.EdgePiADC._EdgePiADC__get_rtd_en_status", return_value=False
    )
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

@pytest.mark.parametrize("reference_config, pin_name",
                        [(ADCReferenceSwitching.GND_SW1.value, ["GNDSW_IN1", "GNDSW_IN2"]),
                         (ADCReferenceSwitching.GND_SW2.value, ["GNDSW_IN2", "GNDSW_IN1"]),
                         (ADCReferenceSwitching.GND_SW_BOTH.value, ["GNDSW_IN1", "GNDSW_IN2"]),
                         (ADCReferenceSwitching.GND_SW_NONE.value, ["GNDSW_IN1", "GNDSW_IN2"])])
def test_set_adc_reference(mocker,reference_config, pin_name, adc):
    set_pin = mocker.patch("edgepi.gpio.edgepi_gpio.EdgePiGPIO.set_expander_pin")
    clear_pin = mocker.patch("edgepi.gpio.edgepi_gpio.EdgePiGPIO.clear_expander_pin")
    adc.set_adc_reference(reference_config)
    if reference_config in [1, 2]:
        set_pin.assert_called_once_with(pin_name[0])
        clear_pin.assert_called_once_with(pin_name[1])
    elif reference_config == 3:
        set_pin.assert_has_calls([mock.call(pin_name[0]), mock.call(pin_name[1])])
    elif reference_config == 0:
        clear_pin.assert_has_calls([mock.call(pin_name[0]), mock.call(pin_name[1])])


@pytest.mark.parametrize('updates, rtd_on, err',
    [
        # RTD related setting: RTD ON (note: values are irrelevant, only key matters)
        ({'adc_1_analog_in': CH.AIN0}, True, pytest.raises(RTDEnabledError)),
        ({'adc_1_mux_n': CH.AIN0}, True, pytest.raises(RTDEnabledError)),
        ({'idac_1_mux': 0}, True, pytest.raises(RTDEnabledError)),
        ({'idac_2_mux': 0}, True, pytest.raises(RTDEnabledError)),
        ({'idac_1_mag': 0}, True, pytest.raises(RTDEnabledError)),
        ({'idac_2_mag': 0}, True, pytest.raises(RTDEnabledError)),
        ({'pos_ref_inp': 0}, True, pytest.raises(RTDEnabledError)),
        ({'neg_ref_inp': 0}, True, pytest.raises(RTDEnabledError)),
        # RTD related setting: RTD OFF
        ({'adc_1_analog_in': CH.AIN0}, False, does_not_raise()),
        ({'adc_1_mux_n': CH.AIN0}, False, does_not_raise()),
        ({'idac_1_mux': 0}, False, does_not_raise()),
        ({'idac_2_mux': 0}, False, does_not_raise()),
        ({'idac_1_mag': 0}, False, does_not_raise()),
        ({'idac_2_mag': 0}, False, does_not_raise()),
        ({'pos_ref_inp': 0}, False, does_not_raise()),
        ({'neg_ref_inp': 0}, False, does_not_raise()),
        # non-RTD related setting: RTD ON
        ({'adc_1_data_rate': ConvMode.PULSE}, True, does_not_raise()),
        ({'adc_2_data_rate': 0}, True, does_not_raise()),
        ({'conversion_mode': 0}, True, does_not_raise()),
        # non-RTD related setting: RTD OFF
        ({'adc_1_data_rate': ConvMode.PULSE}, False, does_not_raise()),
        ({'adc_2_data_rate': 0}, True, does_not_raise()),
        ({'conversion_mode': 0}, True, does_not_raise()),
    ]
)
def test_validate_no_rtd_conflict(mocker, updates, rtd_on, err, adc):
    mocker.patch(
        "edgepi.adc.edgepi_adc.EdgePiADC._EdgePiADC__get_rtd_en_status", return_value=rtd_on
    )
    with err:
        adc._EdgePiADC__validate_no_rtd_conflict(updates)


@pytest.mark.parametrize('adc_num, diff_mode, config_calls', 
    [
        (ADCNum.ADC_1, DiffMode.DIFF_1, {'adc_1_analog_in': CH.AIN0, 'adc_1_mux_n': CH.AIN1}),
        (ADCNum.ADC_2, DiffMode.DIFF_1, {'adc_2_analog_in': CH.AIN0, 'adc_2_mux_n': CH.AIN1}),
        (ADCNum.ADC_1, DiffMode.DIFF_2, {'adc_1_analog_in': CH.AIN2, 'adc_1_mux_n': CH.AIN3}),
        (ADCNum.ADC_2, DiffMode.DIFF_2, {'adc_2_analog_in': CH.AIN2, 'adc_2_mux_n': CH.AIN3}),
        (ADCNum.ADC_1, DiffMode.DIFF_3, {'adc_1_analog_in': CH.AIN4, 'adc_1_mux_n': CH.AIN5}),
        (ADCNum.ADC_2, DiffMode.DIFF_3, {'adc_2_analog_in': CH.AIN4, 'adc_2_mux_n': CH.AIN5}),
        (ADCNum.ADC_1, DiffMode.DIFF_4, {'adc_1_analog_in': CH.AIN6, 'adc_1_mux_n': CH.AIN7}),
        (ADCNum.ADC_2, DiffMode.DIFF_4, {'adc_2_analog_in': CH.AIN6, 'adc_2_mux_n': CH.AIN7}),
        (ADCNum.ADC_1, DiffMode.DIFF_OFF, {'adc_1_analog_in': CH.AIN0, 'adc_1_mux_n': CH.AINCOM}),
        (ADCNum.ADC_2, DiffMode.DIFF_OFF, {'adc_2_analog_in': CH.AIN0, 'adc_2_mux_n': CH.AINCOM}),
    ]
)
def test_select_differential(mocker, adc_num, diff_mode, config_calls, adc):
    config = mocker.patch(
        "edgepi.adc.edgepi_adc.EdgePiADC._EdgePiADC__config"
    )
    adc.select_differential(adc_num, diff_mode)
    config.assert_called_once_with(**config_calls)
