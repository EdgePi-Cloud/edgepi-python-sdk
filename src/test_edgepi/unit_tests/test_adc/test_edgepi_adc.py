"""" Unit tests for edgepi_adc module """
# pylint: disable=too-many-lines

import sys
from copy import deepcopy
from unittest import mock
from contextlib import nullcontext as does_not_raise

sys.modules["periphery"] = mock.MagicMock()

# pylint: disable=wrong-import-position, protected-access

import pytest
from edgepi.adc.edgepi_adc import EdgePiADC
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
    REFMUX,
    RTDModes,
    ADC1RtdConfig,
    ADC2RtdConfig,
    AnalogIn,
    ADC1DataRate,
    ADC2DataRate,
    FilterMode,
    ADC1PGA,
)
from edgepi.reg_helper.reg_helper import OpCode, BitMask
from edgepi.calibration.calibration_constants import CalibParam
from edgepi.adc.edgepi_adc import ADCState
from edgepi.adc.adc_exceptions import (
    ADCRegisterUpdateError,
    RTDEnabledError,
    InvalidDifferentialPairError
)

from edgepi.eeprom.edgepi_eeprom_data import EepromDataClass
from edgepi.eeprom.protobuf_assets.generated_pb2 import edgepi_module_pb2
from test_edgepi.unit_tests.test_eeprom.read_serialized import read_binfile

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
    mocker.patch(
        "edgepi.adc.edgepi_adc.EdgePiADC._EdgePiADC__read_register",
        return_value=deepcopy(adc_default_vals)
    )
    # mock RTD as off by default, mock as on if needed
    mocker.patch("edgepi.adc.edgepi_adc.EdgePiADC._EdgePiADC__is_rtd_on", return_value=False)
    mocker.patch("edgepi.adc.edgepi_adc.EdgePiADC._EdgePiADC__get_rtd_state",
                 return_value=[RTDModes.RTD_OFF, None])
    mocker.patch("edgepi.adc.edgepi_adc.EdgePiADC._EdgePiADC__validate_updates", return_value=True)
    # pylint: disable=no-member
    eelayout= edgepi_module_pb2.EepromData()
    eelayout.ParseFromString(read_binfile())
    mocker.patch("edgepi.dac.edgepi_dac.EdgePiEEPROM.read_edgepi_data",
                  return_value = EepromDataClass.extract_eeprom_data(eelayout))
    mocker.patch("edgepi.adc.edgepi_adc.EdgePiGPIO")
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
            {"adc_1_ch": CH.AIN4},
            {ADCReg.REG_INPMUX.value: 0x4A},
        ),
        # set adc2 analog_in
        (
            {ADCReg.REG_INPMUX.value: 0x01, ADCReg.REG_ADC2MUX.value: 0x23},
            {"adc_2_ch": CH.AIN5},
            {ADCReg.REG_ADC2MUX.value: 0x5A},
        ),
        # set adc analog_in to same pin
        (
            {ADCReg.REG_INPMUX.value: 0x01, ADCReg.REG_ADC2MUX.value: 0x23},
            {"adc_2_ch": CH.AIN2},
            {ADCReg.REG_ADC2MUX.value: 0x2A},
        ),
        # set both adc analog_in
        (
            {ADCReg.REG_INPMUX.value: 0x01, ADCReg.REG_ADC2MUX.value: 0x23},
            {"adc_1_ch": CH.AIN7, "adc_2_ch": CH.AIN5},
            {ADCReg.REG_INPMUX.value: 0x7A, ADCReg.REG_ADC2MUX.value: 0x5A},
        ),
        # set all mux pins
        (
            {ADCReg.REG_INPMUX.value: 0x01, ADCReg.REG_ADC2MUX.value: 0x23},
            {
                "adc_1_mux_n": CH.AIN7,
                "adc_2_mux_n": CH.AIN0,
                "adc_1_ch": CH.AIN6,
                "adc_2_ch": CH.AIN5,
            },
            {ADCReg.REG_INPMUX.value: 0x67, ADCReg.REG_ADC2MUX.value: 0x50},
        ),
        # set adc1 analog_in to pin in use on adc2
        (
            {ADCReg.REG_INPMUX.value: 0x01, ADCReg.REG_ADC2MUX.value: 0x23},
            {"adc_1_ch": CH.AIN2},
            {ADCReg.REG_INPMUX.value: 0x2A},
        ),
        # set mux pins to same pin on different adc's
        (
            {ADCReg.REG_INPMUX.value: 0x01, ADCReg.REG_ADC2MUX.value: 0x23},
            {"adc_1_ch": CH.AIN2, "adc_2_ch": CH.AIN2},
            {ADCReg.REG_INPMUX.value: 0x2A, ADCReg.REG_ADC2MUX.value: 0x2A},
        ),
        # set adc1 analog_in to same pin as mux_n
        (
            {ADCReg.REG_INPMUX.value: 0x01, ADCReg.REG_ADC2MUX.value: 0x23},
            {"adc_1_ch": CH.AIN1},
            {ADCReg.REG_INPMUX.value: 0x1A},
        ),
        # set adc2 analog_in to same pin as mux_n
        (
            {ADCReg.REG_INPMUX.value: 0x01, ADCReg.REG_ADC2MUX.value: 0x33},
            {"adc_2_ch": CH.AIN3},
            {ADCReg.REG_ADC2MUX.value: 0x3A},
        ),
        # set adc 1 mux_n and mux_p to same pin
        (
            {ADCReg.REG_INPMUX.value: 0x01, ADCReg.REG_ADC2MUX.value: 0x23},
            {"adc_1_ch": CH.AIN2, "adc_1_mux_n": CH.AIN2},
            {ADCReg.REG_INPMUX.value: 0x22},
        ),
        # set adc 1 mux_n and mux_p to float mode
        (
            {ADCReg.REG_INPMUX.value: 0x01, ADCReg.REG_ADC2MUX.value: 0x23},
            {"adc_1_ch": CH.FLOAT, "adc_1_mux_n": CH.FLOAT},
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
        # set pos_ref_inp and neg_ref_inp
        (
            {ADCReg.REG_REFMUX.value: 0x3F},
            {"pos_ref_inp": REFMUX.POS_REF_INT_2P5, "neg_ref_inp": REFMUX.NEG_REF_INT_2P5},
            {ADCReg.REG_REFMUX.value: 0x0},
        ),
        (
            {ADCReg.REG_REFMUX.value: 0xFF},
            {"pos_ref_inp": REFMUX.POS_REF_INT_2P5, "neg_ref_inp": REFMUX.NEG_REF_INT_2P5},
            {ADCReg.REG_REFMUX.value: 0xC0},
        ),
        (
            {ADCReg.REG_REFMUX.value: 0x3F},
            {"pos_ref_inp": REFMUX.POS_REF_EXT_AIN0, "neg_ref_inp": REFMUX.NEG_REF_EXT_AIN1},
            {ADCReg.REG_REFMUX.value: 0b00001001},
        ),
        (
            {ADCReg.REG_REFMUX.value: 0x3F},
            {"pos_ref_inp": REFMUX.POS_REF_EXT_AIN2, "neg_ref_inp": REFMUX.NEG_REF_EXT_AIN3},
            {ADCReg.REG_REFMUX.value: 0b00010010},
        ),
        (
            {ADCReg.REG_REFMUX.value: 0x3F},
            {"pos_ref_inp": REFMUX.POS_REF_EXT_AIN4, "neg_ref_inp": REFMUX.NEG_REF_EXT_AIN5},
            {ADCReg.REG_REFMUX.value: 0b00011011},
        ),
        (
            {ADCReg.REG_REFMUX.value: 0x3F},
            {"pos_ref_inp": REFMUX.POS_REF_INT_VAVDD, "neg_ref_inp": REFMUX.NEG_REF_INT_VAVSS},
            {ADCReg.REG_REFMUX.value: 0b00100100},
        ),
        (
            {ADCReg.REG_MODE2.value: 0x0F},
            {"adc_1_pga": ADC1PGA.BYPASSED},
            {ADCReg.REG_MODE2.value: 0x8F}
        ),
        (
            {ADCReg.REG_MODE2.value: 0x8F},
            {"adc_1_pga": ADC1PGA.ENABLED},
            {ADCReg.REG_MODE2.value: 0x0F}
        ),
    ],
)
def test_config(mocker, reg_updates, args, update_vals, adc):
    # modify default register values as needed
    adc_vals = deepcopy(adc_default_vals)
    for addx, reg_val in reg_updates.items():
        adc_vals[addx] = reg_val

    # mock each call to __read_register
    mocker.patch("edgepi.adc.edgepi_adc.EdgePiADC._EdgePiADC__read_register", return_value=adc_vals)
    reg_values = adc._EdgePiADC__config(**args)

    for addx, entry in reg_values.items():
        if entry["is_changed"]:
            assert entry["value"] == update_vals[addx]
        else:
            assert entry["value"] == adc_vals[addx]


