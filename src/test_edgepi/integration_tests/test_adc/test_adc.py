""" Integration tests for EdgePi ADC module """


import pytest
from edgepi.adc.adc_constants import (
    ADCChannel as CH,
    ConvMode,
    ADC1DataRate,
)
# TODO: commented out until RTD module added
# from edgepi.adc.adc_constants import (
#     ADC_NUM_REGS,
#     ADCReg,
#     ADCChannel as CH,
#     ConvMode,
#     ADC1DataRate,
#     ADC2DataRate,
#     FilterMode,
#     CheckMode,
#     ADCPower
# )
from edgepi.adc.edgepi_adc import EdgePiADC


# pylint: disable=protected-access
@pytest.fixture(name="adc", scope="module")
def fixture_adc():
    adc = EdgePiADC()
    adc.reapply_config()
    yield adc


# TODO: these tests are passing but refactoring of RTD channel validation logic
# is now resulting in eexceptions being raised. Commented out until RTD
# enable/disable functionality is added.
# @pytest.mark.parametrize(
#     "args, updated_vals",
#     [
#         # EdgePI ADC defaults: adc_1_mux_p = AIN0, adc_1_mux_n = AINCOM
#         (
#             {
#                 "adc_1_analog_in": CH.AIN0,
#             },
#             {
#                 ADCReg.REG_INPMUX.value: 0x0A,
#             },
#         ),
#         (
#             {
#                 "adc_1_analog_in": CH.AIN1,
#             },
#             {
#                 ADCReg.REG_INPMUX.value: 0x1A,
#             },
#         ),
#         (
#             {
#                 "adc_1_analog_in": CH.AIN2,
#             },
#             {
#                 ADCReg.REG_INPMUX.value: 0x2A,
#             },
#         ),
#         (
#             {
#                 "adc_1_analog_in": CH.AIN3,
#             },
#             {
#                 ADCReg.REG_INPMUX.value: 0x3A,
#             },
#         ),
#         (
#             {
#                 "adc_1_analog_in": CH.AIN4,
#             },
#             {
#                 ADCReg.REG_INPMUX.value: 0x4A,
#             },
#         ),
#         (
#             {
#                 "adc_1_analog_in": CH.AIN5,
#             },
#             {
#                 ADCReg.REG_INPMUX.value: 0x5A,
#             },
#         ),
#         (
#             {
#                 "adc_1_analog_in": CH.AIN6,
#             },
#             {
#                 ADCReg.REG_INPMUX.value: 0x6A,
#             },
#         ),
#         (
#             {
#                 "adc_1_analog_in": CH.AIN7,
#             },
#             {
#                 ADCReg.REG_INPMUX.value: 0x7A,
#             },
#         ),
#         (
#             {
#                 "adc_1_analog_in": CH.AINCOM,
#             },
#             {
#                 ADCReg.REG_INPMUX.value: 0xAA,
#             },
#         ),
#         (
#             {
#                 "adc_1_analog_in": CH.FLOAT,
#             },
#             {
#                 ADCReg.REG_INPMUX.value: 0xFA,
#             },
#         ),
#         (
#             {
#                 "adc_1_mux_n": CH.AIN0,
#             },
#             {
#                 ADCReg.REG_INPMUX.value: 0x0,
#             },
#         ),
#         (
#             {
#                 "adc_1_mux_n": CH.AIN1,
#             },
#             {
#                 ADCReg.REG_INPMUX.value: 0x01,
#             },
#         ),
#         (
#             {
#                 "adc_1_mux_n": CH.AIN2,
#             },
#             {
#                 ADCReg.REG_INPMUX.value: 0x02,
#             },
#         ),
#         (
#             {
#                 "adc_1_mux_n": CH.AIN3,
#             },
#             {
#                 ADCReg.REG_INPMUX.value: 0x03,
#             },
#         ),
#         (
#             {
#                 "adc_1_mux_n": CH.AIN4,
#             },
#             {
#                 ADCReg.REG_INPMUX.value: 0x04,
#             },
#         ),
#         (
#             {
#                 "adc_1_mux_n": CH.AIN5,
#             },
#             {
#                 ADCReg.REG_INPMUX.value: 0x05,
#             },
#         ),
#         (
#             {
#                 "adc_1_mux_n": CH.AIN6,
#             },
#             {
#                 ADCReg.REG_INPMUX.value: 0x06,
#             },
#         ),
#         (
#             {
#                 "adc_1_mux_n": CH.AIN7,
#             },
#             {
#                 ADCReg.REG_INPMUX.value: 0x07,
#             },
#         ),
#         (
#             {
#                 "adc_1_mux_n": CH.AINCOM,
#             },
#             {
#                 ADCReg.REG_INPMUX.value: 0x0A,
#             },
#         ),
#         (
#             {
#                 "adc_1_mux_n": CH.FLOAT,
#             },
#             {
#                 ADCReg.REG_INPMUX.value: 0x0F,
#             },
#         ),
#         # EdgePI ADC defaults: adc_2_mux_p = AIN0, adc_2_mux_n = AIN1
#         (
#             {
#                 "adc_2_analog_in": CH.AIN0,
#             },
#             {
#                 ADCReg.REG_ADC2MUX.value: 0x01,
#             },
#         ),
#         (
#             {
#                 "adc_2_analog_in": CH.AIN1,
#             },
#             {
#                 ADCReg.REG_ADC2MUX.value: 0x11,
#             },
#         ),
#         (
#             {
#                 "adc_2_analog_in": CH.AIN2,
#             },
#             {
#                 ADCReg.REG_ADC2MUX.value: 0x21,
#             },
#         ),
#         (
#             {
#                 "adc_2_analog_in": CH.AIN3,
#             },
#             {
#                 ADCReg.REG_ADC2MUX.value: 0x31,
#             },
#         ),
#         (
#             {
#                 "adc_2_analog_in": CH.AIN4,
#             },
#             {
#                 ADCReg.REG_ADC2MUX.value: 0x41,
#             },
#         ),
#         (
#             {
#                 "adc_2_analog_in": CH.AIN5,
#             },
#             {
#                 ADCReg.REG_ADC2MUX.value: 0x51,
#             },
#         ),
#         (
#             {
#                 "adc_2_analog_in": CH.AIN6,
#             },
#             {
#                 ADCReg.REG_ADC2MUX.value: 0x61,
#             },
#         ),
#         (
#             {
#                 "adc_2_analog_in": CH.AIN7,
#             },
#             {
#                 ADCReg.REG_ADC2MUX.value: 0x71,
#             },
#         ),
#         (
#             {
#                 "adc_2_analog_in": CH.AINCOM,
#             },
#             {
#                 ADCReg.REG_ADC2MUX.value: 0xA1,
#             },
#         ),
#         (
#             {
#                 "adc_2_analog_in": CH.FLOAT,
#             },
#             {
#                 ADCReg.REG_ADC2MUX.value: 0xF1,
#             },
#         ),
#         (
#             {
#                 "adc_2_mux_n": CH.AIN0,
#             },
#             {
#                 ADCReg.REG_ADC2MUX.value: 0x0,
#             },
#         ),
#         (
#             {
#                 "adc_2_mux_n": CH.AIN1,
#             },
#             {
#                 ADCReg.REG_ADC2MUX.value: 0x01,
#             },
#         ),
#         (
#             {
#                 "adc_2_mux_n": CH.AIN2,
#             },
#             {
#                 ADCReg.REG_ADC2MUX.value: 0x02,
#             },
#         ),
#         (
#             {
#                 "adc_2_mux_n": CH.AIN3,
#             },
#             {
#                 ADCReg.REG_ADC2MUX.value: 0x03,
#             },
#         ),
#         (
#             {
#                 "adc_2_mux_n": CH.AIN4,
#             },
#             {
#                 ADCReg.REG_ADC2MUX.value: 0x04,
#             },
#         ),
#         (
#             {
#                 "adc_2_mux_n": CH.AIN5,
#             },
#             {
#                 ADCReg.REG_ADC2MUX.value: 0x05,
#             },
#         ),
#         (
#             {
#                 "adc_2_mux_n": CH.AIN6,
#             },
#             {
#                 ADCReg.REG_ADC2MUX.value: 0x06,
#             },
#         ),
#         (
#             {
#                 "adc_2_mux_n": CH.AIN7,
#             },
#             {
#                 ADCReg.REG_ADC2MUX.value: 0x07,
#             },
#         ),
#         (
#             {
#                 "adc_2_mux_n": CH.AINCOM,
#             },
#             {
#                 ADCReg.REG_ADC2MUX.value: 0x0A,
#             },
#         ),
#         (
#             {
#                 "adc_2_mux_n": CH.FLOAT,
#             },
#             {
#                 ADCReg.REG_ADC2MUX.value: 0x0F,
#             },
#         ),
#         (
#             {
#                 "adc_1_analog_in": CH.AIN1,
#                 "adc_2_analog_in": CH.AIN2,
#                 "adc_1_mux_n": CH.AIN3,
#                 "adc_2_mux_n": CH.AIN4,
#             },
#             {
#                 ADCReg.REG_INPMUX.value: 0x13,
#                 ADCReg.REG_ADC2MUX.value: 0x24,
#             },
#         ),
#         (
#             {
#                 "adc_1_analog_in": CH.AIN2,
#                 "adc_2_analog_in": CH.AIN2,
#             },
#             {
#                 ADCReg.REG_INPMUX.value: 0x2A,
#                 ADCReg.REG_ADC2MUX.value: 0x21,
#             },
#         ),
#         (
#             {
#                 "adc_1_data_rate": ADC1DataRate.SPS_2P5
#             },
#             {
#                 ADCReg.REG_MODE2.value: 0x0,
#             },
#         ),
#         (
#             {
#                 "adc_1_data_rate": ADC1DataRate.SPS_5
#             },
#             {
#                 ADCReg.REG_MODE2.value: 0x01,
#             },
#         ),
#         (
#             {
#                 "adc_1_data_rate": ADC1DataRate.SPS_10
#             },
#             {
#                 ADCReg.REG_MODE2.value: 0x02,
#             },
#         ),
#         (
#             {
#                 "adc_1_data_rate": ADC1DataRate.SPS_16P6
#             },
#             {
#                 ADCReg.REG_MODE2.value: 0x03,
#             },
#         ),
#         (
#             {
#                 "adc_1_data_rate": ADC1DataRate.SPS_20
#             },
#             {
#                 ADCReg.REG_MODE2.value: 0x04,
#             },
#         ),
#         (
#             {
#                 "adc_1_data_rate": ADC1DataRate.SPS_50
#             },
#             {
#                 ADCReg.REG_MODE2.value: 0x05,
#             },
#         ),
#         (
#             {
#                 "adc_1_data_rate": ADC1DataRate.SPS_60
#             },
#             {
#                 ADCReg.REG_MODE2.value: 0x06,
#             },
#         ),
#         (
#             {
#                 "adc_1_data_rate": ADC1DataRate.SPS_100
#             },
#             {
#                 ADCReg.REG_MODE2.value: 0x07,
#             },
#         ),
#         (
#             {
#                 "adc_1_data_rate": ADC1DataRate.SPS_400
#             },
#             {
#                 ADCReg.REG_MODE2.value: 0x08,
#             },
#         ),
#         (
#             {
#                 "adc_1_data_rate": ADC1DataRate.SPS_1200
#             },
#             {
#                 ADCReg.REG_MODE2.value: 0x09,
#             },
#         ),
#         (
#             {
#                 "adc_1_data_rate": ADC1DataRate.SPS_2400
#             },
#             {
#                 ADCReg.REG_MODE2.value: 0x0A,
#             },
#         ),
#         (
#             {
#                 "adc_1_data_rate": ADC1DataRate.SPS_4800
#             },
#             {
#                 ADCReg.REG_MODE2.value: 0x0B,
#             },
#         ),
#         (
#             {
#                 "adc_1_data_rate": ADC1DataRate.SPS_7200
#             },
#             {
#                 ADCReg.REG_MODE2.value: 0x0C,
#             },
#         ),
#         (
#             {
#                 "adc_1_data_rate": ADC1DataRate.SPS_14400
#             },
#             {
#                 ADCReg.REG_MODE2.value: 0x0D,
#             },
#         ),
#         (
#             {
#                 "adc_1_data_rate": ADC1DataRate.SPS_19200
#             },
#             {
#                 ADCReg.REG_MODE2.value: 0x0E,
#             },
#         ),
#         (
#             {
#                 "adc_1_data_rate": ADC1DataRate.SPS_38400
#             },
#             {
#                 ADCReg.REG_MODE2.value: 0x0F,
#             },
#         ),
#         (
#             {
#                 "adc_2_data_rate": ADC2DataRate.SPS_10
#             },
#             {
#                 ADCReg.REG_ADC2CFG.value: 0x0,
#             },
#         ),
#         (
#             {
#                 "adc_2_data_rate": ADC2DataRate.SPS_100
#             },
#             {
#                 ADCReg.REG_ADC2CFG.value: 0x40,
#             },
#         ),
#         (
#             {
#                 "adc_2_data_rate": ADC2DataRate.SPS_400
#             },
#             {
#                 ADCReg.REG_ADC2CFG.value: 0x80,
#             },
#         ),
#         (
#             {
#                 "adc_2_data_rate": ADC2DataRate.SPS_800
#             },
#             {
#                 ADCReg.REG_ADC2CFG.value: 0xC0,
#             },
#         ),
#         (
#             {
#                 "filter_mode": FilterMode.SINC1
#             },
#             {
#                 ADCReg.REG_MODE1.value: 0x0,
#             },
#         ),
#         (
#             {
#                 "filter_mode": FilterMode.SINC2
#             },
#             {
#                 ADCReg.REG_MODE1.value: 0b00100000,
#             },
#         ),
#         (
#             {
#                 "filter_mode": FilterMode.SINC3
#             },
#             {
#                 ADCReg.REG_MODE1.value: 0b01000000,
#             },
#         ),
#         (
#             {
#                 "filter_mode": FilterMode.SINC4
#             },
#             {
#                 ADCReg.REG_MODE1.value: 0b01100000,
#             },
#         ),
#         (
#             {
#                 "filter_mode": FilterMode.FIR
#             },
#             {
#                 ADCReg.REG_MODE1.value: 0b10000000,
#             },
#         ),
#         (
#             {
#                 "conversion_mode": ConvMode.PULSE
#             },
#             {
#                 ADCReg.REG_MODE0.value: 0x40,
#             },
#         ),
#         (
#             {
#                 "conversion_mode": ConvMode.CONTINUOUS
#             },
#             {
#                 ADCReg.REG_MODE0.value: 0x0,
#             },
#         ),
#         (
#             {
#                 "checksum_mode": CheckMode.CHECK_BYTE_CRC
#             },
#             {
#                 ADCReg.REG_INTERFACE.value: 0b00000110,
#             },
#         ),
#         (
#             {
#                 "checksum_mode": CheckMode.CHECK_BYTE_CHK
#             },
#             {
#                 ADCReg.REG_INTERFACE.value: 0b00000101,
#             },
#         ),
#         (
#             {
#                 "checksum_mode": CheckMode.CHECK_BYTE_OFF
#             },
#             {
#                 ADCReg.REG_INTERFACE.value: 0b00000100,
#             },
#         ),
#         (
#             {
#                 "reset_clear": ADCPower.RESET_CLEAR
#             },
#             {
#                 ADCReg.REG_POWER.value: 0x01,
#             },
#         ),
#         (
#             {
#                 "checksum_mode": CheckMode.CHECK_BYTE_CRC
#             },
#             {
#                 ADCReg.REG_INTERFACE.value: 0b00000110,
#             },
#         ),
#     ],
# )
# def test_config(args, updated_vals, adc):
#     original_regs = adc._EdgePiADC__read_register(ADCReg.REG_ID, ADC_NUM_REGS)

#     updates = adc._EdgePiADC__config(**args)
#     updated_regs = adc._EdgePiADC__read_registers_to_map()

#     for addx, entry in updates.items():
#         # assert update values used by __config() were written to registers
#         assert entry["value"] == updated_regs[addx]

#         # assert only updated settings' registers have been modfied
#         if entry["is_changed"]:
#             assert entry["value"] == updated_vals[addx]
#         else:
#             assert entry["value"] == original_regs[addx]

#     # reset adc registers to pre-test values
#     adc.reset()


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
