""" Integration tests for EdgePi ADC module """


import pytest

# TODO: commented out until RTD module added
from edgepi.adc.adc_constants import (
    ADC_NUM_REGS,
    ADCNum,
    ADCReg,
    ADCChannel as CH,
    ConvMode,
    ADC1DataRate,
    ADC2DataRate,
    FilterMode,
    CheckMode,
    ADCPower,
    IDACMUX,
    IDACMAG,
    REFMUX,
    DiffMode
)
from edgepi.adc.edgepi_adc import EdgePiADC


# pylint: disable=protected-access
@pytest.fixture(name="adc", scope="module")
def fixture_adc():
    adc = EdgePiADC()
    yield adc


# TODO: these tests are passing but refactoring of RTD channel validation logic
# is now resulting in eexceptions being raised. Commented out until RTD
# enable/disable functionality is added.
@pytest.mark.parametrize(
    "args, updated_vals",
    [
        # EdgePI ADC defaults: adc_1_mux_p = AIN0, adc_1_mux_n = AINCOM
        (
            {
                "adc_1_analog_in": CH.AIN0,
            },
            {
                ADCReg.REG_INPMUX.value: 0x0A,
            },
        ),
        (
            {
                "adc_1_analog_in": CH.AIN1,
            },
            {
                ADCReg.REG_INPMUX.value: 0x1A,
            },
        ),
        (
            {
                "adc_1_analog_in": CH.AIN2,
            },
            {
                ADCReg.REG_INPMUX.value: 0x2A,
            },
        ),
        (
            {
                "adc_1_analog_in": CH.AIN3,
            },
            {
                ADCReg.REG_INPMUX.value: 0x3A,
            },
        ),
        (
            {
                "adc_1_analog_in": CH.AIN4,
            },
            {
                ADCReg.REG_INPMUX.value: 0x4A,
            },
        ),
        (
            {
                "adc_1_analog_in": CH.AIN5,
            },
            {
                ADCReg.REG_INPMUX.value: 0x5A,
            },
        ),
        (
            {
                "adc_1_analog_in": CH.AIN6,
            },
            {
                ADCReg.REG_INPMUX.value: 0x6A,
            },
        ),
        (
            {
                "adc_1_analog_in": CH.AIN7,
            },
            {
                ADCReg.REG_INPMUX.value: 0x7A,
            },
        ),
        (
            {
                "adc_1_analog_in": CH.AINCOM,
            },
            {
                ADCReg.REG_INPMUX.value: 0xAA,
            },
        ),
        (
            {
                "adc_1_analog_in": CH.FLOAT,
            },
            {
                ADCReg.REG_INPMUX.value: 0xFA,
            },
        ),
        (
            {
                "adc_1_mux_n": CH.AIN0,
            },
            {
                ADCReg.REG_INPMUX.value: 0x0,
            },
        ),
        (
            {
                "adc_1_mux_n": CH.AIN1,
            },
            {
                ADCReg.REG_INPMUX.value: 0x01,
            },
        ),
        (
            {
                "adc_1_mux_n": CH.AIN2,
            },
            {
                ADCReg.REG_INPMUX.value: 0x02,
            },
        ),
        (
            {
                "adc_1_mux_n": CH.AIN3,
            },
            {
                ADCReg.REG_INPMUX.value: 0x03,
            },
        ),
        (
            {
                "adc_1_mux_n": CH.AIN4,
            },
            {
                ADCReg.REG_INPMUX.value: 0x04,
            },
        ),
        (
            {
                "adc_1_mux_n": CH.AIN5,
            },
            {
                ADCReg.REG_INPMUX.value: 0x05,
            },
        ),
        (
            {
                "adc_1_mux_n": CH.AIN6,
            },
            {
                ADCReg.REG_INPMUX.value: 0x06,
            },
        ),
        (
            {
                "adc_1_mux_n": CH.AIN7,
            },
            {
                ADCReg.REG_INPMUX.value: 0x07,
            },
        ),
        (
            {
                "adc_1_mux_n": CH.AINCOM,
            },
            {
                ADCReg.REG_INPMUX.value: 0x0A,
            },
        ),
        (
            {
                "adc_1_mux_n": CH.FLOAT,
            },
            {
                ADCReg.REG_INPMUX.value: 0x0F,
            },
        ),
        # EdgePI ADC defaults: adc_2_mux_p = AIN0, adc_2_mux_n = AIN1
        (
            {
                "adc_2_analog_in": CH.AIN0,
            },
            {
                ADCReg.REG_ADC2MUX.value: 0x01,
            },
        ),
        (
            {
                "adc_2_analog_in": CH.AIN1,
            },
            {
                ADCReg.REG_ADC2MUX.value: 0x11,
            },
        ),
        (
            {
                "adc_2_analog_in": CH.AIN2,
            },
            {
                ADCReg.REG_ADC2MUX.value: 0x21,
            },
        ),
        (
            {
                "adc_2_analog_in": CH.AIN3,
            },
            {
                ADCReg.REG_ADC2MUX.value: 0x31,
            },
        ),
        (
            {
                "adc_2_analog_in": CH.AIN4,
            },
            {
                ADCReg.REG_ADC2MUX.value: 0x41,
            },
        ),
        (
            {
                "adc_2_analog_in": CH.AIN5,
            },
            {
                ADCReg.REG_ADC2MUX.value: 0x51,
            },
        ),
        (
            {
                "adc_2_analog_in": CH.AIN6,
            },
            {
                ADCReg.REG_ADC2MUX.value: 0x61,
            },
        ),
        (
            {
                "adc_2_analog_in": CH.AIN7,
            },
            {
                ADCReg.REG_ADC2MUX.value: 0x71,
            },
        ),
        (
            {
                "adc_2_analog_in": CH.AINCOM,
            },
            {
                ADCReg.REG_ADC2MUX.value: 0xA1,
            },
        ),
        (
            {
                "adc_2_analog_in": CH.FLOAT,
            },
            {
                ADCReg.REG_ADC2MUX.value: 0xF1,
            },
        ),
        (
            {
                "adc_2_mux_n": CH.AIN0,
            },
            {
                ADCReg.REG_ADC2MUX.value: 0x0,
            },
        ),
        (
            {
                "adc_2_mux_n": CH.AIN1,
            },
            {
                ADCReg.REG_ADC2MUX.value: 0x01,
            },
        ),
        (
            {
                "adc_2_mux_n": CH.AIN2,
            },
            {
                ADCReg.REG_ADC2MUX.value: 0x02,
            },
        ),
        (
            {
                "adc_2_mux_n": CH.AIN3,
            },
            {
                ADCReg.REG_ADC2MUX.value: 0x03,
            },
        ),
        (
            {
                "adc_2_mux_n": CH.AIN4,
            },
            {
                ADCReg.REG_ADC2MUX.value: 0x04,
            },
        ),
        (
            {
                "adc_2_mux_n": CH.AIN5,
            },
            {
                ADCReg.REG_ADC2MUX.value: 0x05,
            },
        ),
        (
            {
                "adc_2_mux_n": CH.AIN6,
            },
            {
                ADCReg.REG_ADC2MUX.value: 0x06,
            },
        ),
        (
            {
                "adc_2_mux_n": CH.AIN7,
            },
            {
                ADCReg.REG_ADC2MUX.value: 0x07,
            },
        ),
        (
            {
                "adc_2_mux_n": CH.AINCOM,
            },
            {
                ADCReg.REG_ADC2MUX.value: 0x0A,
            },
        ),
        (
            {
                "adc_2_mux_n": CH.FLOAT,
            },
            {
                ADCReg.REG_ADC2MUX.value: 0x0F,
            },
        ),
        (
            {
                "adc_1_analog_in": CH.AIN1,
                "adc_2_analog_in": CH.AIN2,
                "adc_1_mux_n": CH.AIN3,
                "adc_2_mux_n": CH.AIN4,
            },
            {
                ADCReg.REG_INPMUX.value: 0x13,
                ADCReg.REG_ADC2MUX.value: 0x24,
            },
        ),
        (
            {
                "adc_1_analog_in": CH.AIN2,
                "adc_2_analog_in": CH.AIN2,
            },
            {
                ADCReg.REG_INPMUX.value: 0x2A,
                ADCReg.REG_ADC2MUX.value: 0x21,
            },
        ),
        (
            {
                "adc_1_data_rate": ADC1DataRate.SPS_2P5
            },
            {
                ADCReg.REG_MODE2.value: 0x0,
            },
        ),
        (
            {
                "adc_1_data_rate": ADC1DataRate.SPS_5
            },
            {
                ADCReg.REG_MODE2.value: 0x01,
            },
        ),
        (
            {
                "adc_1_data_rate": ADC1DataRate.SPS_10
            },
            {
                ADCReg.REG_MODE2.value: 0x02,
            },
        ),
        (
            {
                "adc_1_data_rate": ADC1DataRate.SPS_16P6
            },
            {
                ADCReg.REG_MODE2.value: 0x03,
            },
        ),
        (
            {
                "adc_1_data_rate": ADC1DataRate.SPS_20
            },
            {
                ADCReg.REG_MODE2.value: 0x04,
            },
        ),
        (
            {
                "adc_1_data_rate": ADC1DataRate.SPS_50
            },
            {
                ADCReg.REG_MODE2.value: 0x05,
            },
        ),
        (
            {
                "adc_1_data_rate": ADC1DataRate.SPS_60
            },
            {
                ADCReg.REG_MODE2.value: 0x06,
            },
        ),
        (
            {
                "adc_1_data_rate": ADC1DataRate.SPS_100
            },
            {
                ADCReg.REG_MODE2.value: 0x07,
            },
        ),
        (
            {
                "adc_1_data_rate": ADC1DataRate.SPS_400
            },
            {
                ADCReg.REG_MODE2.value: 0x08,
            },
        ),
        (
            {
                "adc_1_data_rate": ADC1DataRate.SPS_1200
            },
            {
                ADCReg.REG_MODE2.value: 0x09,
            },
        ),
        (
            {
                "adc_1_data_rate": ADC1DataRate.SPS_2400
            },
            {
                ADCReg.REG_MODE2.value: 0x0A,
            },
        ),
        (
            {
                "adc_1_data_rate": ADC1DataRate.SPS_4800
            },
            {
                ADCReg.REG_MODE2.value: 0x0B,
            },
        ),
        (
            {
                "adc_1_data_rate": ADC1DataRate.SPS_7200
            },
            {
                ADCReg.REG_MODE2.value: 0x0C,
            },
        ),
        (
            {
                "adc_1_data_rate": ADC1DataRate.SPS_14400
            },
            {
                ADCReg.REG_MODE2.value: 0x0D,
            },
        ),
        (
            {
                "adc_1_data_rate": ADC1DataRate.SPS_19200
            },
            {
                ADCReg.REG_MODE2.value: 0x0E,
            },
        ),
        (
            {
                "adc_1_data_rate": ADC1DataRate.SPS_38400
            },
            {
                ADCReg.REG_MODE2.value: 0x0F,
            },
        ),
        (
            {
                "adc_2_data_rate": ADC2DataRate.SPS_10
            },
            {
                ADCReg.REG_ADC2CFG.value: 0x0,
            },
        ),
        (
            {
                "adc_2_data_rate": ADC2DataRate.SPS_100
            },
            {
                ADCReg.REG_ADC2CFG.value: 0x40,
            },
        ),
        (
            {
                "adc_2_data_rate": ADC2DataRate.SPS_400
            },
            {
                ADCReg.REG_ADC2CFG.value: 0x80,
            },
        ),
        (
            {
                "adc_2_data_rate": ADC2DataRate.SPS_800
            },
            {
                ADCReg.REG_ADC2CFG.value: 0xC0,
            },
        ),
        (
            {
                "filter_mode": FilterMode.SINC1
            },
            {
                ADCReg.REG_MODE1.value: 0x0,
            },
        ),
        (
            {
                "filter_mode": FilterMode.SINC2
            },
            {
                ADCReg.REG_MODE1.value: 0b00100000,
            },
        ),
        (
            {
                "filter_mode": FilterMode.SINC3
            },
            {
                ADCReg.REG_MODE1.value: 0b01000000,
            },
        ),
        (
            {
                "filter_mode": FilterMode.SINC4
            },
            {
                ADCReg.REG_MODE1.value: 0b01100000,
            },
        ),
        (
            {
                "filter_mode": FilterMode.FIR
            },
            {
                ADCReg.REG_MODE1.value: 0b10000000,
            },
        ),
        (
            {
                "conversion_mode": ConvMode.PULSE
            },
            {
                ADCReg.REG_MODE0.value: 0x40,
            },
        ),
        (
            {
                "conversion_mode": ConvMode.CONTINUOUS
            },
            {
                ADCReg.REG_MODE0.value: 0x0,
            },
        ),
        (
            {
                "checksum_mode": CheckMode.CHECK_BYTE_CRC
            },
            {
                ADCReg.REG_INTERFACE.value: 0b00000110,
            },
        ),
        (
            {
                "checksum_mode": CheckMode.CHECK_BYTE_CHK
            },
            {
                ADCReg.REG_INTERFACE.value: 0b00000101,
            },
        ),
        (
            {
                "checksum_mode": CheckMode.CHECK_BYTE_OFF
            },
            {
                ADCReg.REG_INTERFACE.value: 0b00000100,
            },
        ),
        (
            {
                "reset_clear": ADCPower.RESET_CLEAR
            },
            {
                ADCReg.REG_POWER.value: 0x01,
            },
        ),
        (
            {
                "checksum_mode": CheckMode.CHECK_BYTE_CRC
            },
            {
                ADCReg.REG_INTERFACE.value: 0b00000110,
            },
        ),
        (
            {
                "idac_1_mux": IDACMUX.IDAC1_AIN0,
                "idac_2_mux": IDACMUX.IDAC2_AIN0,
            },
            {
                ADCReg.REG_IDACMUX.value: 0x00,
            },
        ),
        (
            {
                "idac_1_mux": IDACMUX.IDAC1_AIN1,
                "idac_2_mux": IDACMUX.IDAC2_AIN1,
            },
            {
                ADCReg.REG_IDACMUX.value: 0x11,
            },
        ),
        (
            {
                "idac_1_mux": IDACMUX.IDAC1_AIN2,
                "idac_2_mux": IDACMUX.IDAC2_AIN2,
            },
            {
                ADCReg.REG_IDACMUX.value: 0x22,
            },
        ),
        (
            {
                "idac_1_mux": IDACMUX.IDAC1_AIN3,
                "idac_2_mux": IDACMUX.IDAC2_AIN3,
            },
            {
                ADCReg.REG_IDACMUX.value: 0x33,
            },
        ),
        (
            {
                "idac_1_mux": IDACMUX.IDAC1_AIN4,
                "idac_2_mux": IDACMUX.IDAC2_AIN4,
            },
            {
                ADCReg.REG_IDACMUX.value: 0x44,
            },
        ),
        (
            {
                "idac_1_mux": IDACMUX.IDAC1_AIN5,
                "idac_2_mux": IDACMUX.IDAC2_AIN5,
            },
            {
                ADCReg.REG_IDACMUX.value: 0x55,
            },
        ),
        (
            {
                "idac_1_mux": IDACMUX.IDAC1_AIN6,
                "idac_2_mux": IDACMUX.IDAC2_AIN6,
            },
            {
                ADCReg.REG_IDACMUX.value: 0x66,
            },
        ),
        (
            {
                "idac_1_mux": IDACMUX.IDAC1_AIN7,
                "idac_2_mux": IDACMUX.IDAC2_AIN7,
            },
            {
                ADCReg.REG_IDACMUX.value: 0x77,
            },
        ),
        (
            {
                "idac_1_mux": IDACMUX.IDAC1_AIN8,
                "idac_2_mux": IDACMUX.IDAC2_AIN8,
            },
            {
                ADCReg.REG_IDACMUX.value: 0x88,
            },
        ),
        (
            {
                "idac_1_mux": IDACMUX.IDAC1_AIN9,
                "idac_2_mux": IDACMUX.IDAC2_AIN9,
            },
            {
                ADCReg.REG_IDACMUX.value: 0x99,
            },
        ),
        (
            {
                "idac_1_mux": IDACMUX.IDAC1_AINCOM,
                "idac_2_mux": IDACMUX.IDAC2_AINCOM,
            },
            {
                ADCReg.REG_IDACMUX.value: 0xAA,
            },
        ),
        (
            {
                "idac_1_mux": IDACMUX.IDAC1_NO_CONNECT,
                "idac_2_mux": IDACMUX.IDAC2_NO_CONNECT,
            },
            {
                ADCReg.REG_IDACMUX.value: 0xBB,
            },
        ),
        (
            {
                "idac_1_mag": IDACMAG.IDAC1_50,
                "idac_2_mag": IDACMAG.IDAC2_50,
            },
            {
                ADCReg.REG_IDACMAG.value: 0x11,
            },
        ),
        (
            {
                "idac_1_mag": IDACMAG.IDAC1_100,
                "idac_2_mag": IDACMAG.IDAC2_100,
            },
            {
                ADCReg.REG_IDACMAG.value: 0x22,
            },
        ),
        (
            {
                "idac_1_mag": IDACMAG.IDAC1_250,
                "idac_2_mag": IDACMAG.IDAC2_250,
            },
            {
                ADCReg.REG_IDACMAG.value: 0x33,
            },
        ),
        (
            {
                "idac_1_mag": IDACMAG.IDAC1_500,
                "idac_2_mag": IDACMAG.IDAC2_500,
            },
            {
                ADCReg.REG_IDACMAG.value: 0x44,
            },
        ),
        (
            {
                "idac_1_mag": IDACMAG.IDAC1_750,
                "idac_2_mag": IDACMAG.IDAC2_750,
            },
            {
                ADCReg.REG_IDACMAG.value: 0x55,
            },
        ),
        (
            {
                "idac_1_mag": IDACMAG.IDAC1_1000,
                "idac_2_mag": IDACMAG.IDAC2_1000,
            },
            {
                ADCReg.REG_IDACMAG.value: 0x66,
            },
        ),
        (
            {
                "idac_1_mag": IDACMAG.IDAC1_1500,
                "idac_2_mag": IDACMAG.IDAC2_1500,
            },
            {
                ADCReg.REG_IDACMAG.value: 0x77,
            },
        ),
        (
            {
                "idac_1_mag": IDACMAG.IDAC1_2000,
                "idac_2_mag": IDACMAG.IDAC2_2000,
            },
            {
                ADCReg.REG_IDACMAG.value: 0x88,
            },
        ),
        (
            {
                "idac_1_mag": IDACMAG.IDAC1_2500,
                "idac_2_mag": IDACMAG.IDAC2_2500,
            },
            {
                ADCReg.REG_IDACMAG.value: 0x99,
            },
        ),
        (
            {
                "idac_1_mag": IDACMAG.IDAC1_3000,
                "idac_2_mag": IDACMAG.IDAC2_3000,
            },
            {
                ADCReg.REG_IDACMAG.value: 0xAA,
            },
        ),
        (
            {
                "idac_1_mag": IDACMAG.IDAC1_OFF,
                "idac_2_mag": IDACMAG.IDAC2_OFF,
            },
            {
                ADCReg.REG_IDACMAG.value: 0x0,
            },
        ),
        (
            {
                "pos_ref_inp": REFMUX.POS_REF_EXT_AIN0,
                "neg_ref_inp": REFMUX.NEG_REF_EXT_AIN1,
            },
            {
                ADCReg.REG_REFMUX.value: 0b00001001,
            },
        ),
        (
            {
                "pos_ref_inp": REFMUX.POS_REF_EXT_AIN2,
                "neg_ref_inp": REFMUX.NEG_REF_EXT_AIN3,
            },
            {
                ADCReg.REG_REFMUX.value: 0b00010010,
            },
        ),
        (
            {
                "pos_ref_inp": REFMUX.POS_REF_EXT_AIN4,
                "neg_ref_inp": REFMUX.NEG_REF_EXT_AIN5,
            },
            {
                ADCReg.REG_REFMUX.value: 0b00011011,
            },
        ),
        (
            {
                "pos_ref_inp": REFMUX.POS_REF_INT_VAVDD,
                "neg_ref_inp": REFMUX.NEG_REF_INT_VAVSS,
            },
            {
                ADCReg.REG_REFMUX.value: 0b00100100,
            },
        ),
        (
            {
                "pos_ref_inp": REFMUX.POS_REF_INT_2P5,
                "neg_ref_inp": REFMUX.NEG_REF_INT_2P5,
            },
            {
                ADCReg.REG_REFMUX.value: 0x0,
            },
        ),
    ],
)
def test_config(args, updated_vals, adc):
    original_regs = adc._EdgePiADC__read_register(ADCReg.REG_ID, ADC_NUM_REGS)

    updates = adc._EdgePiADC__config(**args)
    updated_regs = adc._EdgePiADC__read_registers_to_map()

    for addx, entry in updates.items():
        # assert update values used by __config() were written to registers
        assert entry["value"] == updated_regs[addx]

        # assert only updated settings' registers have been modfied
        if entry["is_changed"]:
            assert entry["value"] == updated_vals[addx]
        else:
            assert entry["value"] == original_regs[addx]

    # reset adc registers to pre-test values
    adc.reset()