@pytest.mark.parametrize(
    "args",
    [
        # set adc1 mux_n w/o mux_p
        (
            {"adc_1_mux_n": CH.AINCOM}
        ),
        # set adc2 mux_n w/o mux_p
        (
            {"adc_2_mux_n": CH.AIN5}
        ),
        # set both adc mux_n w/o mux_p
        (
            {"adc_1_mux_n": CH.AIN7, "adc_2_mux_n": CH.AIN5}
        ),
    ]
)
def test_config_raises(mocker, args, adc):
    adc_vals = deepcopy(adc_default_vals)
    # mock each call to __read_register
    mocker.patch(
        "edgepi.adc.edgepi_adc.EdgePiADC._EdgePiADC__read_register",
        side_effect=[
            adc_vals,
        ],
    )
    with pytest.raises(ValueError):
        print(args)
        adc._EdgePiADC__config(**args)


@pytest.mark.parametrize(
    "mux_map, args, expected",
    [
        (
            [0x12, 0x34],
            {
                'adc_1_mux_p': None,
                'adc_2_mux_p': None,
                'adc_1_mux_n': None,
                'adc_2_mux_n': None,
            },
            []
        ),
        (
            [0x12, 0x34],
            {
                'adc_1_mux_p': CH.AIN0,
            },
            [
                OpCode(
                    op_code=0x0A,
                    reg_address=ADCReg.REG_INPMUX.value,
                    op_mask=BitMask.BYTE.value,
                )
            ],
        ),
        (
            [0x12, 0x34],
            {
                'adc_2_mux_p': CH.AIN0,
            },
            [
                OpCode(
                    op_code=0x0A,
                    reg_address=ADCReg.REG_ADC2MUX.value,
                    op_mask=BitMask.BYTE.value,
                )
            ],
        ),
        (
            [0x12, 0x34],
            {
                'adc_1_mux_n': CH.AIN0,
            },
            [],
        ),
        (
            [0x12, 0x34],
            {
                'adc_2_mux_n': CH.AIN0,
            },
            [],
        ),
        (
            [0x12, 0x34],
            {
                'adc_1_mux_p': CH.AIN0,
                'adc_2_mux_p': CH.AIN1,
            },
            [
                OpCode(
                    op_code=0x0A,
                    reg_address=ADCReg.REG_INPMUX.value,
                    op_mask=BitMask.BYTE.value,
                ),
                OpCode(
                    op_code=0x1A,
                    reg_address=ADCReg.REG_ADC2MUX.value,
                    op_mask=BitMask.BYTE.value,
                ),
            ],
        ),
        (
            [0x12, 0x34],
            {
                'adc_1_mux_n': CH.AIN0,
                'adc_2_mux_n': CH.AIN1,
            },
            [],
        ),
        (
            [0x12, 0x34],
            {
                'adc_1_mux_p': CH.AIN6,
                'adc_1_mux_n': CH.AIN7,
            },
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
            {
                'adc_2_mux_p': CH.AIN6,
                'adc_2_mux_n': CH.AIN7,
            },
            [
                OpCode(
                    op_code=0x67,
                    reg_address=ADCReg.REG_ADC2MUX.value,
                    op_mask=BitMask.BYTE.value,
                ),
            ],
        ),
        (
            [0x12, 0x34],
            {
                'adc_1_mux_p': CH.AIN3,
                'adc_1_mux_n': CH.AIN4,
                'adc_2_mux_p': CH.AIN5,
                'adc_2_mux_n': CH.AIN6,
            },
            [
                OpCode(
                    op_code=0x34,
                    reg_address=ADCReg.REG_INPMUX.value,
                    op_mask=BitMask.BYTE.value,
                ),
                OpCode(
                    op_code=0x56,
                    reg_address=ADCReg.REG_ADC2MUX.value,
                    op_mask=BitMask.BYTE.value,
                ),
            ],
        ),
        (
            [0x12, 0x34],
            {
                'adc_1_mux_p': CH.AIN3,
                'adc_1_mux_n': CH.AIN4,
                'adc_2_mux_n': CH.AIN6,
            },
            [
                OpCode(
                    op_code=0x34,
                    reg_address=ADCReg.REG_INPMUX.value,
                    op_mask=BitMask.BYTE.value,
                ),
            ],
        ),
        (
            [0x12, 0x34],
            {
                'adc_1_mux_n': CH.AIN4,
                'adc_2_mux_p': CH.AIN5,
                'adc_2_mux_n': CH.AIN6,
            },
            [
                OpCode(
                    op_code=0x56,
                    reg_address=ADCReg.REG_ADC2MUX.value,
                    op_mask=BitMask.BYTE.value,
                ),
            ],
        ),
    ],
)
def test_get_channel_assign_opcodes(
    mocker, mux_map, args, expected, adc
):
    mocker.patch(
        "edgepi.adc.edgepi_adc.EdgePiADC._EdgePiADC__read_register",
        side_effect=[[mux_map[0]], [mux_map[1]]],
    )
    out = adc._EdgePiADC__get_channel_assign_opcodes(**args)
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
def test_validate_updates(mocker, updated_regs, actual_regs, err):
    mocker.patch("edgepi.peripherals.spi.SPI")
    mocker.patch("edgepi.peripherals.i2c.I2C")
    mocker.patch("edgepi.adc.edgepi_adc.EdgePiGPIO.set_expander_pin")
    mocker.patch("edgepi.adc.edgepi_adc.EdgePiGPIO.clear_expander_pin")
    mocker.patch("edgepi.adc.edgepi_adc.EdgePiADC._EdgePiADC__write_register")
    # mock RTD as off by default, mock as on if needed
    mocker.patch("edgepi.adc.edgepi_adc.EdgePiADC._EdgePiADC__get_rtd_state",
                 return_value=[RTDModes.RTD_OFF, None])
    mocker.patch("edgepi.adc.edgepi_adc.EdgePiADC._EdgePiADC__is_rtd_on", return_value=False)
    mocker.patch("edgepi.adc.edgepi_adc.EdgePiEEPROM")
    adc = EdgePiADC()
    mocker.patch(
        "edgepi.adc.edgepi_adc.EdgePiADC._EdgePiADC__read_registers_to_map",
        return_value=actual_regs,
    )
    with err:
        assert adc._EdgePiADC__validate_updates(updated_regs)


