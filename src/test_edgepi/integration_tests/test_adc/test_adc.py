""" Integration tests for EdgePi ADC module """

import time

import pytest
from edgepi.adc.adc_constants import (
    ADC_NUM_REGS,
    ADCReg,
    ADCChannel as CH,
    ConvMode,
    ADC1DataRate,
)
from edgepi.adc.edgepi_adc import EdgePiADC

# pylint: disable=protected-access
@pytest.fixture(name="adc", scope="module")
def fixture_adc():
    adc = EdgePiADC()
    yield adc


def test_read_register_individual(adc):
    # read each ADC register individually
    for reg_addx in ADCReg:
        out = adc._EdgePiADC__read_register(reg_addx, 1)
        # output data frame bytes = [null, null, reg_data]
        assert len(out) == 1


# __init__ configures INPMUX = 0xFA


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
                "adc_1_analog_in": CH.AINCOM,
            },
            {
                ADCReg.REG_INPMUX.value: 0xAA,
            },
        ),
        (
            {
                "adc_1_analog_in": CH.AIN1,
                "adc_1_mux_n": CH.AIN1,
            },
            {
                ADCReg.REG_INPMUX.value: 0x11,
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


# def test_read_voltage_pulse(adc):
#     read_len = adc._EdgePiADC__get_data_read_len()
#     adc._EdgePiADC__config(conversion_mode=ConvMode.PULSE)
#     for ch in CH:
#         if ch != CH.FLOAT:
#             args = {
#                 "adc_1_analog_in": ch,
#                 "adc_1_mux_n": CH.FLOAT,
#             }
#             adc._EdgePiADC__config(**args)
#             data = adc.read_voltage()
#             print(data)
#             assert len(data[1:]) == read_len
#             assert data[1:] != [0] * read_len


# def test_read_voltage_continuous(adc):
#     read_len = adc._EdgePiADC__get_data_read_len()
#     adc._EdgePiADC__config(conversion_mode=ConvMode.CONTINUOUS)
#     adc.start_auto_conversions()
#     for ch in CH:
#         if ch != CH.FLOAT:
#             args = {
#                 "adc_1_analog_in": ch,
#                 "adc_1_mux_n": CH.FLOAT,
#             }
#             adc._EdgePiADC__config(**args)
#             data = adc.read_voltage()
#             print(data)
#             assert len(data[1:]) == read_len
#             assert data[1:] != [0] * read_len
#     adc.stop_auto_conversions()


def test_voltage_individual(adc):
    adc._EdgePiADC__config(
        conversion_mode=ConvMode.PULSE,
        adc_1_analog_in=CH.AIN3,
        adc_1_data_rate=ADC1DataRate.SPS_20,
    )
    out = adc.single_sample()
    print(out)


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
            print(out)
    finally:
        adc.stop_conversions()