def test_voltage_individual(adc):
    adc._EdgePiADC__config(
        conversion_mode=ConvMode.PULSE,
        adc_1_analog_in=CH.AIN3,
        adc_1_data_rate=ADC1DataRate.SPS_20,
    )
    out = adc.single_sample()
    assert out != 0


def test_voltage_continuous(adc):
    try:
        adc._EdgePiADC__config(
            conversion_mode=ConvMode.CONTINUOUS,
            adc_1_analog_in=CH.AIN3,
            adc_1_data_rate=ADC1DataRate.SPS_20,
        )
        adc.start_conversions()
        for _ in range(10):
            out = adc.read_voltage()
            assert out != 0
    finally:
        adc.stop_conversions()


@pytest.mark.parametrize('adc_num, diff, mux_reg, mux_reg_val',
    [
        (ADCNum.ADC_1, DiffMode.DIFF_1, ADCReg.REG_INPMUX, 0x01),
        (ADCNum.ADC_1, DiffMode.DIFF_2, ADCReg.REG_INPMUX, 0x23),
        (ADCNum.ADC_1, DiffMode.DIFF_3, ADCReg.REG_INPMUX, 0x45),
        (ADCNum.ADC_1, DiffMode.DIFF_4, ADCReg.REG_INPMUX, 0x67),
        (ADCNum.ADC_1, DiffMode.DIFF_OFF, ADCReg.REG_INPMUX, 0x0A),
    ]
)
def test_select_differential(adc_num, diff, mux_reg, mux_reg_val, adc):
    adc.select_differential(adc_num, diff)
    assert adc._EdgePiADC__read_register(mux_reg) == [mux_reg_val]


@pytest.mark.parametrize(
    "enable",
    [
        (True),
        (False)
    ]
)
def test_rtd_mode(enable, adc):
    # TODO: pass if no error raised for now, check RTD is on once get_state is implemented
    adc.rtd_mode(enable=enable)