@pytest.mark.parametrize(
    "reference_config, pin_name",
    [
        (ADCReferenceSwitching.GND_SW1.value, ["GNDSW_IN1", "GNDSW_IN2"]),
        (ADCReferenceSwitching.GND_SW2.value, ["GNDSW_IN2", "GNDSW_IN1"]),
        (ADCReferenceSwitching.GND_SW_BOTH.value, ["GNDSW_IN1", "GNDSW_IN2"]),
        (ADCReferenceSwitching.GND_SW_NONE.value, ["GNDSW_IN1", "GNDSW_IN2"]),
    ],
)
def test_set_adc_reference(reference_config, pin_name, adc):
    adc.set_adc_reference(reference_config)
    if reference_config in [1, 2]:
        adc.gpio.set_pin_state.assert_called_with(pin_name[0])
        adc.gpio.clear_pin_state.assert_called_with(pin_name[1])
    elif reference_config == 3:
        adc.gpio.set_pin_state.assert_has_calls([mock.call(pin_name[0]),
                                                    mock.call(pin_name[1])])
    elif reference_config == 0:
        adc.gpio.clear_pin_state.assert_has_calls([mock.call(pin_name[0]),
                                                      mock.call(pin_name[1])])


@pytest.mark.parametrize(
    "updates, rtd_state, err",
    [
        # RTD related setting: RTD1 ON (note: values are irrelevant, only key matters)
        ({"adc_1_ch":CH.AIN0},[RTDModes.RTD_ON,ADCNum.ADC_1],pytest.raises(RTDEnabledError)),
        ({"adc_1_mux_n": CH.AIN0}, [RTDModes.RTD_ON, ADCNum.ADC_1], pytest.raises(RTDEnabledError)),
        ({"idac_1_mux": 0}, [RTDModes.RTD_ON, ADCNum.ADC_1], pytest.raises(RTDEnabledError)),
        ({"idac_2_mux": 0}, [RTDModes.RTD_ON, ADCNum.ADC_1], pytest.raises(RTDEnabledError)),
        ({"idac_1_mag": 0}, [RTDModes.RTD_ON, ADCNum.ADC_1], pytest.raises(RTDEnabledError)),
        ({"idac_2_mag": 0}, [RTDModes.RTD_ON, ADCNum.ADC_1], pytest.raises(RTDEnabledError)),
        ({"pos_ref_inp": 0},[RTDModes.RTD_ON, ADCNum.ADC_1], pytest.raises(RTDEnabledError)),
        ({"neg_ref_inp": 0},[RTDModes.RTD_ON, ADCNum.ADC_1], pytest.raises(RTDEnabledError)),
        # RTD related setting: RTD2 ON (note: values are irrelevant, only key matters)
        ({"adc_2_ch":CH.AIN0},[RTDModes.RTD_ON,ADCNum.ADC_2],pytest.raises(RTDEnabledError)),
        ({"adc_2_mux_n": CH.AIN0}, [RTDModes.RTD_ON, ADCNum.ADC_2], pytest.raises(RTDEnabledError)),
        ({"idac_1_mux": 0}, [RTDModes.RTD_ON, ADCNum.ADC_2], pytest.raises(RTDEnabledError)),
        ({"idac_2_mux": 0}, [RTDModes.RTD_ON, ADCNum.ADC_2], pytest.raises(RTDEnabledError)),
        ({"idac_1_mag": 0}, [RTDModes.RTD_ON, ADCNum.ADC_2], pytest.raises(RTDEnabledError)),
        ({"idac_2_mag": 0}, [RTDModes.RTD_ON, ADCNum.ADC_2], pytest.raises(RTDEnabledError)),
        ({"adc2_ref_inp": 0}, [RTDModes.RTD_ON, ADCNum.ADC_2], pytest.raises(RTDEnabledError)),
        # ADC2 related setting: RTD1 ON (note: values are irrelevant, only key matters)
        ({"adc_2_ch": CH.AIN0}, [RTDModes.RTD_ON, ADCNum.ADC_1], does_not_raise()),
        ({"adc_2_mux_n": CH.AIN0}, [RTDModes.RTD_ON, ADCNum.ADC_1], does_not_raise()),
        ({"adc2_ref_inp": 0}, [RTDModes.RTD_ON, ADCNum.ADC_1], does_not_raise()),
        # ADC1 related setting: RTD2 ON (note: values are irrelevant, only key matters)
        ({"adc_1_ch": CH.AIN0}, [RTDModes.RTD_ON, ADCNum.ADC_2], does_not_raise()),
        ({"adc_1_mux_n": CH.AIN0}, [RTDModes.RTD_ON, ADCNum.ADC_2], does_not_raise()),
        ({"pos_ref_inp": 0}, [RTDModes.RTD_ON, ADCNum.ADC_2], does_not_raise()),
        ({"neg_ref_inp": 0}, [RTDModes.RTD_ON, ADCNum.ADC_2], does_not_raise()),
        # RTD related setting: RTD OFF
        ({"adc_1_ch": CH.AIN0}, [RTDModes.RTD_OFF, None], does_not_raise()),
        ({"adc_1_mux_n": CH.AIN0}, [RTDModes.RTD_OFF, None], does_not_raise()),
        ({"idac_1_mux": 0}, [RTDModes.RTD_OFF, None], does_not_raise()),
        ({"idac_2_mux": 0}, [RTDModes.RTD_OFF, None], does_not_raise()),
        ({"idac_1_mag": 0}, [RTDModes.RTD_OFF, None], does_not_raise()),
        ({"idac_2_mag": 0}, [RTDModes.RTD_OFF, None], does_not_raise()),
        ({"pos_ref_inp": 0}, [RTDModes.RTD_OFF, None], does_not_raise()),
        ({"neg_ref_inp": 0}, [RTDModes.RTD_OFF, None], does_not_raise()),
        # non-RTD related setting: RTD ON
        ({"adc_1_data_rate": ConvMode.PULSE}, [RTDModes.RTD_ON, ADCNum.ADC_1], does_not_raise()),
        ({"adc_2_data_rate": 0}, [RTDModes.RTD_ON, ADCNum.ADC_1], does_not_raise()),
        ({"conversion_mode": 0}, [RTDModes.RTD_ON, ADCNum.ADC_1], does_not_raise()),
        ({"adc_1_data_rate": ConvMode.PULSE}, [RTDModes.RTD_ON, ADCNum.ADC_2], does_not_raise()),
        ({"adc_2_data_rate": 0}, [RTDModes.RTD_ON, ADCNum.ADC_2], does_not_raise()),
        ({"conversion_mode": 0}, [RTDModes.RTD_ON, ADCNum.ADC_2], does_not_raise()),
        # non-RTD related setting: RTD OFF
        ({"adc_1_data_rate": ConvMode.PULSE}, [RTDModes.RTD_OFF, None], does_not_raise()),
        ({"adc_2_data_rate": 0}, [RTDModes.RTD_OFF, None], does_not_raise()),
        ({"conversion_mode": 0}, [RTDModes.RTD_OFF, None], does_not_raise()),
    ],
)
def test_validate_no_rtd_conflict(mocker, updates, rtd_state, err, adc):
    mocker.patch("edgepi.adc.edgepi_adc.EdgePiADC._EdgePiADC__get_rtd_state",return_value=rtd_state)
    with err:
        adc._EdgePiADC__validate_no_rtd_conflict(updates)


@pytest.mark.parametrize(
    "adc_num, diff_mode, config_calls",
    [
        (ADCNum.ADC_1, DiffMode.DIFF_1, {"adc_1_ch": CH.AIN0, "adc_1_mux_n": CH.AIN1}),
        (ADCNum.ADC_2, DiffMode.DIFF_1, {"adc_2_ch": CH.AIN0, "adc_2_mux_n": CH.AIN1}),
        (ADCNum.ADC_1, DiffMode.DIFF_2, {"adc_1_ch": CH.AIN2, "adc_1_mux_n": CH.AIN3}),
        (ADCNum.ADC_2, DiffMode.DIFF_2, {"adc_2_ch": CH.AIN2, "adc_2_mux_n": CH.AIN3}),
        (ADCNum.ADC_1, DiffMode.DIFF_3, {"adc_1_ch": CH.AIN4, "adc_1_mux_n": CH.AIN5}),
        (ADCNum.ADC_2, DiffMode.DIFF_3, {"adc_2_ch": CH.AIN4, "adc_2_mux_n": CH.AIN5}),
        (ADCNum.ADC_1, DiffMode.DIFF_4, {"adc_1_ch": CH.AIN6, "adc_1_mux_n": CH.AIN7}),
        (ADCNum.ADC_2, DiffMode.DIFF_4, {"adc_2_ch": CH.AIN6, "adc_2_mux_n": CH.AIN7}),
        (ADCNum.ADC_1, DiffMode.DIFF_OFF, {"adc_1_ch": CH.FLOAT, "adc_1_mux_n": CH.AINCOM}),
        (ADCNum.ADC_2, DiffMode.DIFF_OFF, {"adc_2_ch": CH.FLOAT, "adc_2_mux_n": CH.AINCOM}),
    ],
)
def test_select_differential(mocker, adc_num, diff_mode, config_calls, adc):
    config = mocker.patch("edgepi.adc.edgepi_adc.EdgePiADC._EdgePiADC__config")
    adc.select_differential(adc_num, diff_mode)
    config.assert_called_once_with(**config_calls)

@pytest.mark.parametrize("enable",[(True), (False)])
def test__set_rtd_pin(enable, adc):
    adc._EdgePiADC__set_rtd_pin(enable)
    if enable:
        adc.gpio.set_pin_state.assert_called_with("RTD_EN")
    else:
        adc.gpio.clear_pin_state.assert_called_with("RTD_EN")

@pytest.mark.parametrize(
    "reg_updates, result_1, result_2",
    [
        ({ADCReg.REG_INPMUX: 0x0A,ADCReg.REG_ADC2MUX: 0x0A},[10, 0],[10, 0]),
        ({ADCReg.REG_INPMUX: 0x1A,ADCReg.REG_ADC2MUX: 0x1A},[10, 1],[10, 1]),
        ({ADCReg.REG_INPMUX: 0x2A,ADCReg.REG_ADC2MUX: 0x2A},[10, 2],[10, 2]),
        ({ADCReg.REG_INPMUX: 0x3A,ADCReg.REG_ADC2MUX: 0x3A},[10, 3],[10, 3]),
        ({ADCReg.REG_INPMUX: 0x4A,ADCReg.REG_ADC2MUX: 0x4A},[10, 4],[10, 4]),
        ({ADCReg.REG_INPMUX: 0x5A,ADCReg.REG_ADC2MUX: 0x5A},[10, 5],[10, 5]),
        ({ADCReg.REG_INPMUX: 0x6A,ADCReg.REG_ADC2MUX: 0x6A},[10, 6],[10, 6]),
        ({ADCReg.REG_INPMUX: 0x7A,ADCReg.REG_ADC2MUX: 0x7A},[10, 7],[10, 7]),
        ({ADCReg.REG_INPMUX: 0x01,ADCReg.REG_ADC2MUX: 0x01},[1, 0],[1, 0]),
        ({ADCReg.REG_INPMUX: 0x23,ADCReg.REG_ADC2MUX: 0x23},[3, 2],[3, 2]),
        ({ADCReg.REG_INPMUX: 0x45,ADCReg.REG_ADC2MUX: 0x45},[5, 4],[5, 4]),
        ({ADCReg.REG_INPMUX: 0x67,ADCReg.REG_ADC2MUX: 0x67},[7, 6],[7, 6]),
    ]
)
def test__check_adc_pins(mocker, reg_updates, result_1, result_2, adc):
    # mock register values and adc state
    mock_regs = deepcopy(adc_default_vals)
    _apply_register_updates(mock_regs, reg_updates)
    mock_state = ADCState(mock_regs)
    mocker.patch("edgepi.adc.edgepi_adc.EdgePiADC.get_state", return_value=mock_state)
    mux_1, mux_2= adc._EdgePiADC__check_adc_pins()
    assert mux_1 == result_1
    assert mux_2 == result_2

@pytest.mark.parametrize("adc_num, result",
                         [(ADCNum.ADC_1, RTDModes.RTD_OFF.value | ADC1RtdConfig.OFF.value),
                          (ADCNum.ADC_2, RTDModes.RTD_OFF.value | ADC2RtdConfig.OFF.value),
                          ])
def test__get_rtd_off_update_config(adc_num, result, adc):
    update= adc._EdgePiADC__get_rtd_off_update_config(adc_num)
    assert update == result

ADC1_RTD_ON_1 = RTDModes.RTD_ON.value | ADC2RtdConfig.OFF.value | ADC1RtdConfig.ON.value
ADC1_RTD_ON_2 = RTDModes.RTD_ON.value | ADC1RtdConfig.ON.value
ADC2_RTD_ON_1 = RTDModes.RTD_ON.value | ADC1RtdConfig.OFF.value | ADC2RtdConfig.ON.value
ADC2_RTD_ON_2 = RTDModes.RTD_ON.value | ADC2RtdConfig.ON.value

@pytest.mark.parametrize("mux_list, adc_num, result",
                         [
                        # Case 1. ADC1 RTD ON, ADC2 Inputs on not allowed channels
                          ([4, 0], ADCNum.ADC_1, ADC1_RTD_ON_1),
                          ([5, 0], ADCNum.ADC_1, ADC1_RTD_ON_1),
                          ([6, 0], ADCNum.ADC_1, ADC1_RTD_ON_1),
                          ([7, 0], ADCNum.ADC_1, ADC1_RTD_ON_1),
                          ([0, 4], ADCNum.ADC_1, ADC1_RTD_ON_1),
                          ([0, 5], ADCNum.ADC_1, ADC1_RTD_ON_1),
                          ([0, 6], ADCNum.ADC_1, ADC1_RTD_ON_1),
                          ([0, 7], ADCNum.ADC_1, ADC1_RTD_ON_1),
                        # Case 2. ADC1 RTD ON, ADC2 Inputs on allowed channels
                          ([0, 0], ADCNum.ADC_1, ADC1_RTD_ON_2),
                          ([1, 0], ADCNum.ADC_1, ADC1_RTD_ON_2),
                          ([2, 0], ADCNum.ADC_1, ADC1_RTD_ON_2),
                          ([3, 0], ADCNum.ADC_1, ADC1_RTD_ON_2),
                          ([0, 0], ADCNum.ADC_1, ADC1_RTD_ON_2),
                          ([0, 1], ADCNum.ADC_1, ADC1_RTD_ON_2),
                          ([0, 2], ADCNum.ADC_1, ADC1_RTD_ON_2),
                          ([0, 3], ADCNum.ADC_1, ADC1_RTD_ON_2),
                        # Case 3. ADC2 RTD ON, ADC2 Inputs on not allowed channels
                          ([4, 0], ADCNum.ADC_2, ADC2_RTD_ON_1),
                          ([5, 0], ADCNum.ADC_2, ADC2_RTD_ON_1),
                          ([6, 0], ADCNum.ADC_2, ADC2_RTD_ON_1),
                          ([7, 0], ADCNum.ADC_2, ADC2_RTD_ON_1),
                          ([0, 4], ADCNum.ADC_2, ADC2_RTD_ON_1),
                          ([0, 5], ADCNum.ADC_2, ADC2_RTD_ON_1),
                          ([0, 6], ADCNum.ADC_2, ADC2_RTD_ON_1),
                          ([0, 7], ADCNum.ADC_2, ADC2_RTD_ON_1),
                        # Case 4. ADC2 RTD ON, ADC2 Inputs on allowed channels
                          ([0, 0], ADCNum.ADC_2, ADC2_RTD_ON_2),
                          ([1, 0], ADCNum.ADC_2, ADC2_RTD_ON_2),
                          ([2, 0], ADCNum.ADC_2, ADC2_RTD_ON_2),
                          ([3, 0], ADCNum.ADC_2, ADC2_RTD_ON_2),
                          ([0, 0], ADCNum.ADC_2, ADC2_RTD_ON_2),
                          ([0, 1], ADCNum.ADC_2, ADC2_RTD_ON_2),
                          ([0, 2], ADCNum.ADC_2, ADC2_RTD_ON_2),
                          ([0, 3], ADCNum.ADC_2, ADC2_RTD_ON_2),
                          ])
def test__get_rtd_on_update_config(mux_list, adc_num, result, adc):
    update= adc._EdgePiADC__get_rtd_on_update_config(mux_list, adc_num)
    assert update == result

@pytest.mark.parametrize(
    "set_rtd, adc_num, adc_mux, config_calls",
    [
    # case 1 ADC_1, ADC_2 inputs on not allowed channel
     (True, ADCNum.ADC_1, [["Dont'care"],[4,10]], ADC1_RTD_ON_1),
     (True, ADCNum.ADC_1, [["Dont'care"],[5,10]], ADC1_RTD_ON_1),
     (True, ADCNum.ADC_1, [["Dont'care"],[6,10]], ADC1_RTD_ON_1),
     (True, ADCNum.ADC_1, [["Dont'care"],[7,10]], ADC1_RTD_ON_1),
    # case 2 ADC_1, ADC_2 inputs on not allowed channel
     (True, ADCNum.ADC_1, [["Dont'care"],[0,10]], ADC1_RTD_ON_2),
     (True, ADCNum.ADC_1, [["Dont'care"],[1,10]], ADC1_RTD_ON_2),
     (True, ADCNum.ADC_1, [["Dont'care"],[2,10]], ADC1_RTD_ON_2),
     (True, ADCNum.ADC_1, [["Dont'care"],[3,10]], ADC1_RTD_ON_2),
    # case 3 ADC_2, ADC_1 inputs on not allowed channel
     (True, ADCNum.ADC_2, [[4,10],["Dont'care"]], ADC2_RTD_ON_1),
     (True, ADCNum.ADC_2, [[5,10],["Dont'care"]], ADC2_RTD_ON_1),
     (True, ADCNum.ADC_2, [[6,10],["Dont'care"]], ADC2_RTD_ON_1),
     (True, ADCNum.ADC_2, [[7,10],["Dont'care"]], ADC2_RTD_ON_1),
    # case 4 ADC_2, ADC_1 inputs on not allowed channel
     (True, ADCNum.ADC_2, [[0,10],["Dont'care"]], ADC2_RTD_ON_2),
     (True, ADCNum.ADC_2, [[1,10],["Dont'care"]], ADC2_RTD_ON_2),
     (True, ADCNum.ADC_2, [[2,10],["Dont'care"]], ADC2_RTD_ON_2),
     (True, ADCNum.ADC_2, [[3,10],["Dont'care"]], ADC2_RTD_ON_2),
    # case 5 ADC1, RTD_OFF
     (False,
      ADCNum.ADC_1,
      [["Dont'care"],["Dont'care"]],
      RTDModes.RTD_OFF.value | ADC1RtdConfig.OFF.value),
     (False,
      ADCNum.ADC_2,
      [["Dont'care"],["Dont'care"]],
      RTDModes.RTD_OFF.value | ADC2RtdConfig.OFF.value),
    ],
)
def test_set_rtd(mocker, set_rtd, adc_num, adc_mux, config_calls, adc):
    mocker.patch("edgepi.adc.edgepi_adc.EdgePiADC._EdgePiADC__check_adc_pins", return_value=adc_mux)
    config = mocker.patch("edgepi.adc.edgepi_adc.EdgePiADC._EdgePiADC__config")
    adc.set_rtd(set_rtd=set_rtd, adc_num=adc_num)
    config.assert_called_once_with(**config_calls, override_rtd_validation=True)


@pytest.mark.parametrize(
    "args, result",
    [
        (
            {
                'adc_1_ch': None,
                'adc_2_ch': None,
                'adc_1_mux_n': None,
                'adc_2_mux_n': None,
            },
            {},
        ),
        (
            {
                'filter_mode': None,
            },
            {},
        ),
        (
            {
                'adc_1_ch': CH.AIN0,
                'adc_2_ch': None,
                'adc_1_mux_n': None,
                'adc_2_mux_n': None,
            },
            {
                'adc_1_mux_p': CH.AIN0,
            },
        ),
        (
            {
                'adc_1_ch': None,
                'adc_2_ch': CH.AIN0,
                'adc_1_mux_n': None,
                'adc_2_mux_n': None,
            },
            {
                'adc_2_mux_p': CH.AIN0,
            },
        ),
        (
            {
                'adc_1_ch': None,
                'adc_2_ch': None,
                'adc_1_mux_n': CH.AIN0,
                'adc_2_mux_n': None,
            },
            {
                'adc_1_mux_n': CH.AIN0,
            },
        ),
        (
            {
                'adc_1_ch': None,
                'adc_2_ch': None,
                'adc_1_mux_n': None,
                'adc_2_mux_n': CH.AIN0,
            },
            {
                'adc_2_mux_n': CH.AIN0,
            },
        ),
        (
            {
                'adc_1_ch': CH.AIN0,
                'adc_2_ch': CH.AIN1,
                'adc_1_mux_n': CH.AIN2,
                'adc_2_mux_n': CH.AIN3,
            },
            {
                'adc_1_mux_p': CH.AIN0,
                'adc_2_mux_p': CH.AIN1,
                'adc_1_mux_n': CH.AIN2,
                'adc_2_mux_n': CH.AIN3,
            },
        ),
    ]
)
def test_extract_mux_args(args, result, adc):
    assert adc._EdgePiADC__extract_mux_args(args) == result

def _apply_register_updates(reg_map: list, updates: dict):
    for addx, value in updates.items():
        reg_map[addx.value] = value

@pytest.mark.parametrize(
    "reg_updates, adc_num, expected, err",
    [
        ({ADCReg.REG_INPMUX: 0x0A}, ADCNum.ADC_1, CalibParam(1, 0), does_not_raise()),
        ({ADCReg.REG_INPMUX: 0x1A}, ADCNum.ADC_1, CalibParam(1, 0), does_not_raise()),
        ({ADCReg.REG_INPMUX: 0x2A}, ADCNum.ADC_1, CalibParam(1, 0), does_not_raise()),
        ({ADCReg.REG_INPMUX: 0x3A}, ADCNum.ADC_1, CalibParam(1, 0), does_not_raise()),
        ({ADCReg.REG_INPMUX: 0x4A}, ADCNum.ADC_1, CalibParam(1, 0), does_not_raise()),
        ({ADCReg.REG_INPMUX: 0x5A}, ADCNum.ADC_1, CalibParam(1, 0), does_not_raise()),
        ({ADCReg.REG_INPMUX: 0x6A}, ADCNum.ADC_1, CalibParam(1, 0), does_not_raise()),
        ({ADCReg.REG_INPMUX: 0x7A}, ADCNum.ADC_1, CalibParam(1, 0), does_not_raise()),
        ({ADCReg.REG_INPMUX: 0x01}, ADCNum.ADC_1, CalibParam(1, 0), does_not_raise()),
        ({ADCReg.REG_INPMUX: 0x23}, ADCNum.ADC_1, CalibParam(1, 0), does_not_raise()),
        ({ADCReg.REG_INPMUX: 0x45}, ADCNum.ADC_1, CalibParam(1, 0), does_not_raise()),
        ({ADCReg.REG_INPMUX: 0x67}, ADCNum.ADC_1, CalibParam(1, 0), does_not_raise()),
        ({ADCReg.REG_ADC2MUX: 0x0A}, ADCNum.ADC_2, CalibParam(1, 0), does_not_raise()),
        ({ADCReg.REG_ADC2MUX: 0x1A}, ADCNum.ADC_2, CalibParam(1, 0), does_not_raise()),
        ({ADCReg.REG_ADC2MUX: 0x2A}, ADCNum.ADC_2, CalibParam(1, 0), does_not_raise()),
        ({ADCReg.REG_ADC2MUX: 0x3A}, ADCNum.ADC_2, CalibParam(1, 0), does_not_raise()),
        ({ADCReg.REG_ADC2MUX: 0x4A}, ADCNum.ADC_2, CalibParam(1, 0), does_not_raise()),
        ({ADCReg.REG_ADC2MUX: 0x5A}, ADCNum.ADC_2, CalibParam(1, 0), does_not_raise()),
        ({ADCReg.REG_ADC2MUX: 0x6A}, ADCNum.ADC_2, CalibParam(1, 0), does_not_raise()),
        ({ADCReg.REG_ADC2MUX: 0x7A}, ADCNum.ADC_2, CalibParam(1, 0), does_not_raise()),
        ({ADCReg.REG_ADC2MUX: 0x01}, ADCNum.ADC_2, CalibParam(1, 0), does_not_raise()),
        ({ADCReg.REG_ADC2MUX: 0x23}, ADCNum.ADC_2, CalibParam(1, 0), does_not_raise()),
        ({ADCReg.REG_ADC2MUX: 0x45}, ADCNum.ADC_2, CalibParam(1, 0), does_not_raise()),
        ({ADCReg.REG_ADC2MUX: 0x67}, ADCNum.ADC_2, CalibParam(1, 0), does_not_raise()),
        ({ADCReg.REG_INPMUX: 0xFA}, ADCNum.ADC_1, None, pytest.raises(ValueError)),
        ({ADCReg.REG_INPMUX: 0x1F}, ADCNum.ADC_1, None, pytest.raises(ValueError)),
        (
            {ADCReg.REG_INPMUX: 0x47}, ADCNum.ADC_1, None,
            pytest.raises(InvalidDifferentialPairError)
        ),
    ]
)
def test_get_calibration_values(mocker, reg_updates, adc_num, expected, err, adc):
    # mock register values and adc state
    mock_regs = deepcopy(adc_default_vals)
    _apply_register_updates(mock_regs, reg_updates)
    mock_state = ADCState(mock_regs)
    mocker.patch("edgepi.adc.edgepi_adc.EdgePiADC.get_state", return_value=mock_state)

    with err:
        out = adc._EdgePiADC__get_calibration_values(adc.adc_calib_params[adc_num], adc_num)
        assert out == expected


@pytest.mark.parametrize("adc_to_read, validate",
    [
        (ADCNum.ADC_1, True),
        (ADCNum.ADC_2, False),
    ]
)
def test_adc_voltage_read_conv_mode_validation(mocker, adc_to_read, validate, adc):
    validate_func = mocker.patch(
        "edgepi.adc.edgepi_adc.EdgePiADC._EdgePiADC__check_adc_1_conv_mode"
    )
    mocker.patch("edgepi.adc.edgepi_adc.EdgePiADC._EdgePiADC__continuous_time_delay")
    mocker.patch("edgepi.adc.edgepi_adc.EdgePiADC._EdgePiADC__voltage_read", return_value=[0,0,0])
    mocker.patch("edgepi.adc.edgepi_adc.EdgePiADC._EdgePiADC__get_calibration_values")
    mocker.patch("edgepi.adc.edgepi_adc.code_to_voltage")
    mocker.patch("edgepi.adc.edgepi_adc.get_adc_status")
    adc.read_voltage(adc_to_read)
    if validate:
        validate_func.assert_called()
    else:
        validate_func.assert_not_called()

@pytest.mark.parametrize("adc_to_read, ch",
    [
        (ADCNum.ADC_1, CH.AINCOM), #single-ended
        (ADCNum.ADC_1, CH.AIN1), #differential
        (ADCNum.ADC_1, CH.AIN2), #differential
        (ADCNum.ADC_2, CH.AINCOM), #differential
        (ADCNum.ADC_2, CH.AIN1),#differential
        (ADCNum.ADC_2, CH.AIN2),#differential
    ]
)
def test_adc_voltage_read_mode(mocker, adc_to_read, ch, adc):
    # changing the ADC1 Input mux negative value to the channel value. This will allow to determine
    # if the adc is in single ended or differential
    if adc_to_read == ADCNum.ADC_1:
        adc_default_vals[6] = 0x10 + ch.value
    else:
        adc_default_vals[22] = 0x10 + ch.value
    mocker.patch(
        "edgepi.adc.edgepi_adc.EdgePiADC._EdgePiADC__read_register",
        return_value=deepcopy(adc_default_vals)
    )
    mocker.patch("edgepi.adc.edgepi_adc.EdgePiADC._EdgePiADC__check_adc_1_conv_mode")
    mocker.patch("edgepi.adc.edgepi_adc.EdgePiADC._EdgePiADC__continuous_time_delay")
    mocker.patch("edgepi.adc.edgepi_adc.EdgePiADC._EdgePiADC__voltage_read", return_value=[0,0,0])
    mocker.patch("edgepi.adc.edgepi_adc.EdgePiADC._EdgePiADC__get_calibration_values")
    differential = mocker.patch("edgepi.adc.edgepi_adc.code_to_voltage")
    single = mocker.patch("edgepi.adc.edgepi_adc.code_to_voltage_single_ended")
    mocker.patch("edgepi.adc.edgepi_adc.get_adc_status")
    adc.read_voltage(adc_to_read)
    if ch == CH.AINCOM:
        single.assert_called_once()
    else:
        differential.assert_called_once()

@pytest.mark.parametrize("adc_to_read, ch",
    [
        (ADCNum.ADC_1, CH.AINCOM), #single-ended
        (ADCNum.ADC_1, CH.AIN1), #differential
        (ADCNum.ADC_1, CH.AIN2), #differential
        (ADCNum.ADC_2, CH.AINCOM), #differential
        (ADCNum.ADC_2, CH.AIN1),#differential
        (ADCNum.ADC_2, CH.AIN2),#differential
    ]
)
def test_adc_single_sample_mode(mocker, adc_to_read, ch, adc):
    # changing the ADC1 Input mux negative value to the channel value. This will allow to determine
    # if the adc is in single ended or differential
    # ADC2 channel shouldn't return differential as well since single sampel only cares about
    # ADC1
    if adc_to_read == ADCNum.ADC_1:
        adc_default_vals[6] = 0x10 + ch.value
    else:
        adc_default_vals[22] = 0x10 + ch.value
    mocker.patch(
        "edgepi.adc.edgepi_adc.EdgePiADC._EdgePiADC__read_register",
        return_value=deepcopy(adc_default_vals)
    )
    mocker.patch("edgepi.adc.edgepi_adc.EdgePiADC.start_conversions")
    mocker.patch("edgepi.adc.edgepi_adc.EdgePiADC._EdgePiADC__voltage_read", return_value=[0,0,0])
    mocker.patch("edgepi.adc.edgepi_adc.EdgePiADC._EdgePiADC__get_calibration_values")
    differential = mocker.patch("edgepi.adc.edgepi_adc.code_to_voltage")
    single = mocker.patch("edgepi.adc.edgepi_adc.code_to_voltage_single_ended")
    mocker.patch("edgepi.adc.edgepi_adc.get_adc_status")
    adc.single_sample()
    if ch == CH.AINCOM and adc_to_read == ADCNum.ADC_1:
        single.assert_called_once()
    else:
        differential.assert_called_once()

@pytest.mark.parametrize("adc_num, mock_val, expected",
    [
        (ADCNum.ADC_1, [161,96]+[255]*5, True),
        (ADCNum.ADC_1, [161,160]+[255]*5, False),
        (ADCNum.ADC_2, [161,160]+[255]*5, True),
        (ADCNum.ADC_2, [161,96]+[255]*5, False),
    ]
)
def test__is_data_ready(mocker,adc_num, mock_val, expected, adc):
    mocker.patch("edgepi.adc.edgepi_adc.EdgePiADC.transfer", return_value = mock_val)
    assert expected == adc._EdgePiADC__is_data_ready(adc_num)

@pytest.mark.parametrize("mock_value, result",
                    [
                        ([True, False],True),
                        ([False, False],False),
                        ([False, True],False),
                        ([True, True],False),
                    ]
)
def test__is_rtd_on(mocker, mock_value, result):
    # mocker.patch("edgepi.adc.edgepi_adc.EdgePiGPIO")
    mocker.patch("edgepi.adc.edgepi_adc.EdgePiEEPROM")
    mocker.patch("edgepi.adc.edgepi_adc.EdgePiADC._EdgePiADC__config")
    mocker.patch("edgepi.adc.edgepi_adc.EdgePiADC.set_adc_reference")
    adc = EdgePiADC()
    mocker.patch("edgepi.adc.edgepi_adc.EdgePiGPIO.read_pin_state", return_value=mock_value[0])
    mocker.patch("edgepi.adc.edgepi_adc.EdgePiGPIO.get_pin_direction", return_value=mock_value[1])
    assert adc._EdgePiADC__is_rtd_on() == result

@pytest.mark.parametrize("param, error",
                    [
                        ([AnalogIn.AIN1,
                          ADC1DataRate.SPS_10,
                          AnalogIn.AIN2,
                          ADC2DataRate.SPS_100,
                          FilterMode.FIR,
                          ConvMode.CONTINUOUS,
                          True], does_not_raise()),
                        ([CH.AIN1,
                          ADC1DataRate.SPS_10,
                          AnalogIn.AIN2,
                          ADC2DataRate.SPS_100,
                          FilterMode.FIR,
                          ConvMode.CONTINUOUS,
                          True], pytest.raises(TypeError)),
                        ([AnalogIn.AIN1,
                          ADC1DataRate.SPS_10,
                          CH.AIN2,
                          ADC2DataRate.SPS_100,
                          FilterMode.FIR,
                          ConvMode.CONTINUOUS,
                          True], pytest.raises(TypeError)),
                    ]
)
def test_set_config(param, error, adc):
    with error:
        adc.set_config(adc_1_analog_in = param[0],
                       adc_1_data_rate = param[1],
                       adc_2_analog_in = param[2],
                       adc_2_data_rate = param[3],
                       filter_mode = param[4],
                       conversion_mode = param[5],
                       override_updates_validation = param[6])
